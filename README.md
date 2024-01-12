# ChatFlowProcessor

Efficiently transform your OpenAI chat transcripts, exported as a zip file, into well-structured markdown files, each representing an individual chat session, using a local processing approach.

## Features

- Command line tool.
- Unzip and process chat export files.

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

### Functions

- `unzip_file(zip_file_path, verbose)`: Unzips the provided zip file.
- `process_conversation(conversation, out_dir, verbose)`: Processes individual conversations and saves them in markdown format.

## Contributing

Contributions to ChatFlowProcessor are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - your.email@example.com

Project Link: https://github.com/yourusername/ChatFlowProcessor
```

Remember to replace placeholders like `yourusername`, `Your Name`, and `your.email@example.com` with your actual GitHub username, name, and contact email. You may also want to adjust the sections to better reflect the specifics of your project, such as detailed usage instructions, configuration options, or additional functionalities.
