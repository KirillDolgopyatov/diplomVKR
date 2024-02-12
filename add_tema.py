import json
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

        self.load_layout()

    def explore_layout(self):
        widgets_dict = {}  # Пересоздаем словарь для очистки предыдущих данных

        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item.widget():
                widget = item.widget()
                if isinstance(widget, QLabel):
                    # Сохраняем данные QLabel
                    widgets_dict[f"label_{i}"] = {'type': 'QLabel', 'text': widget.text()}
            elif item.layout():
                layout = item.layout()
                grid_info = {}
                for j in range(layout.count()):
                    grid_widget = layout.itemAt(j).widget()
                    position = layout.getItemPosition(j)  # Получаем позицию виджета
                    pos_key = f"{position[0]}_{position[1]}"  # Создаем уникальный ключ из позиции
                    if isinstance(grid_widget, QLineEdit):
                        widget_info = {'type': 'QLineEdit', 'text': grid_widget.text()}
                        grid_info[pos_key] = widget_info  # Используем уникальный ключ для сохранения виджета
                    elif isinstance(grid_widget, QPushButton):
                        widget_info = {'type': 'QPushButton'}
                        grid_info[pos_key] = widget_info  # Используем уникальный ключ для сохранения виджета
                widgets_dict[f"grid_{i}"] = grid_info

        with open('layout_state.json', 'w') as f:
            json.dump(widgets_dict, f, indent=4)

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

    def load_layout(self):
        try:
            with open('layout_state.json', 'r') as f:
                widgets_dict = json.load(f)
                for properties in widgets_dict.items():
                    if properties['type'] == 'QLabel':
                        label = QLabel()
                        label.setText(properties.get('text', ''))
                        label.setStyleSheet('color: white; font: 14pt;')
                        self.layout.addWidget(label)
                    elif properties['type'] == 'QGridLayout':
                        grid = QGridLayout()
                        self.layout.addLayout(grid)
                        for pos_key, widget_info in properties.items():
                            if widget_info['type'] == 'QLineEdit':
                                line_edit = QLineEdit()
                                line_edit.setText(widget_info.get('text', ''))
                                line_edit.setFixedSize(30, 30)
                                line_edit.setStyleSheet("background-color: white; color: black; font: 10pt;")
                                line_edit.setAlignment(Qt.AlignCenter)
                                # Распаковываем позицию виджета из ключа
                                row, col = map(int, pos_key.split('_'))
                                grid.addWidget(line_edit, row, col)

                            elif widget_info['type'] == 'QPushButton':
                                button = QPushButton()
                                button.setFixedSize(20, 20)
                                button.setIcon(QIcon("icons/iconPlus.svg"))
                                button.setIconSize(QSize(14, 14))
                                # Распаковываем позицию виджета из ключа
                                row, col = map(int, pos_key.split('_'))
                                grid.addWidget(button, row, col)
        except FileNotFoundError:
            pass

    def new_grid(self):
        grid = QGridLayout()
        self.layout.addLayout(grid)

        line_edit = self.create_new_line_edit()
        grid.addWidget(line_edit, 0, 0)

        self.add_buttons_to_grid(grid, 0, 0)

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
        self.explore_layout()
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
