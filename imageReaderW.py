from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, QListWidget, QVBoxLayout, QLineEdit


class ImageReaderWindow(QWidget):
    def __init__(self):
        super().__init__(self)
        self.__line_edit = QLineEdit()
        self.__button_load = QListWidget()
        self.__text_edit = QTextEdit()

    def __load(self):
        pass
