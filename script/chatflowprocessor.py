import argparse
from pathlib import Path
from slugify import slugify
import json
import re
from typing import Dict, List
import zipfile


def validate_and_get_absolute_zip_path(zip_file_path: str) -> str:
    """
    Validates the given zip file path and returns its absolute path.

    This function checks if the provided path exists, if it points to a file,
    and if the file has a .zip extension. If any of these checks fail, it raises
    a ValueError with an appropriate message.

    Args:
        zip_file_path (str): The path to the zip file, taken from the user input for command line argument `--zip_file_path`

    Returns:
        Path (str): The absolute path object of the zip file.

    Raises:
        ValueError: If the path does not exist, if not a file, or is not a .zip file.
    """
    zip_path = Path(zip_file_path).resolve()
    # Check if the path exists
    if not zip_path.exists():
        raise ValueError(f"The provided path does not exist: {zip_path}")

    # Check if Path zip_path is a file
    if not zip_path.is_file():
        raise ValueError(f"The Path is not a file: {zip_path}")

    # Check if Path zip_path has file extension zip
    if zip_path.suffix.lower() != ".zip":
        raise ValueError(f"The Path is not a zip file: {zip_path}")

    return str(zip_path)


def unzip_file(zip_file_path: Path, verbose: bool = False) -> None:
    """
    Unzips the downloaded `.zip` file in a new child directory with the exported data from OpenAI of the user, if there is not already a child directory in the zip file path named `unzipped_data` containing files. It exits without unzipping otherwise.

    Args:
        zip_file_path (Path): Absolute file path to the zip archive with all chats.
        verbose (bool): If True, enables verbose output, printing detailed messages during execution. Default is False.
    """

    output_directory_path = zip_file_path.parent / "unzipped_data"

    if output_directory_path.exists() and any(output_directory_path.iterdir()):
        if verbose:
            print(
                f"Output directory {output_directory_path} already exists and is not empty. Skipping extraction."
            )
        return

    output_directory_path.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(output_directory_path)
        if verbose:
            print(f"Extracted {zip_file_path} to {output_directory_path}")
    except zipfile.BadZipFile:
        print(f"Error: Invalid zip file {zip_file_path}")
    except Exception as e:
        print(f"Extraction error: {e}")


def get_conversation_messages(conversation: Dict) -> List[Dict[str, str]]:
    """
    Extracts messages from a given conversation.

    This function processes a conversation dictionary, typically obtained from OpenAI's exported chat data.
    It identifies and extracts messages, assigning 'ChatGPT' or 'User' as the author, and omits non-message nodes
    like instructions or system messages. The extracted messages maintain valid markdown syntax, suitable for
    markdown file representation, including TeX math, code blocks, etc.

    The conversation is processed in reverse order, starting from the last message to the first. The final output
    is a list of messages in the correct chronological order.

    Args:
        conversation (Dict): A dictionary representing a single chat conversation, as formatted in OpenAI's chat export.

    Returns:
        List[Dict[str, str]]: A list of message dictionaries, each containing 'author' and 'text' keys.
    """
    messages = []
    current_node = conversation["current_node"]

    while current_node:
        node = conversation["mapping"][current_node]
        message = node.get("message")

        if not message or not isinstance(content := message.get("content"), dict):
            current_node = node.get("parent")
            continue

        author_info = message.get("author", {})
        author_role = author_info.get("role")
        if (
            not author_info
            or author_role not in {"assistant", "user"}
            or author_info.get("name") == "browser"
        ):
            current_node = node.get("parent")
            continue

        author = "ChatGPT" if author_role == "assistant" else "User"

        if content.get("content_type") in {"text", "code"}:
            text = (
                content.get("parts")[0]
                if content.get("parts")
                else content.get("text", "")
            )
        else:
            text = content.get("text", "")

        # Filter messages that contain string 'mclick', as they are part of the logging when GPT uses the browser.
        if text and author == "ChatGPT":
            if "mclick([" not in text and not text.endswith(")]"):
                messages.append({"author": author, "text": text})
        elif text and author == "User":
            messages.append({"author": author, "text": text})

        current_node = node.get("parent")

    return list(reversed(messages))


