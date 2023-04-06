# PDF Financial Statement Extractor 📚🔍

This Python script extracts tables containing specific keywords, such as "Revenue" and "Income," from a collection of PDF files in the specified input directory and saves the extracted tables as Excel files in the specified output directory.

## Features ✨

- Extract tables with specific keywords from PDF files
- Parallel processing for faster extraction
- Customizable regex pattern for keyword search
- Error handling and logging for better traceability
- Supports specifying input and output directories

## Installation 🛠️

### Dependencies

- Python 3.7 or higher
- [pdfgrep](https://pdfgrep.org/) (system package)

### Steps

1. Clone the repository or download the script:

```
git clone financial-statement-pdf-extractor.git
```

Install the Python dependencies using pip:
```
pip install -r requirements.txt 
```

Install the pdfgrep package using your system's package manager:
For Ubuntu:

```
sudo apt-get install pdfgrep
```

For macOS:
```
brew install pdfgrep
```
## Usage

Replace input_directory with the path to the directory containing the PDF files you want to process, and output_directory with the path to the directory where you want to save the extracted tables.

Optional Arguments
-p, --processes: Number of parallel processes (default: number of CPU cores)
-r, --regex: Custom regex pattern for searching specific keywords in PDF files (default: '^(?s:(?=.*Revenue)|(?=.*Income))')
For example, to use a custom regex pattern and specify the number of parallel processes, run the script as follows:

```
python script.py -i input_directory -o output_directory -r 'your_custom_pattern' -p 4
```


## License 📄
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing 🤝
Please feel free to open an issue or submit a pull request if you would like to contribute to the project or have any suggestions for improvements.

