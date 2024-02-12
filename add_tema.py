import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton, \
    QMessageBox

from Designer.designerTest import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.layout = QVBoxLayout()
        self.ui.widget_2.setLayout(self.layout)
        self.ui.btnSaveTopic.clicked.connect(self.create_new_label)

    def explore_layout(self):
        grid_layout = []
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item.widget():
                print(f"Widget: {item.widget().__class__.__name__}")
            elif item.layout():
                print(f"Layout: {item.layout().__class__.__name__}")
                for j in range(item.layout().count()):
                    widgets = item.layout().itemAt(j)
                    grid_layout.append(widgets)
                    print(f"LineEdit: {widgets.widget().__class__.__name__}")
        print(grid_layout)

    def create_new_label(self):
        if self.ui.lineTopic.text() != "":
            text = self.ui.lineTopic.text()
            label = QLabel(text)
            label.setStyleSheet('color: white; font: 14pt;')
            self.layout.addWidget(label)

            self.new_grid()
            self.ui.lineTopic.clear()
        else:
            QMessageBox.warning(None, "Ошибка", "Введите тему")

    def new_grid(self):
        grid = QGridLayout()
        self.layout.addLayout(grid)

        line_edit = self.create_new_line_edit()
        grid.addWidget(line_edit, 0, 0)

        self.add_buttons_to_grid(grid, 0, 0)
        self.explore_layout()

    def add_buttons_to_grid(self, grid, row, column):
        plus_right = self.create_new_button(lambda: self.add_new_element(grid, row, column + 1, 'right'))
        plus_down = self.create_new_button(lambda: self.add_new_element(grid, row + 1, column, 'down'))

        grid.addWidget(plus_right, row, column + 1)
        grid.addWidget(plus_down, row + 1, column)

        self.column_stretch(grid)

    def add_new_element(self, grid, row, column, direction):
        line_edit = self.create_new_line_edit()
        grid.addWidget(line_edit, row, column)

        if direction == 'right':
            self.add_buttons_to_grid(grid, row, column)
        else:
            self.add_buttons_to_grid(grid, row, column)

        self.column_stretch(grid)

    def closeEvent(self, event):
        # self.save_state()
        event.accept()  # Подтверждаем закрытие приложения

    @staticmethod
    def column_stretch(grid):
        grid.setColumnStretch(grid.columnCount(), 1)
        grid.setRowStretch(grid.rowCount(), 1)

    @staticmethod
    def create_new_line_edit():
        line_edit = QLineEdit()
        line_edit.setFixedSize(30, 30)
        line_edit.setStyleSheet("background-color: white; color: black; font: 10pt;")
        line_edit.setAlignment(Qt.AlignCenter)
        return line_edit

    @staticmethod
    def create_new_button(callback):
        button = QPushButton()
        button.setFixedSize(20, 20)
        button.setIcon(QIcon("icons/iconPlus.svg"))
        button.setIconSize(QSize(14, 14))
        button.clicked.connect(callback)
        return button


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