def get_unique_filename(path: Path) -> Path:
    """
    Generates a unique file path for a Markdown file.

    This function accepts a Path object targeting a '.md' file and checks for its existence. If the file does not exist,
    the original Path is returned. If it exists, the function appends an incrementing integer to the file's stem (before
    the extension) until a unique file path is found.

    Args:
        path (Path): An absolute Path object representing the intended location and filename of an exported '.md' file.

    Returns:
        Path: A Path object representing a unique file path for the file.
    """
    counter = 1
    new_path = path
    while new_path.exists():
        new_path = path.parent / f"{path.stem}-{counter}{path.suffix}"
        counter += 1
    return new_path


def write_text_file(text_file: Path, content: str, append: bool = True) -> None:
    """
    Writes content to a text file.

    Args:
        text_file (Path): The path of the text file.
        content (str): The content to be written.
        append (bool): If True, appends the content to the file. Default is True.
    """
    mode = "a" if append else "w"
    with open(text_file, mode, encoding="utf-8") as f:
        f.write(content)


def process_conversation(
    conversation: Dict, out_dir: Path, verbose: bool = False
) -> None:
    """
    Processes a single conversation, creating a markdown file with its content.

    This function performs several checks to ensure the validity of inputs and
    handles errors during the processing. It validates the type and integrity of
    the `conversation` dictionary, checks the validity of the `out_dir` path, and
    captures exceptions during file operations.

    Args:
        conversation (Dict): A dictionary representing the conversation to be processed.
                              Must contain a 'title' key with a string value.
                              Each message in the conversation should contain 'author'
                              and 'text' keys.
        out_dir (Path): The output directory where the markdown file will be saved.
                        Must be a valid directory path.
        verbose (bool): If True, prints additional information during processing
                        and any error occurrences. Default is False.

    Raises:
        TypeError: If `conversation` is not a dictionary or `out_dir` is not a Path object.
        ValueError: If `out_dir` does not exist or is not a directory, or if
                    necessary keys are missing in `conversation`.
        Exception: Propagates any exceptions that occur during file writing.

    Note:
        The function relies on external functions `slugify`, `get_unique_filename`,
        `write_text_file`, and `get_conversation_messages`, which need to be defined.
    """
    if not isinstance(conversation, dict):
        raise TypeError("conversation must be a dictionary")
    if not isinstance(out_dir, Path):
        raise TypeError("out_dir must be a Path object")
    if not out_dir.is_dir():
        raise ValueError("out_dir does not exist or is not a directory")

    title = conversation.get("title", "").strip()
    if title is None or not isinstance(title, str):
        raise ValueError("title missing or not a string in conversation")

    title_file = slugify(
        title if "{" not in title and len(title) < 60 else "Conversation"
    )

    try:
        md_filepath = get_unique_filename(out_dir / f"chat-{title_file}.md")
        write_text_file(md_filepath, f"# {title}\n", append=False)
        messages = get_conversation_messages(conversation)
        for message in messages:
            message_content = f"## {message['author']}:\n{message['text']}\n\n"
            write_text_file(
                md_filepath, re.sub(r"^\n{3,}", "\n\n", message_content), append=True
            )
        if verbose:
            print(f"Conversation processed and saved to {md_filepath}")
    except Exception as e:
        if verbose:
            print(f"Error processing conversation {e}")
        raise


def main(
    zip_file_path: str,
    verbose: bool = False,
) -> None:
    """
    Main function to process conversations from a zip file.

    Args:
        zip_file_path (str): Path to the downloaded zip file.
        verbose (bool): Enables verbose output if True. Default is False.
    """

    zip_file_path = validate_and_get_absolute_zip_path(zip_file_path)
    unzip_file(Path(zip_file_path), verbose)

    # File 'conversations.json' is one of the files in the `.zip` archive.
    json_file = Path(zip_file_path).parent / "unzipped_data" / "conversations.json"

    out_dir = json_file.parent / "chat-export-by-conversation"
    out_dir.mkdir(parents=True, exist_ok=True)

    with json_file.open(encoding="utf-8") as file:
        json_data = json.load(file)

    for conversation in json_data:
        process_conversation(conversation, out_dir, verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Give the file path to your zip file containing the downloaded data. Export each conversation in the zip file as a separate markdown file."
    )
    parser.add_argument(
        "--zip_file_path",
        type=str,
        required=True,
        help="Path to the downloaded zip file",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Increase output verbosity"
    )
    args = parser.parse_args()
    main(args.zip_file_path, args.verbose)
