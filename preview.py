import sys
import os
import fitz
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QPushButton, QFileDialog, QSplitter, QSizePolicy, QScrollArea, QMenu, QAction, QInputDialog, QLineEdit
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt
import PyPDF2

class PDFViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDF Viewer")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout(self)

        # Create a splitter widget to adjust the size of the list and preview sections
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Create a widget for the list section
        list_widget = QWidget()
        splitter.addWidget(list_widget)

        # Create list widget to display PDF files in the chosen directory
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.load_pdf)
        list_layout = QVBoxLayout()
        list_layout.addWidget(self.list_widget)
        list_widget.setLayout(list_layout)

        # Create a widget for the preview section
        preview_widget = QWidget()
        splitter.addWidget(preview_widget)

        # Create a scroll area for the PDF preview
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Allow the widget to resize
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow expansion
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable horizontal scrollbar
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.scroll_area)
        preview_widget.setLayout(preview_layout)

        # Create a label to display the scaled PDF preview
        self.preview_label = QLabel()
        self.scroll_area.setWidget(self.preview_label)

        # Create a button to choose the directory containing PDFs
        self.choose_dir_button = QPushButton("Choose Directory")
        self.choose_dir_button.clicked.connect(self.choose_directory)

        # Create a refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_list)

        # Create a context menu for renaming files
        self.context_menu = QMenu(self)
        self.rename_action = QAction("Rename", self)
        self.rename_action.triggered.connect(self.rename_selected)
        self.context_menu.addAction(self.rename_action)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.choose_dir_button)
        button_layout.addWidget(self.refresh_button)

        # Create a button to combine PDFs
        self.combine_button = QPushButton("Combine PDFs")
        self.combine_button.clicked.connect(self.combine_pdfs)
        button_layout.addWidget(self.combine_button)

        main_layout.addLayout(button_layout)
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

        self.selected_pdf = None  # Store the currently selected PDF path

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose Directory")
        if directory:
            self.load_pdf_files(directory)

    def load_pdf_files(self, directory):
        self.list_widget.clear()
        pdf_files = [file for file in os.listdir(directory) if file.lower().endswith('.pdf')]
        pdf_files.sort()  # Sort the list alphabetically
        self.pdf_files = [os.path.join(directory, file) for file in pdf_files]
        self.list_widget.addItems(pdf_files)

    def load_pdf(self, item):
        self.selected_pdf = self.pdf_files[self.list_widget.currentRow()]
        self.display_pdf(self.selected_pdf)

    def display_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            image_list = []

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pixmap = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
                image = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888)
                image_list.append(image)

            # Combine all pages into a single image
            combined_image = QImage(image_list[0].width(), sum(image.height() for image in image_list), QImage.Format_RGB888)
            painter = QPainter(combined_image)
            y_offset = 0
            for image in image_list:
                painter.drawImage(0, y_offset, image)
                y_offset += image.height()
            painter.end()

            # Scale the image to fit the available width while maintaining aspect ratio with anti-aliasing
            scaled_pixmap = QPixmap.fromImage(combined_image).scaledToWidth(self.scroll_area.width(), Qt.SmoothTransformation)
            self.preview_label.setPixmap(scaled_pixmap)

            doc.close()
        except Exception as e:
            print(f"Error loading PDF: {e}")

    def contextMenuEvent(self, event):
        self.context_menu.exec_(self.mapToGlobal(event.pos()))

    def rename_selected(self):
        selected_index = self.list_widget.currentRow()
        if selected_index != -1:
            selected_pdf = self.pdf_files[selected_index]

            current_name = os.path.basename(selected_pdf)
            new_name, ok = QInputDialog.getText(self, "Rename File", "Enter new file name:", QLineEdit.Normal, current_name)

            if ok and new_name.strip() != "":
                # Ensure the new name doesn't already have a .pdf extension
                if not new_name.endswith(".pdf"):
                    new_name += ".pdf"
                new_pdf_path = os.path.join(os.path.dirname(selected_pdf), new_name)
                os.rename(selected_pdf, new_pdf_path)
                self.load_pdf_files(os.path.dirname(selected_pdf))

    def combine_pdfs(self):
        if self.pdf_files:
            output_pdf, _ = QFileDialog.getSaveFileName(self, "Save Combined PDF", "", "PDF Files (*.pdf)")
            if output_pdf:
                merger = PyPDF2.PdfMerger()
                for pdf_file in self.pdf_files:
                    merger.append(pdf_file)
                with open(output_pdf, "wb") as merged_file:
                    merger.write(merged_file)

    def refresh_list(self):
        # Refresh the list of PDF files in the current directory
        if hasattr(self, 'selected_pdf'):
            current_directory = os.path.dirname(self.selected_pdf)
            self.load_pdf_files(current_directory)

    def resizeEvent(self, event):
        # Resize the scaled PDF preview label when the splitter or main window is resized
        if self.selected_pdf:
            self.display_pdf(self.selected_pdf)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())
