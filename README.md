# PDF-to-Image Converter

A desktop application for converting PDFs into images using PyMuPDF and PyQt5.

## Project Description
This tool allows users to convert multiple PDF files into individual image files (PNG format) in a customizable output directory. The application includes features like progress tracking, error handling, and user-friendly interface.

## Features

- **Multiple PDF Selection**: Select multiple PDF files from the file dialog.
- **Output Folder Selection**: Choose a custom directory for saving converted images.
- **Progress Tracking**: Visual progress bar updates during conversion.
- **Page-wise Conversion**: Converts each page of a PDF into an individual image.

## Installation Requirements
To run this application, you'll need to install the following dependencies:

```bash
pip install PyMuPDF PyQt5
```

## Usage

1. **Run the Application**: Execute `pdf2image.py` using Python.
2. **Select PDFs**: Click "Select PDFs" and choose multiple PDF files from your system.
3. **Choose Output Folder**: Click "Select Output Folder" to specify where images will be saved.
4. **Convert PDFs**: Click "Convert PDFs to Images" to start the conversion process.
5. **Wait for Completion**: The progress bar will update as each page is converted.

## Notes
- **Image Format**: Converted images are saved in PNG format.
- **File Naming Convention**: Each image is named as `filename_page_number.png`.
- **Error Handling**: The application includes basic error handling and user feedback.

## License Information  
his project is licensed under the [GNU General Public License v3.0](https://github.com/Harshuqt/Pdf-to-Image-Converter/blob/main/LICENSE). See the LICENSE file in this repository for details.

## GitHub Repository  
The complete project can be found on GitHub at [this link](https://github.com/Harshuqt/Pdf-to-Image-Converter).