import pickle
import sys

import PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QDateTime, QTimer
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox,
                             QPushButton, QLineEdit, QLabel, QVBoxLayout, QFrame, QHBoxLayout)

from Designer.des import Ui_MainWindow
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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #####
        self.animation = None
        self.installEventFilter(self)
        self.keyPressEvent = self.key_press_event
        self.ui.helpBtn.clicked.connect(self.slideRightSubMenu)
        self.ui.closeCenterMenu_2.clicked.connect(self.slideRightSubMenu)
        #####
        self.function_switch_between_stack_widgets()
        self.function_add_table_personnel()

        #####
        self.task_counter = 0
        self.task_time_labels = []
        self.ui.btn_new_task.clicked.connect(self.addTask)
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_all_time)
        self.update_timer.start(1000)
        self.ui.dateTimeEdit.setCalendarPopup(True)
        self.ui.dateTimeEdit.setDateTime(PyQt5.QtCore.QDateTime.currentDateTime())
        self.ui.scrollAreaWC.setLayout(QVBoxLayout())
        #####

    ####################################################################################################################
    def function_switch_between_stack_widgets(self):
        self.ui.btnHome.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(0))
        self.ui.btnPerson.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(1))
        self.ui.btnTopic.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(2))
        self.ui.helpBtn.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(3))

    def function_add_table_personnel(self):
        self.ui.le_fio.returnPressed.connect(self.save_personnel)
        self.ui.le_zvanie.returnPressed.connect(self.save_personnel)
        self.ui.le_subunit.returnPressed.connect(self.save_personnel)
        self.ui.le_duty.returnPressed.connect(self.save_personnel)

        self.ui.btn_save_personnel.clicked.connect(self.save_personnel)
        self.ui.btn_delete_personnel.clicked.connect(self.delete_personnel)

        self.table_widget()

    def table_widget(self):  # создание таблиц
        # таблица личного состава
        self.ui.table_personnel.setRowCount(1)
        self.ui.table_personnel.setColumnCount(4)
        self.ui.table_personnel.setHorizontalHeaderLabels(['ФИО', 'В/зв', 'Подразделение', 'Должность'])

        ###########
        ###########

        ###########
        ###########
        # таблица задач
        self.load_data()

    ####################################################################################################################

    def save_personnel(self):
        fio = self.ui.le_fio.text()
        rank = self.ui.le_zvanie.text()
        subunit = self.ui.le_subunit.text()
        duty = self.ui.le_duty.text()

        if fio != '' and rank != '' and subunit != '' and duty != '':
            rowCount = self.ui.table_personnel.rowCount()
            self.ui.table_personnel.insertRow(rowCount)
            self.ui.table_personnel.setItem(rowCount, 0, QTableWidgetItem(fio))
            self.ui.table_personnel.setItem(rowCount, 1, QTableWidgetItem(rank))
            self.ui.table_personnel.setItem(rowCount, 2, QTableWidgetItem(subunit))
            self.ui.table_personnel.setItem(rowCount, 3, QTableWidgetItem(duty))

            self.ui.le_fio.clear()
            self.ui.le_zvanie.clear()
            self.ui.le_subunit.clear()
            self.ui.le_duty.clear()

        else:
            QMessageBox.warning(None, "Ошибка", "Заполните все поля")

    ####################################################################################################################
    def delete_personnel(self):  # удаление выбранных строк в таблице с личным составом
        selected_ranges = self.ui.table_personnel.selectedRanges()
        if len(selected_ranges) > 0:
            for selected_range in selected_ranges:
                top_row = selected_range.topRow()
                bottom_row = selected_range.bottomRow()

                for row in range(bottom_row, top_row - 1, -1):
                    self.ui.table_personnel.removeRow(row)
        else:
            last_row = self.ui.table_personnel.rowCount() - 1
            if last_row >= 0:  # Удалить только если есть строки в таблице
                self.ui.table_personnel.removeRow(last_row)
            else:
                QMessageBox.warning(None, "Ошибка", "Таблица пустая")

    ####################################################################################################################
    def save_data(self):  # Сохранение данных в pickle
        # Сохранение данных в файл
        data = []
        for i in range(self.ui.table_personnel.rowCount()):
            row = []
            for j in range(self.ui.table_personnel.columnCount()):
                item = self.ui.table_personnel.item(i, j)
                if item is not None:
                    row.append(item.text())
                else:
                    row.append('')
            data.append(row)
        with open('saveData/data1.pickle', 'wb') as file1:
            pickle.dump(data, file1)

    ####################################################################################################################
    def load_data(self):  # открываем сохраненный файл pickle
        try:
            # Попытка загрузить данные из файла 1
            with open('saveData/data1.pickle', 'rb') as file1:
                data = pickle.load(file1)

                # Установка количества строк и столбцов
                if len(data) > 0:
                    self.ui.table_personnel.setRowCount(len(data))
                    self.ui.table_personnel.setColumnCount(len(data[0]))

                    # Заполнение ячеек данными
                    for i, row in enumerate(data):
                        for j, val in enumerate(row):
                            item = QTableWidgetItem(val)
                            self.ui.table_personnel.setItem(i, j, item)
        except FileNotFoundError:
            # Если файл не найден, создаем пустую таблицу
            self.ui.table_personnel.setRowCount(1)
            self.ui.table_personnel.setColumnCount(3)

    ####################################################################################################################

    def addTask(self):
        if self.ui.le_write_task.text() != '':
            task_text = self.ui.le_write_task.text()
            datetime_edit = self.ui.dateTimeEdit.dateTime()
            new_frame = QFrame(self.ui.scrollAreaWC)  # Изменено на scrollAreaWC
            new_frame.setFrameShape(QFrame.StyledPanel)
            new_frame.setFrameShadow(QFrame.Raised)
            new_frame.setStyleSheet("background-color: rgb(45, 45, 45);")
            new_frame.setFixedHeight(50)

            frame_layout = QHBoxLayout(new_frame)

            task_label = QLabel(task_text, new_frame)
            task_label.setStyleSheet("color: white; font: 12pt;")

            task_but = QPushButton(new_frame)
            task_but.setFixedSize(25, 25)
            task_but.setIconSize(QSize(20, 20))
            task_but.setStyleSheet("""
                   QPushButton {
                       border-radius: 12px;
                       border: 2px solid white;
                   }
                   QPushButton:hover {
                       icon: url('icons/galka.png');
                       icon-size: 20px;
                   }
                   QPushButton:pressed {
                       icon: url('icons/galka.png');
                       border: 2px solid grey;

                   }
               """)

            task_line_edit = QLineEdit(new_frame)
            task_line_edit.setStyleSheet("color: yellow; font: 10 pt;")

            time_left_label = QLabel("", new_frame)
            time_left_label.setStyleSheet('color:white; font: 8pt;')

            frame_layout.addWidget(task_but)
            frame_layout.addWidget(task_label)
            frame_layout.addWidget(task_line_edit)
            frame_layout.addWidget(time_left_label)

            # Измените следующую строку, чтобы добавить new_frame в layout, который принадлежит scrollAreaWC
            self.ui.scrollAreaWC.layout().insertWidget(0, new_frame)
            self.ui.le_write_task.clear()

            self.task_time_labels.append((datetime_edit, time_left_label))

    def update_all_time(self):
        current_time = QDateTime.currentDateTime()
        for datetime_edit, time_left_label in self.task_time_labels:
            time_diff = current_time.secsTo(datetime_edit)
            is_overdue = time_diff < 0
            abs_time_diff = abs(time_diff)
            days_left = abs_time_diff // (60 * 60 * 24)
            hours_left = (abs_time_diff % (60 * 60 * 24)) // (60 * 60)
            minutes_left = (abs_time_diff % (60 * 60)) // 60

            if is_overdue:
                time_left_label.setStyleSheet('color: red')

                time_left_str = f"Просрочено: {days_left} д. {hours_left} ч. {minutes_left} м."
            else:
                time_left_label.setStyleSheet('color: green')
                time_left_str = f"Срок выполнения: {days_left} д. {hours_left} ч. {minutes_left} м."

            time_left_label.setText(time_left_str)

    ####################################################################################################################
    def closeEvent(self, event):
        # Вызывается при закрытии приложения
        self.save_data()  # сохраняем данные с таблиц
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

    def key_press_event(self, event):  # удаление строк с помощью клавиши DELETE
        if event.key() == Qt.Key_Delete:
            current_widget_index = self.ui.MainStack.currentIndex()
            if current_widget_index == 1:
                self.btn_delete()
            elif current_widget_index == 2:
                self.btnDeleteTopic()

    ####################################################################################################################


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    window = MainWindow()
    form.show()
    sys.exit(app.exec_())
