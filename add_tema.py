import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton, \
    QMessageBox

from Designer.designerTest import Ui_MainWindow  # Импорт класса Ui_MainWindow из другого модуля


########################################################################################################################

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Создание экземпляра класса Ui_MainWindow
        self.ui.setupUi(self)  # Инициализация UI элементов

        self.layout = QVBoxLayout()
        self.ui.widget_2.setLayout(self.layout)  # Установка QVBoxLayout как layout для виджета widget_2

        self.ui.btnSaveTopic.clicked.connect(
            self.create_new_label)  # Подключение функции create_new_label при нажатии на кнопку btnSaveTopic

    def create_new_label(self):  # Создание новой метки и вызов функции new_grid
        if self.ui.lineTopic.text() != "":
            text = self.ui.lineTopic.text()
            label = QLabel(text)
            label.setStyleSheet('color: white; font: 14pt;')
            self.layout.addWidget(label)

            self.new_grid()  # Создание нового grid

            self.ui.lineTopic.clear()
        else:
            QMessageBox.warning(None, "Ошибка", "Введите тему")  # Показ предупреждающего сообщения

    def new_grid(self):  # Создание нового grid layout с элементами
        grid = QGridLayout()
        self.layout.addLayout(grid)

        line_edit = self.create_new_line_edit()
        grid.addWidget(line_edit, 0, 0)

        plus_right = QPushButton()
        plus_right.setFixedSize(20, 20)
        plus_right.setIcon(QIcon("icons/iconPlus.svg"))
        plus_right.setIconSize(QSize(14, 14))

        plus_down = QPushButton()
        plus_down.setFixedSize(20, 20)
        plus_down.setIcon(QIcon("icons/iconPlus.svg"))
        plus_down.setIconSize(QSize(14, 14))

        grid.addWidget(plus_right, 0, 1)
        grid.addWidget(plus_down, 1, 0)

        plus_right.clicked.connect(lambda: self.create_new_btn_right(grid))
        plus_down.clicked.connect(lambda: self.create_new_btn_down(grid))

        self.column_stretch(grid)  # Установка растягиваем колонки и строки

    def create_new_btn_down(self, grid):  # Создание новой строки при нажатии на кнопку вниз
        clicked_widget = self.sender()

        # Получение позиции нажатого виджета в сетке
        for i in range(grid.count()):
            item = grid.itemAt(i)
            if item.widget() == clicked_widget:
                row, column = grid.getItemPosition(i)[:2]
                break
        else:
            return

        line_edit = self.create_new_line_edit()
        plus_right = self.create_new_button(lambda: self.create_new_btn_right(grid))
        plus_down = self.create_new_button(lambda: self.create_new_btn_down(grid))

        grid.addWidget(line_edit, row, column)
        grid.addWidget(plus_down, row + 1, column)
        grid.addWidget(plus_right, row, column + 1)

    def create_new_btn_right(self, grid):  # Создание новой колонки при нажатии на кнопку вправо
        clicked_widget = self.sender()

        # Получение позиции нажатого виджета в сетке
        for i in range(grid.count()):
            item = grid.itemAt(i)
            if item.widget() == clicked_widget:
                row, column = grid.getItemPosition(i)[:2]
                break
        else:
            return

        line_edit = self.create_new_line_edit()
        plus_right = self.create_new_button(lambda: self.create_new_btn_right(grid))

        grid.addWidget(line_edit, row, column)
        grid.addWidget(plus_right, row, column + 1)

        self.column_stretch(grid)

    @staticmethod
    def column_stretch(grid):  # Установка растягиваем колонки и строки сетки
        grid.setColumnStretch(grid.columnCount(), 1)
        grid.setRowStretch(grid.rowCount(), 1)

    @staticmethod
    def create_new_line_edit():  # Создание нового QLineEdit
        line_edit = QLineEdit()
        line_edit.setFixedSize(30, 30)
        line_edit.setStyleSheet("background-color: white; color: black; font: 10pt;")
        line_edit.setAlignment(Qt.AlignCenter)
        return line_edit

    @staticmethod
    def create_new_button(callback):  # Создание новой кнопки
        button = QPushButton()
        button.setFixedSize(20, 20)
        button.setIcon(QIcon("icons/iconPlus.svg"))
        button.setIconSize(QSize(14, 14))
        button.clicked.connect(callback)
        return button


########################################################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
