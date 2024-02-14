import json
import pickle
import sys

import PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox,
                             QPushButton, QLineEdit, QGridLayout, QLabel, QVBoxLayout, QFrame, QDateTimeEdit,
                             QHBoxLayout)

from Designer.designerVKR import Ui_MainWindow
from Designer.loginVKR import Ui_Form


########################################################################################################################
########################################################################################################################
class Form(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.drag_position = None
        self.ui.btn_close.clicked.connect(self.close)  # закрытие окна авторизации
        self.ui.btn_signin.clicked.connect(self.enter)

    ####################################################################################################################

    def enter(self):
        # login = self.ui.lineEdit_login.text()
        # password = self.ui.lineEdit_password.text()
        # if login == "admin" and password == "12345":
        self.close()
        window.show()
        # else:
        #     QMessageBox.warning(None, "Error", "Проверьте ведённые данные")

    ####################################################################################################################

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = None
            event.accept()


########################################################################################################################
########################################################################################################################
class MainWindow(QMainWindow):
    previous = False

    def __init__(self):
        super().__init__()
        self.animation = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.helpBtn.clicked.connect(self.slideRightSubMenu)
        self.ui.closeCenterMenu_2.clicked.connect(self.slideRightSubMenu)

        self.ui.btnHome.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(0))
        self.ui.btnPerson.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(1))
        self.ui.btnTopic.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(2))
        self.ui.helpBtn.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(3))

        self.ui.lineFIO_22.returnPressed.connect(self.person_save)
        self.ui.lineGroup_22.returnPressed.connect(self.person_save)
        self.ui.lineGpa_22.returnPressed.connect(self.person_save)
        self.ui.btnSavePerson_22.clicked.connect(self.person_save)
        self.ui.btnDeleteFio_22.clicked.connect(self.btn_delete)

        self.installEventFilter(self)
        self.keyPressEvent = self.key_press_event

        self.table_widget()

        self.layout = QVBoxLayout()
        self.ui.widget_2.setLayout(self.layout)

        self.ui.btnSaveTopic.clicked.connect(self.create_new_label)
        self.ui.btnDeleteTopic.clicked.connect(self.remove_last_label_and_grid)

        self.load_layout()

        self.task_counter = 0
        self.ui.btn_new_task.clicked.connect(self.addTask)

    ####################################################################################################################

    def table_widget(self):  # создание таблиц
        # таблица личного состава
        self.ui.tableWidget_2.setRowCount(1)
        self.ui.tableWidget_2.setColumnCount(3)
        self.ui.tableWidget_2.setHorizontalHeaderLabels(('ФИО', '№ группы', 'Средний балл'))
        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        ###########
        ###########
        self.ui.tableWidget_1.setRowCount(1)
        self.ui.tableWidget_1.setColumnCount(1)
        self.ui.tableWidget_1.setColumnWidth(0, 250)
        self.ui.tableWidget_1.setHorizontalHeaderItem(0, QTableWidgetItem("ФИО"))

        ###########
        ###########
        # таблица задач
        self.load_data()
        self.update()

    ####################################################################################################################

    def person_save(self):
        fio = self.ui.lineFIO_22.text()
        group = self.ui.lineGroup_22.text()
        gpa = self.ui.lineGpa_22.text()

        if fio != '' and gpa != '' and group != '':
            rowCount = self.ui.tableWidget_2.rowCount()
            self.ui.tableWidget_2.insertRow(rowCount)
            self.ui.tableWidget_2.setItem(rowCount, 0, QTableWidgetItem(fio))
            self.ui.tableWidget_2.setItem(rowCount, 1, QTableWidgetItem(group))
            self.ui.tableWidget_2.setItem(rowCount, 2, QTableWidgetItem(gpa))

            self.ui.lineGroup_22.clear()
            self.ui.lineGpa_22.clear()
            self.ui.lineFIO_22.clear()
        else:
            QMessageBox.warning(None, "Ошибка", "Заполните все поля")

    ####################################################################################################################
    def btn_delete(self):  # удаление выбранных строк в таблице с личным составом
        selected_ranges = self.ui.tableWidget_2.selectedRanges()
        if len(selected_ranges) > 0:
            for selected_range in selected_ranges:
                top_row = selected_range.topRow()
                bottom_row = selected_range.bottomRow()

                for row in range(bottom_row, top_row - 1, -1):
                    self.ui.tableWidget_2.removeRow(row)
        else:
            last_row = self.ui.tableWidget_2.rowCount() - 1
            if last_row >= 0:  # Удалить только если есть строки в таблице
                self.ui.tableWidget_2.removeRow(last_row)
            else:
                QMessageBox.warning(None, "Ошибка", "Таблица пустая")

    ####################################################################################################################

    def key_press_event(self, event):  # удаление строк с помощью клавиши DELETE
        if event.key() == Qt.Key_Delete:
            current_widget_index = self.ui.MainStack.currentIndex()
            if current_widget_index == 1:
                self.btn_delete()
            elif current_widget_index == 2:
                self.btnDeleteTopic()

    ####################################################################################################################
    def save_data(self):  # Сохранение данных в pickle
        # Сохранение данных в файл
        data = []
        for i in range(self.ui.tableWidget_2.rowCount()):
            row = []
            for j in range(self.ui.tableWidget_2.columnCount()):
                item = self.ui.tableWidget_2.item(i, j)
                if item is not None:
                    row.append(item.text())
                else:
                    row.append('')
            data.append(row)
        with open('saveData/data1.pickle', 'wb') as file1:
            pickle.dump(data, file1)

            # Сохранение данных в файл основная таблица
            data = []
            for i in range(self.ui.tableWidget_1.rowCount()):
                row = []
                for j in range(self.ui.tableWidget_1.columnCount()):
                    item = self.ui.tableWidget_1.item(i, j)
                    if item is not None:
                        row.append(item.text())
                    else:
                        row.append('')
                data.append(row)
            with open('saveData/data3.pickle', 'wb') as file3:
                pickle.dump(data, file3)

    ####################################################################################################################
    def load_data(self):  # открываем сохраненный файл pickle
        try:
            # Попытка загрузить данные из файла 1
            with open('saveData/data1.pickle', 'rb') as file1:
                data = pickle.load(file1)

                # Установка количества строк и столбцов
                if len(data) > 0:
                    self.ui.tableWidget_2.setRowCount(len(data))
                    self.ui.tableWidget_2.setColumnCount(len(data[0]))

                    # Заполнение ячеек данными
                    for i, row in enumerate(data):
                        for j, val in enumerate(row):
                            item = QTableWidgetItem(val)
                            self.ui.tableWidget_2.setItem(i, j, item)
        except FileNotFoundError:
            # Если файл не найден, создаем пустую таблицу
            self.ui.tableWidget_2.setRowCount(1)
            self.ui.tableWidget_2.setColumnCount(3)

        try:
            # Попытка загрузить данные из файла 1
            with open('saveData/data3.pickle', 'rb') as file3:
                data = pickle.load(file3)

                # Установка количества строк и столбцов
                if len(data) > 0:
                    self.ui.tableWidget_1.setRowCount(len(data))
                    self.ui.tableWidget_1.setColumnCount(len(data[0]))

                    # Заполнение ячеек данными
                    for i, row in enumerate(data):
                        for j, val in enumerate(row):
                            item = QTableWidgetItem(val)
                            self.ui.tableWidget_1.setItem(i, j, item)
        except FileNotFoundError:
            # Если файл не найден, создаем пустую таблицу
            self.ui.tableWidget_1.setRowCount(1)
            self.ui.tableWidget_1.setColumnCount(1)

    ####################################################################################################################
    def update(self):
        rowCount = self.ui.tableWidget_2.rowCount()
        for row in range(rowCount):
            combobox = PyQt5.QtWidgets.QComboBox()
            combobox.addItem("")
            combobox.setCurrentIndex(-1)
            combobox.setStyleSheet("QComboBox { background-color: rgb(217, 217, 217); color: black; }"
                                   "QComboBox QAbstractItemView {background-color: rgb(255, 255, 255); color: black; }")

            for i in range(rowCount):
                item = self.ui.tableWidget_2.item(i, 0)
                if item is not None:
                    combobox.addItem(item.text())

            self.ui.tableWidget_1.setCellWidget(row, 0, combobox)

    ####################################################################################################################
    def add_column_person(self):
        rowCount = self.ui.tableWidget_1.rowCount()
        self.ui.tableWidget_1.insertRow(rowCount)

    ####################################################################################################################
    def add_row_person(self):
        columnCount = self.ui.tableWidget_1.columnCount()
        self.ui.tableWidget_1.insertColumn(columnCount)
        self.ui.tableWidget_1.setColumnWidth(0, 250)
        self.ui.tableWidget_1.setHorizontalHeaderItem(0, QTableWidgetItem("ФИО"))
        for columnIndex in range(1, columnCount + 1):
            self.ui.tableWidget_1.setHorizontalHeaderItem(columnIndex, QTableWidgetItem(str(columnIndex)))

    ####################################################################################################################
    def delete_row_person(self):
        selected_ranges = self.ui.tableWidget_1.selectedRanges()
        if len(selected_ranges) > 0:
            for selected_range in selected_ranges:
                left_column = selected_range.leftColumn()
                right_column = selected_range.rightColumn()

                for column in range(right_column, left_column - 1, -1):
                    self.ui.tableWidget_1.removeColumn(column)
        else:
            last_column = self.ui.tableWidget_1.columnCount() - 1
            if last_column >= 0:  # Удалить только если есть столбцы в таблице
                self.ui.tableWidget_1.removeColumn(last_column)
            else:
                QMessageBox.warning(None, "Ошибка", "Таблица пустая")

    ####################################################################################################################
    def delete_column_person(self):
        selected_ranges = self.ui.tableWidget_1.selectedRanges()
        if len(selected_ranges) > 0:
            for selected_range in selected_ranges:
                top_row = selected_range.topRow()
                bottom_row = selected_range.bottomRow()

                for row in range(bottom_row, top_row - 1, -1):
                    self.ui.tableWidget_1.removeRow(row)
        else:
            last_row = self.ui.tableWidget_1.rowCount() - 1
            if last_row >= 0:  # Удалить только если есть строки в таблице
                self.ui.tableWidget_1.removeRow(last_row)
            else:
                QMessageBox.warning(None, "Ошибка", "Таблица пустая")

    ####################################################################################################################
    def save_layout(self):  # создаем виджеты для темы
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
                        widget_info = {'type': 'QPushButton', 'direction': grid_widget.objectName()}
                        grid_info[pos_key] = widget_info  # Используем уникальный ключ для сохранения виджета
                widgets_dict[f"grid_{i}"] = grid_info

        with open('saveData/layout_state.json', 'w') as f:
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

    def load_layout(self):  # загружаем виджеты с таблицы
        try:
            with open('saveData/layout_state.json', 'r') as f:
                widgets_dict = json.load(f)
                for widget_name, properties in widgets_dict.items():
                    if 'label' in widget_name:
                        label = QLabel()
                        label.setText(properties.get('text', ''))
                        label.setStyleSheet('color: white; font: 14pt;')
                        self.layout.addWidget(label)
                    elif 'grid' in widget_name:
                        grid = QGridLayout()
                        self.layout.addLayout(grid)
                        for pos_key, widget_info in properties.items():
                            row, col = map(int, pos_key.split('_'))
                            if widget_info['type'] == 'QLineEdit':
                                line_edit = QLineEdit()
                                line_edit.setText(widget_info.get('text', ''))
                                line_edit.setFixedSize(25, 25)
                                line_edit.setStyleSheet("background-color: white; color: black; font: 8pt;")
                                line_edit.setAlignment(Qt.AlignCenter)
                                grid.addWidget(line_edit, row, col)
                                grid.setSpacing(2)
                            elif widget_info['type'] == 'QPushButton':
                                # Создаем кнопку с привязанной функцией, которая добавляет элемент в ее собственный grid
                                button = QPushButton()
                                button.setFixedSize(20, 20)
                                button.setIcon(QIcon("icons/iconPlus.svg"))
                                button.setIconSize(QSize(14, 14))
                                # Важно: используем замыкание для сохранения контекста grid, row, col
                                direction = widget_info.get('direction')
                                if direction == 'right':
                                    button.clicked.connect(
                                        lambda checked, g=grid, r=row, c=col: self.add_new_element(g, r, c, 'right'))
                                    grid.addWidget(button, row, col)
                                else:
                                    button.clicked.connect(
                                        lambda checked, g=grid, r=row, c=col: self.add_new_element(g, r, c, 'down'))
                                    grid.addWidget(button, row, col)

                                self.column_stretch(grid)
        except FileNotFoundError:
            pass

    def new_grid(self):  # создаем виджеты для тем
        grid = QGridLayout()
        self.layout.addLayout(grid)

        line_edit = self.create_new_line_edit()
        grid.addWidget(line_edit, 0, 0)
        grid.setSpacing(2)

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
            # Добавляем кнопку plus_right справа от нового элемента
            plus_right = self.create_new_button(lambda: self.add_new_element(grid, row, column + 1, 'right'))
            plus_right.setObjectName('right')
            grid.addWidget(plus_right, row, column + 1)

            self.column_stretch(grid)

        elif direction == 'down':
            # Добавляем кнопку plus_down ниже нового элемента и plus_right справа от исходного элемента
            plus_down = self.create_new_button(lambda: self.add_new_element(grid, row + 1, column, 'down'))
            plus_down.setObjectName('down')
            grid.addWidget(plus_down, row + 1, column)
            # Возможно, вам также нужно добавить plus_right снова, если это необходимо по логике вашего интерфейса
            plus_right = self.create_new_button(lambda: self.add_new_element(grid, row, column + 1, 'right'))
            plus_right.setObjectName('right')
            grid.addWidget(plus_right, row, column + 1)

            self.column_stretch(grid)

    @staticmethod
    def column_stretch(grid):
        grid.setColumnStretch(grid.columnCount(), 1)
        grid.setRowStretch(grid.rowCount(), 1)

    @staticmethod
    def create_new_line_edit():
        line_edit = QLineEdit()
        line_edit.setFixedSize(25, 25)
        line_edit.setStyleSheet("background-color: white; color: black; font: 8pt;")
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

    def remove_last_label_and_grid(self):
        # Предполагаем, что self.layout - это QVBoxLayout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                self.layout.removeWidget(widget)
                widget.deleteLater()
                break  # Прерываем цикл после удаления первого найденного QLabel

        for i in reversed(range(self.layout.count())):
            layout_item = self.layout.itemAt(i)
            if isinstance(layout_item.layout(), QGridLayout):
                grid = layout_item.layout()
                # Удаление всех виджетов из QGridLayout
                while grid.count():
                    item = grid.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                self.layout.removeItem(grid)  # Удаление самого QGridLayout из QVBoxLayout
                break  # Прерываем цикл после удаления первого найденного QGridLayout

    ####################################################################################################################

    def addTask(self):
        if self.ui.le_write_task.text() != '':
            task_text = self.ui.le_write_task.text()
            new_frame = QFrame(self.ui.frame_12)
            new_frame.setFrameShape(QFrame.StyledPanel)
            new_frame.setFrameShadow(QFrame.Raised)
            new_frame.setStyleSheet("background-color: rgb(45, 45, 45);")
            new_frame.setFixedHeight(50)
            frame_layout = QHBoxLayout(new_frame)

            task_label = QLabel(task_text, new_frame)
            task_label.setStyleSheet("color: white")

            task_but = QPushButton(new_frame)
            task_but.setFixedSize(25, 25)
            task_but.setStyleSheet("background-color: white")
            task_but.setIcon(QIcon("icons/ready.png."))

            task_but.setIconSize(QSize(24, 24))
            task_but.setStyleSheet('border-radius: 12px; background-color: white}')

            task_line_edit = QLineEdit(new_frame)
            task_line_edit.setStyleSheet("")

            # Создаем QDateTimeEdit и QLabel для отображения оставшегося времени
            datetime_edit = QDateTimeEdit(new_frame)
            datetime_edit.setCalendarPopup(True)
            datetime_edit.setStyleSheet("background-color: white")
            datetime_edit.setDateTime(QDateTime.currentDateTime())

            time_left_label = QLabel("Оставшееся время: ", new_frame)
            time_left_label.setStyleSheet('color:white; font: 8pt;')

            # Подключаем сигнал dateTimeChanged к слоту для обновления QLabel
            datetime_edit.dateTimeChanged.connect(lambda: self.update_time_left(datetime_edit, time_left_label))

            frame_layout.addWidget(task_but)
            frame_layout.addWidget(task_label)
            frame_layout.addWidget(task_line_edit)
            frame_layout.addWidget(datetime_edit)
            frame_layout.addWidget(time_left_label)

            self.ui.frame_12.layout().addWidget(new_frame)
            self.ui.le_write_task.clear()

            # Вызываем update_time_left вручную, чтобы инициализировать отображение оставшегося времени
            self.update_time_left(datetime_edit, time_left_label)

    @staticmethod
    def update_time_left(datetime_edit, time_left_label):
        current_time = QDateTime.currentDateTime()
        selected_time = datetime_edit.dateTime()
        time_diff = current_time.secsTo(selected_time)
        days_left = time_diff // (60 * 60 * 24)
        hours_left = (time_diff % (60 * 60 * 24)) // (60 * 60)
        minutes_left = (time_diff % (60 * 60)) // 60
        time_left_label.setText(f"Срок выполнения: {days_left} д. {hours_left} ч. {minutes_left} м")

    ####################################################################################################################
    def closeEvent(self, event):
        # Вызывается при закрытии приложения
        self.save_data()  # сохраняем данные с таблиц
        self.save_layout()  # сохраняем данные с виджетов тем
        event.accept()

    ####################################################################################################################
    def slideRightSubMenu(self):  # открывает левое меню для кнопки задачи дизайн
        width2 = self.ui.leftSubMenu.width()

        if width2 == 0:
            newWidth2 = 150
        else:
            newWidth2 = 0

        self.animation = QPropertyAnimation(self.ui.leftSubMenu, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width2)
        self.animation.setEndValue(newWidth2)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InQuart)
        self.animation.start()

    def slideRightMenu(self):  # открывает левое меню дизайн
        width = self.ui.leftMenu.width()

        if width == 35:
            newWidth = 145
        else:
            newWidth = 35

        self.animation = QPropertyAnimation(self.ui.leftMenu, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InQuart)
        self.animation.start()

    ####################################################################################################################


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    window = MainWindow()
    form.show()
    sys.exit(app.exec_())
