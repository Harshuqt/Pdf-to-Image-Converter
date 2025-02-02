import os
import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, 
    QFileDialog, QLabel, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class PDFConverterThread(QThread):
    """
    Background thread to handle PDF to image conversion
    to prevent UI from freezing during processing
    """
    progress_update = pyqtSignal(int)
    conversion_complete = pyqtSignal(bool)

    def __init__(self, pdf_paths, output_folder):
        super().__init__()
        self.pdf_paths = pdf_paths
        self.output_folder = output_folder

    def run(self):
        """
        Main conversion process run in background thread
        """
        try:
            total_pdfs = len(self.pdf_paths)
            for index, pdf_path in enumerate(self.pdf_paths, 1):
                # Create folder with PDF filename
                pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
                pdf_output_folder = os.path.join(self.output_folder, pdf_filename)
                os.makedirs(pdf_output_folder, exist_ok=True)

                # Open PDF and convert pages to images
                doc = fitz.open(pdf_path)
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    
                    # Render page to an image
                    pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
                    
                    # Save image
                    img_path = os.path.join(
                        pdf_output_folder, 
                        f"{pdf_filename}_page_{page_num + 1}.png"
                    )
                    pix.save(img_path)

                # Update progress
                progress = int((index / total_pdfs) * 100)
                self.progress_update.emit(progress)

            # Signal completion
            self.conversion_complete.emit(True)

        except Exception as e:
            print(f"Conversion error: {e}")
            self.conversion_complete.emit(False)

class PDFToImageConverter(QWidget):
    """
    Main application window for PDF to Image conversion
    """
    def __init__(self):
        super().__init__()
        self.initUI()
        self.pdf_paths = []
        self.output_folder = ""

    def initUI(self):
        """
        Setup the user interface
        """
        self.setWindowTitle('PDF to Image Converter')
        self.setGeometry(300, 300, 500, 300)

        # Main layout
        layout = QVBoxLayout()

        # PDF Selection Section
        pdf_selection_layout = QHBoxLayout()
        self.pdf_label = QLabel('No PDFs selected')
        pdf_select_btn = QPushButton('Select PDFs')
        pdf_select_btn.clicked.connect(self.select_pdfs)
        pdf_selection_layout.addWidget(self.pdf_label)
        pdf_selection_layout.addWidget(pdf_select_btn)
        layout.addLayout(pdf_selection_layout)

        # Output Folder Selection Section
        output_layout = QHBoxLayout()
        self.output_label = QLabel('No output folder selected')
        output_select_btn = QPushButton('Select Output Folder')
        output_select_btn.clicked.connect(self.select_output_folder)
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(output_select_btn)
        layout.addLayout(output_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Convert Button
        convert_btn = QPushButton('Convert PDFs to Images')
        convert_btn.clicked.connect(self.start_conversion)
        layout.addWidget(convert_btn)

        self.setLayout(layout)

    def select_pdfs(self):
        """
        Open file dialog to select multiple PDF files
        """
        file_dialog = QFileDialog()
        self.pdf_paths, _ = file_dialog.getOpenFileNames(
            self, 
            'Select PDF Files', 
            '', 
            'PDF Files (*.pdf)'
        )
        
        if self.pdf_paths:
            self.pdf_label.setText(f'{len(self.pdf_paths)} PDFs selected')
        else:
            self.pdf_label.setText('No PDFs selected')

    def select_output_folder(self):
        """
        Open folder dialog to select output directory
        """
        self.output_folder = QFileDialog.getExistingDirectory(
            self, 
            'Select Output Folder'
        )
        
        if self.output_folder:
            self.output_label.setText(f'Output: {self.output_folder}')
        else:
            self.output_label.setText('No output folder selected')

    def start_conversion(self):
        """
        Validate inputs and start PDF conversion process
        """
        # Validate PDF and output folder selection
        if not self.pdf_paths:
            QMessageBox.warning(self, 'Error', 'Please select PDF files first.')
            return
        
        if not self.output_folder:
            QMessageBox.warning(self, 'Error', 'Please select an output folder.')
            return

        # Reset and prepare progress bar
        self.progress_bar.setValue(0)

        # Create conversion thread
        self.converter_thread = PDFConverterThread(
            self.pdf_paths, 
            self.output_folder
        )
        self.converter_thread.progress_update.connect(self.update_progress)
        self.converter_thread.conversion_complete.connect(self.conversion_finished)
        
        # Start conversion
        self.converter_thread.start()

    def update_progress(self, value):
        """
        Update progress bar during conversion
        """
        self.progress_bar.setValue(value)

    def conversion_finished(self, success):
        """
        Show completion message
        """
        if success:
            QMessageBox.information(
                self, 
                'Conversion Complete', 
                'PDFs have been successfully converted to images!'
            )
        else:
            QMessageBox.warning(
                self, 
                'Conversion Failed', 
                'An error occurred during PDF conversion.'
            )

def main():
    """
    Main entry point of the application
    """
    app = QApplication(sys.argv)
    converter = PDFToImageConverter()
    converter.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# Installation Requirements:
# pip install PyMuPDF PyQt5