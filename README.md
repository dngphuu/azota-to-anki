# Azota to Anki Converter

A Python CLI tool to convert Azota exam result HTML files into Anki-importable flashcards (CSV format).

## Features

-   **Automatic Parsing**: Extracts questions, options, and correct answers from Azota HTML result pages.
-   **Anki Compatible**: Generates CSV files ready for import into Anki (semicolon-separated).
-   **Smart Detection**: Warns if questions are not fully loaded (skeleton blocks) in the HTML.
-   **Batch Processing**: Process a single file or all files in the input directory.

## Prerequisites

-   Python 3.12+
-   `uv` (recommended for package management)

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/dngphuu/azota-to-anki.git
    cd azota-to-anki
    ```

2.  Install dependencies:
    ```bash
    uv venv
    uv pip install -r requirements.txt
    ```

## Usage

1.  **Prepare Input**:
    -   Open your Azota exam result page in a browser.
    -   **Scroll to the bottom** to ensure all questions are loaded.
    -   Save the page as HTML (Ctrl+S).
    -   Place the saved HTML file(s) in the `input` directory.

2.  **Run the Tool**:
    ```bash
    uv run python azota_to_anki.py
    ```

3.  **Select Files**:
    -   The tool will list available HTML files.
    -   Enter the number of the file to process, or type `all` to process everything.

4.  **Import to Anki**:
    -   Open Anki.
    -   Go to **File** -> **Import**.
    -   Select the generated `.csv` file from the `output` directory.
    -   **Settings**:
        -   Separator: **Semicolon (;)**
        -   Allow HTML in fields: **Checked**
        -   Map Field 1 to **Front** and Field 2 to **Back**.

## Project Structure

```
azota-to-anki/
├── input/          # Place HTML files here
├── output/         # Generated CSV files appear here
├── azota_to_anki.py # Main script
├── requirements.txt
└── README.md
```

## License

MIT
