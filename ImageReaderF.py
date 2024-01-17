from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, QListWidget, QVBoxLayout, QLineEdit
import ImageReader


class ImageReaderFactory:

    def create_image_reader(path: str) -> ImageReader.ImageReader | None:
        if path.endswith(".fml"):
            return ImageReader.Format1ImageReader(path)
        if path.endswith(".fm2"):
            return ImageReader.Format2ImageReader(path)
        return None
