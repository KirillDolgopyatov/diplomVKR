import sqlite3
import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox)

from Designer.des import Ui_MainWindow


########################################################################################################################
########################################################################################################################
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.function_switch_between_stack_widgets()
        self.function_add_table_personnel()

        self.db_connection = sqlite3.connect('personnel.db')
        self.cursor = self.db_connection.cursor()
        self.load_data_from_sqlite()

    ####################################################################################################################

    def save_data_to_sqlite(self):
        conn = sqlite3.connect('your_database_name.db')
        cursor = conn.cursor()

        # Создание таблицы, если ее еще нет
        cursor.execute('''CREATE TABLE IF NOT EXISTS personnel (
                            fio TEXT,
                            rank TEXT,
                            subunit TEXT,
                            duty TEXT
                        )''')

        # Получение данных из таблицы и вставка их в базу данных SQLite
        for i in range(self.ui.table_personnel.rowCount()):
            fio = self.ui.table_personnel.item(i, 0).text()
            rank = self.ui.table_personnel.item(i, 1).text()
            subunit = self.ui.table_personnel.item(i, 2).text()
            duty = self.ui.table_personnel.item(i, 3).text()

            cursor.execute('''INSERT INTO personnel (fio, rank, subunit, duty)
                              VALUES (?, ?, ?, ?)''', (fio, rank, subunit, duty))

        conn.commit()
        conn.close()

    def load_data_from_sqlite(self):
        conn = sqlite3.connect('your_database_name.db')
        cursor = conn.cursor()

        cursor.execute('''SELECT fio, rank, subunit, duty FROM personnel''')
        rows = cursor.fetchall()

        self.ui.table_personnel.setRowCount(0)  # Очистка таблицы перед заполнением
        for row in rows:
            rowCount = self.ui.table_personnel.rowCount()
            self.ui.table_personnel.insertRow(rowCount)
            for i, value in enumerate(row):
                self.ui.table_personnel.setItem(rowCount, i, QTableWidgetItem(str(value)))

        conn.close()

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
        self.ui.table_personnel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

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
    def closeEvent(self, event):
        # Вызывается при закрытии приложения
        self.save_data()  # сохраняем данные с таблиц
        self.save_layout()  # сохраняем данные с виджетов тем
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
