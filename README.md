# ChatFlowProcessor

Efficiently transform your OpenAI chat transcripts, exported as a zip file, into well-structured markdown files, each representing an individual chat session, using a local processing approach.

## Features

- Can be used as Command line tool or standalone python script.
- Unzips the downloaded OpenAI user data, and processes `conversations.json` file.
- Splits by chat

### Input



```css
| Line | Code |
| ---- | ---- |
| 1    | .    |
| 2    | ├── c4158bd210b5ede180fb368313c2377cc4f3fa2c07c08b3be367fbd43f2cd5b1-2024-01-05-15-11-33.zip |
| 3    | └── unzipped_data |
| 4    |     ├── chat-export-by-conversation  [1227 entries exceeds filelimit, not opening dir] |
| 5    |     ├── chat.html |
| 6    |     ├── conversations.json |
| 7    |     ├── message_feedback.json |
| 8    |     ├── model_comparisons.json |
| 9    |     ├── shared_conversations.json |
| 10   |     └── user.json |
```

### Processing of `conversations.json`
- TODO: add details of how the file is split into chats

### Export to Markdown Files
- Each `.md` file in directory `chat-export-by-conversation` contains all messages of one chat.
- Filenames generally follow the pattern `chat-{title_file}.md`, see [Construction of Filenames](line 198) in script defined TODO: make less specific and more.
- Unique filenames for markdown files are generated in case of the filename already existing, to prevent overwriting.
- The structure for each file is the following:
    - First line of the file: H1 heading with the value of node `title`.
    - Each H2 heading titled `## User:`, or `## ChatGPT:` is followed by one message from either the user or ChatGPT respectively reconstructing the flow in the original chat from the browser UI.
    - For more details on the rendering of user messages see section [Rendering of User Messages](#rendering-of-user-messages)

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages: `pathlib`, `json`, `re`

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/ChatFlowProcessor.git
cd ChatFlowProcessor
```

### Usage

Run the main script and provide necessary arguments:

```bash
python chatflowprocessor.py --zip-file-path "/path/to/zip_file"
```

## Functions

- `unzip_file(zip_file_path, verbose)`: Unzips the provided zip file.
- `process_conversation(conversation, out_dir, verbose)`: Processes individual conversations and saves them in markdown format.


## Rendering of User Messages

### Overview
The markdown files exported from OpenAI Chat contain user messages formatted distinctly for clarity and structured navigation. This section provides an in-depth explanation of how user messages are rendered in markdown format in these exports.

### Formatting Details
- **Heading Identification:** Each user message in the conversation starts with an H2 heading, denoted as `## User:` in the markdown file. This format aids in differentiating user messages from other parts of the conversation.

- **Markdown Compliance:** The correct rendering of user messages in markdown depends on whether the original message adhered to standard Markdown syntax. This means that lists, links, code blocks, emphasis, and other Markdown elements will render as intended if they were used correctly in the user's message.

- **Non-Code Block Markdown Syntax:** Crucially, any Markdown syntax in the user's message that is not enclosed within a Markdown code block (initiated with ```` ```md ````) will be rendered as per its markdown nature in the exported file. This implies that:
  - Additional headings (e.g., `#`, `##`, `###`) will be rendered as headings.
  - Bullet points and numbered lists will appear as lists.
  - Hyperlinks (`[text](URL)`) will be clickable links.
  - Text enclosed in asterisks (`*text*` or `**text**`) will be italicized or bolded, respectively.

### Implications for Developers
- **Awareness of Rendering Behavior:** When using these exports in documentation or repositories, developers should note that the accuracy of rendering is linked to both the user's use of Markdown syntax and the placement of Markdown elements inside or outside of code blocks. Non-compliant or incorrectly placed elements might render unexpectedly.
  
- **Enhanced Documentation Potential:** Understanding this rendering behavior can be advantageous in cases where conversations are being used for documentation, training, or examples in public repositories, especially for illustrating Markdown usage or formatting examples.

## Contributing

Contributions to ChatFlowProcessor are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - your.email@example.com

Project Link: https://github.com/yourusername/ChatFlowProcessor
```

Remember to replace placeholders like `yourusername`, `Your Name`, and `your.email@example.com` with your actual GitHub username, name, and contact email. You may also want to adjust the sections to better reflect the specifics of your project, such as detailed usage instructions, configuration options, or additional functionalities.
