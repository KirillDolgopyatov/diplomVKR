import pickle
import sys

import PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox

from Designer.loginVKR import Ui_Form
from Designer.designerVKR import Ui_MainWindow


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

        # self.ui.lineTopic.returnPressed.connect(self.topic_save)
        # self.ui.btnSaveTopic.clicked.connect(self.topic_save)
        # self.ui.btnDeleteTopic.clicked.connect(self.btnDeleteTopic)

        self.ui.plus_right.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_1.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_1.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_2.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_2.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_3.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_3.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_4.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_4.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_5.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_5.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_6.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_6.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_7.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_7.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_8.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_8.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_9.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_9.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_10.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_10.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_11.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_11.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_13.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_13.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_14.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_14.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_15.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_15.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_16.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_16.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_17.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_17.clicked.connect(self.add_line_edit_down)

        self.ui.plus_right_18.clicked.connect(self.add_line_edit_right)
        self.ui.plus_down_18.clicked.connect(self.add_line_edit_down)

        self.ui.btnAdd_row.clicked.connect(self.add_row_person)
        self.ui.btnAdd_column.clicked.connect(self.add_column_person)
        self.ui.btnDelete_row.clicked.connect(self.delete_row_person)
        self.ui.btnDelete_column.clicked.connect(self.delete_column_person)

        self.installEventFilter(self)
        self.keyPressEvent = self.key_press_event

        self.table_widget()

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
    def topic_save(self):
        pass

    ####################################################################################################################
    def btnDeleteTopic(self):  # удаление выбранных строк в таблице с личным составом
        pass

    def add_line_edit_right(self):
        name_layout = self.sender().parent().layout()

        row, column = self.get_row_column(name_layout)

        self.remove_previous_widget(row, column, name_layout)

        new_line_edit = self.create_line_edit()
        plus_btn = self.create_button(self.on_plus_btn_right)

        name_layout.addWidget(new_line_edit, row, column)
        name_layout.addWidget(plus_btn, row, column + 1)

    def on_plus_btn_right(self):
        self.add_line_edit_right()

    def add_line_edit_down(self):
        name_layout = self.sender().parent().layout()  # не забудь завтра добавить try except

        row, column = self.get_row_column(name_layout)

        self.remove_previous_widget(row, column, name_layout)

        new_line_edit = self.create_line_edit()
        plus_btn_down = self.create_button(self.on_plus_btn_right)
        plus_btn = self.create_button(self.on_plus_btn_clicked)

        name_layout.addWidget(new_line_edit, row, column)
        name_layout.addWidget(plus_btn_down, row, column + 1)
        name_layout.addWidget(plus_btn, row + 1, column)

    def on_plus_btn_clicked(self):
        self.add_line_edit_down()

    def get_row_column(self, name_layout):
        clicked_widget = self.sender()
        index = name_layout.indexOf(clicked_widget)
        if index != -1:
            row, column, _, _ = name_layout.getItemPosition(index)
            return row, column

    @staticmethod
    def remove_previous_widget(row, column, name_layout):
        try:
            item = name_layout.itemAtPosition(row, column)
            if item:
                widget = item.widget()
                if widget:
                    name_layout.removeWidget(widget)
                    widget.deleteLater()
        except UnboundLocalError:
            pass

    @staticmethod
    def create_line_edit():
        line_edit = PyQt5.QtWidgets.QLineEdit()
        line_edit.setFixedSize(30, 30)
        line_edit.setStyleSheet("background-color: white; color: black; font: 10pt;")
        line_edit.setAlignment(QtCore.Qt.AlignCenter)
        return line_edit

    @staticmethod
    def create_button(callback):
        button = PyQt5.QtWidgets.QPushButton()
        button.setFixedSize(20, 20)
        button.setObjectName("plus_right")
        button.setIcon(QIcon("icons/iconPlus.svg"))
        button.setIconSize(QtCore.QSize(14, 14))
        button.clicked.connect(callback)
        return button

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
    def closeEvent(self, event):
        # Вызывается при закрытии приложения
        self.save_data()
        event.accept()

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
