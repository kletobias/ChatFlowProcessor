## Table of Contents
- [ChatFlowProcessor](#chatflowprocessor)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Markdown File Structure](#markdown-file-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Examples](#examples)
  - [Input: Sample Message](#input-sample-message)
  - [Output: Markdown from Sample Message](#output-markdown-from-sample-message)
  - [Full Chat Conversation Example](#full-chat-conversation-example)
- [Rendering of User Messages](#rendering-of-user-messages)
  - [Overview](#overview)
  - [Formatting Details](#formatting-details)
  - [Developer Implications](#developer-implications)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)


# ChatFlowProcessor

Efficiently transform your OpenAI chat transcripts, exported as a zip file, into well-structured markdown files. Each file represents an individual chat session, processed locally for convenience and efficiency.

## Features

- **Command Line Tool**: Easily used as a command line tool for quick processing.
- **Local Processing**: Unzips the downloaded OpenAI user data and processes the `conversations.json` file on your machine.
- **Session Splitting**: Splits the data by individual chat sessions for organized documentation.

## Directory Structure

- The [script](script/chatflowprocessor.py) requires the path to the .zip file as input.
- It creates a `unzipped_data` directory within the zip file's parent directory.
- Extracts the zip contents into `unzipped_data`.
- Inside `unzipped_data`, a `chat-export-by-conversation` directory is created.
- Each chat is saved as a Markdown file inside `chat-export-by-conversation`.

```css
| Line | Code |
| ---- | ---- |
| 1    | .    |
| 2    | ├── your_chat_data.zip |
| 3    | └── unzipped_data |
| 4    |     ├── chat-export-by-conversation  [1337 entries exceeds filelimit, not opening dir] |
| 5    |     ├── chat.html |
| 6    |     ├── conversations.json |
| 7    |     ├── message_feedback.json |
| 8    |     ├── model_comparisons.json |
| 9    |     ├── shared_conversations.json |
| 10   |     └── user.json |
```

## Markdown File Structure

- Each `.md` file in `chat-export-by-conversation` contains all messages from one chat session.
- Filenames follow the pattern `chat-{title_file}.md`, where `title_file` is a sanitized version of the `title`.
- Generates unique filenames to prevent overwriting.
- File Structure:
    - The first line: H1 heading with the chat `title`.
    - Messages are under H2 headings titled `## User:` or `## ChatGPT:`, reconstructing the original chat flow.

## Getting Started

### Prerequisites

- Python 3.x
- Required packages: `pathlib`, `json`, `re`

### Installation

```bash
git clone https://github.com/yourusername/ChatFlowProcessor.git
cd ChatFlowProcessor
```

### Usage

As a command line script, the required argument is `--zip_file_path` which is the file path to the downloaded OpenAI chat data. See [Directory Structure](#directory-structure).


```bash
python chatflowprocessor.py --zip_file_path "/path/to/zip_file"
```


Optional command line argument `--verbose` can be passed to the script, to make the output more verbose.


```bash
python chatflowprocessor.py --zip_file_path "/path/to/zip_file" --verbose
```


## Examples

### Input: Sample Message
Go from this `content`:

```json
{
    "part_type": "AssistantMessage",
    "payload": {
        "content": "To showcase a Python code block featuring the walrus operator (`:=`), formatted in the Black code style for a Markdown environment, we can create a small, readable example. The walrus operator is useful for assignments within expressions, allowing for a more concise code. Here, I'll create a snippet that uses this operator in a loop to process a list of numbers. The code will be designed to adhere to the Black formatter's style, focusing on readability and consistency. The example will be within 10 lines, making it suitable for a Markdown code block showcase.\n\n```python\ndef process_numbers(numbers: List[int]) -> List[int]:\n    result = []\n    for number in numbers:\n        if (squared := number ** 2) > 20:\n            result.append(squared)\n    return result\n\n# Example usage\nnumbers = [1, 2, 3, 4, 5]\nprint(process_numbers(numbers))\n```\n\nThis code demonstrates the use of the walrus operator in a loop, checking if the square of a number is greater than 20, and if so, appending it to the `result` list. The function `process_numbers` takes a list of integers and returns a new list with the squared values that meet the condition. This example is formatted according to Black's style guidelines, ensuring it is visually appealing for a Markdown code block."
    },
    "id": "[Message ID]",
    "timestamp": "[Timestamp]"
}
```

### Output: Markdown from Sample Message

To showcase a Python code block featuring the walrus operator (`:=`), formatted in the Black code style for a Markdown environment, we can create a small, readable example. The walrus operator is useful for assignments within expressions, allowing for a more concise code. Here, I'll create a snippet that uses this operator in a loop to process a list of numbers. The code will be designed to adhere to the Black formatter's style, focusing on readability and consistency. The example will be within 10 lines, making it suitable for a Markdown code block showcase.

```python
def process_numbers(numbers: List[int]) -> List[int]:
    result = []
    for number in numbers:
        if (squared := number ** 2) > 20:
            result.append(squared)
    return result

# Example usage
numbers = [1, 2, 3, 4, 5]
print(process_numbers(numbers))
```

This code demonstrates the use of the walrus operator in a loop, checking if the square of a number is greater than 20, and if so, appending it to the `result` list. The function `process_numbers` takes a list of integers and returns a new list with the squared values that meet the condition. This example is formatted according to Black's style guidelines, ensuring it is visually appealing for a Markdown code block.

### Full Chat Conversation Example
You find a sample chat conversation in `.json`, `.md`, and as a rendered image in [examples](/examples)

## Rendering of User Messages

### Overview

- **Distinct Formatting**: User messages in the markdown files are formatted distinctly for clarity.
- **Markdown Compliance**: Messages retain original Markdown formatting.

### Formatting Details

- **Headings**: User messages start with an H2 heading (`## User:`).
- **Markdown Elements**: Lists, links, code blocks, emphasis, etc., are preserved.
- **Non-Code Block Syntax**: Markdown elements outside code blocks render as intended.

### Developer Implications

- **Rendering Behavior**: Be aware of how Markdown syntax affects rendering.
- **Documentation Use**: Useful for documentation or training where formatting is key.

## Contributing

Contributions are welcome. Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [MIT LICENSE](LICENSE) file for details.

## Contact

Tobias Klein - progress (dot) unveiled (at) gmail (dot) com 
Website: [www.deep-learning-master.com](https://deep-learning-master.com)
Project Link: https://github.com/kletobias/ChatFlowProcessor
