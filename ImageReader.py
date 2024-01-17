import sys
from abc import abstractmethod, ABC

from PyQt5.QtWidgets import (QApplication, QMessageBox, QHBoxLayout, QPushButton,
                             QWidget, QVBoxLayout, QLineEdit, QTextEdit)
from PyQt5.QtCore import Qt, QFile, QTextStream


class ImageReader(ABC):
    def __init__(self, path: str):
        self._qfile: QFile | None = None
        self._text_stream: QTextStream | None = None
        self._path: str = path
        self.__open_file()

    def __open_file(self) -> None:
        self._qfile = QFile(self._path)
        if not self._qfile.open(QFile.ReadOnly | QFile.Text):
            print("File not found.")
            return
        self._text_stream = QTextStream(self._qfile)

    @abstractmethod
    def read_file(self) -> list[str]:
        pass


class Format1ImageReader(ImageReader):

    def read_file(self) -> list[str]:
        data: list[str] = []
        if self._text_stream is None:
            print(f"Error : Unable t oopen file: {self._path}")
            return data
        # read the file
        width: int = int(self._text_stream.readLine())
        height: int = int(self._text_stream.readLine())
        for i in range(height):
            line: str = ""
            for j in range(width):
                line += self._text_stream.readLine()
            data.append(line)
        return data


class Format2ImageReader(ImageReader):

    def read_file(self) -> list[str]:
        data = []
        if self._text_stream is None:
            print(f"Error : Unable t oopen file: {self._path}")
        # read the file
        line: str = ""
        width: int = int(self._text_stream.readLine())
        temp: list[str] = self._text_stream.readLine()
        for i in range(len(temp)):
            if i % width == 0:
                data.append(line)
                line = ""
            line += temp[i]
        data.append(line)
        return data


class ImageReaderFactory:

    @staticmethod
    def create_image_reader(path: str) -> ImageReader | None:
        if path.endswith(".fm1"):
            return Format1ImageReader(path)
        if path.endswith(".fm2"):
            return Format2ImageReader(path)
        return None


# ☺de nouveau fonctionnel c'est genial
class ImageReaderWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Factory test")

        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setPlaceholderText("entre l'image que tu as envie d'afficher")

        self.buttonLoad = QPushButton("load", self)

        self.textEdit = QTextEdit()
        self.textEdit.setMinimumSize(350, 350)
        self.textEdit.setFontFamily("Courrier")

        h_layout.addWidget(self.lineEdit)
        h_layout.addWidget(self.buttonLoad)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.textEdit)
        self.setLayout(v_layout)

        self.buttonLoad.clicked.connect(self.load)

    def load(self):
        image_reader = ImageReaderFactory.create_image_reader(self.__line_edit.text())

        if image_reader is None:
            return

        data = image_reader.read_file()

        self.__text_edit.clear()
        for line in data:
            self.__text_edit.append(line)

        del image_reader


class ImageReaderWindow2(QWidget):
    def __init__(self):
        super().__init__()
        self.init_wind()

    def init_wind(self):
        layout = QVBoxLayout()


        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Enter the file to load")
        layout.addWidget(self.line_edit)

        load_button = QPushButton('Load', self)
        load_button.clicked.connect(self.load)
        layout.addWidget(load_button)

        self.text_edit = QTextEdit(self)
        self.text_edit.setFontFamily("Courier")
        layout.addWidget(self.text_edit)

        self.setLayout(layout)
        self.setWindowTitle('Image Reader')

    def load(self):
        path = self.line_edit.text()
        print(self.line_edit.text())
        print(path)
        try:
            reader = ImageReaderFactory.create_image_reader(path)
            data = reader.read_file()
            self.text_edit.setText('\n'.join(data))
        except ValueError as e:
            self.text_edit.setText(str(e))
        except Exception as e:
            self.text_edit.setText("error " + str(e))


if __name__ == '__main__':
    path = "Image1.fm1"
    reader = ImageReaderFactory.create_image_reader(path)
    print("\n".join(reader.read_file()))
    app = QApplication(sys.argv)
    window = ImageReaderWindow2()
    window.show()
    sys.exit(app.exec_())
