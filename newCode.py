import sqlite3  # Импорт модуля для работы с SQLite
import sys  # Импорт системного модуля

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, \
    QMessageBox, QCompleter  # Импорт необходимых классов из PyQt5

from Designer.des import Ui_MainWindow  # Импорт дизайна интерфейса, созданного в Qt Designer


class MainWindow(QMainWindow):  # Определение класса MainWindow, наследующего QMainWindow
    def __init__(self):
        super().__init__()  # Вызов конструктора базового класса
        self.ui = Ui_MainWindow()  # Создание экземпляра дизайна интерфейса
        self.ui.setupUi(self)  # Настройка интерфейса в текущем окне

        self.function_switch_between_stack_widgets()  # Инициализация переключения между виджетами
        self.function_add_table_personnel()  # Инициализация функционала таблицы персонала

        self.db_connection = sqlite3.connect('personnel.db')  # Подключение к базе данных SQLite
        self.cursor = self.db_connection.cursor()  # Создание курсора для работы с базой данных
        self.load_data_from_sqlite()  # Загрузка данных из базы данных при запуске приложения

        self.ui.table_personnel.itemChanged.connect(
            self.save_data_to_sqlite)  # Подключение сигнала изменения элемента таблицы к методу сохранения данных

    def setupCompleterForFio(self):
        # Получение всех уникальных значений из первого столбца таблицы
        list_fio = set()
        for i in range(self.ui.table_personnel.rowCount()):
            cell_item = self.ui.table_personnel.item(i, 0)
            if cell_item is not None:
                list_fio.add(cell_item.text())

        # Создание QCompleter с этими значениями
        completer_fio = QCompleter(list(list_fio))

        list_rank = set()
        for i in range(self.ui.table_personnel.rowCount()):
            cell_item = self.ui.table_personnel.item(i, 1)
            if cell_item is not None:
                list_rank.add(cell_item.text())

        # Создание QCompleter с этими значениями
        completer_rank = QCompleter(list(list_rank))

        list_subunit = set()
        for i in range(self.ui.table_personnel.rowCount()):
            cell_item = self.ui.table_personnel.item(i, 2)
            if cell_item is not None:
                list_subunit.add(cell_item.text())

        # Создание QCompleter с этими значениями
        completer_subunit = QCompleter(list(list_subunit))

        list_duty = set()
        for i in range(self.ui.table_personnel.rowCount()):
            cell_item = self.ui.table_personnel.item(i, 3)
            if cell_item is not None:
                list_duty.add(cell_item.text())

        # Создание QCompleter с этими значениями
        completer_duty = QCompleter(list(list_duty))

        self.ui.le_fio.setCompleter(completer_fio)
        self.ui.le_zvanie.setCompleter(completer_rank)
        self.ui.le_subunit.setCompleter(completer_subunit)
        self.ui.le_duty.setCompleter(completer_duty)

    def save_data_to_sqlite(self):
        # Метод для сохранения данных из таблицы в базу данных SQLite
        conn = sqlite3.connect('personnel.db')  # Подключение к базе данных
        cursor = conn.cursor()  # Создание курсора

        # Создание таблицы, если она не существует
        cursor.execute('''CREATE TABLE IF NOT EXISTS personnel (
                            fio TEXT,
                            rank TEXT,
                            subunit TEXT,
                            duty TEXT
                        )''')

        cursor.execute('DELETE FROM personnel')  # Очистка таблицы перед вставкой новых данных

        # Вставка данных из таблицы интерфейса в базу данных
        for i in range(self.ui.table_personnel.rowCount()):
            fio = self.ui.table_personnel.item(i, 0).text() if self.ui.table_personnel.item(i, 0) else ''
            rank = self.ui.table_personnel.item(i, 1).text() if self.ui.table_personnel.item(i, 1) else ''
            subunit = self.ui.table_personnel.item(i, 2).text() if self.ui.table_personnel.item(i, 2) else ''
            duty = self.ui.table_personnel.item(i, 3).text() if self.ui.table_personnel.item(i, 3) else ''

            cursor.execute('''INSERT INTO personnel (fio, rank, subunit, duty)
                              VALUES (?, ?, ?, ?)''', (fio, rank, subunit, duty))

        conn.commit()  # Подтверждение изменений в базе данных
        conn.close()  # Закрытие соединения с базой данных

        self.setupCompleterForFio()

    def load_data_from_sqlite(self):
        # Метод для загрузки данных из базы данных SQLite в таблицу интерфейса
        conn = sqlite3.connect('personnel.db')  # Подключение к базе данных
        cursor = conn.cursor()  # Создание курсора

        # Создание таблицы, если она не существует
        cursor.execute('''CREATE TABLE IF NOT EXISTS personnel (
                            fio TEXT,
                            rank TEXT,
                            subunit TEXT,
                            duty TEXT
                        )''')

        cursor.execute('''SELECT fio, rank, subunit, duty FROM personnel''')  # Выборка данных из таблицы
        rows = cursor.fetchall()  # Получение всех строк

        self.ui.table_personnel.setRowCount(0)  # Очистка таблицы в интерфейсе перед заполнением
        for row in rows:
            rowCount = self.ui.table_personnel.rowCount()
            self.ui.table_personnel.insertRow(rowCount)
            for i, value in enumerate(row):
                self.ui.table_personnel.setItem(rowCount, i, QTableWidgetItem(str(value)))

        conn.close()  # Закрытие соединения с базой данных

    def function_switch_between_stack_widgets(self):
        # Метод для инициализации переключения между виджетами
        self.ui.btnHome.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(0))
        self.ui.btnPerson.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(1))
        self.ui.btnTopic.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(2))
        self.ui.helpBtn.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(3))

    def function_add_table_personnel(self):
        # Метод для инициализации функционала таблицы персонала
        self.ui.le_fio.returnPressed.connect(self.save_personnel)
        self.ui.le_zvanie.returnPressed.connect(self.save_personnel)
        self.ui.le_subunit.returnPressed.connect(self.save_personnel)
        self.ui.le_duty.returnPressed.connect(self.save_personnel)

        self.ui.btn_save_personnel.clicked.connect(self.save_personnel)
        self.ui.btn_delete_personnel.clicked.connect(self.delete_personnel)

        self.table_widget()

    def table_widget(self):
        # Метод для настройки внешнего вида таблицы
        self.ui.table_personnel.setRowCount(1)
        self.ui.table_personnel.setColumnCount(4)
        self.ui.table_personnel.setHorizontalHeaderLabels(['ФИО', 'В/зв', 'Подразделение', 'Должность'])
        self.ui.table_personnel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def save_personnel(self):
        # Метод для сохранения данных из полей ввода в таблицу интерфейса
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

    def delete_personnel(self):
        selected_ranges = self.ui.table_personnel.selectedRanges()
        if len(selected_ranges) > 0:
            conn = sqlite3.connect('personnel.db')
            cursor = conn.cursor()

            for selected_range in selected_ranges:
                top_row = selected_range.topRow()
                bottom_row = selected_range.bottomRow()

                for row in range(bottom_row, top_row - 1, -1):
                    # Assuming the first four columns are fio, rank, subunit, and duty
                    fio = self.ui.table_personnel.item(row, 0).text()
                    rank = self.ui.table_personnel.item(row, 1).text()
                    subunit = self.ui.table_personnel.item(row, 2).text()
                    duty = self.ui.table_personnel.item(row, 3).text()

                    # Delete the row from the database
                    cursor.execute('''DELETE FROM personnel WHERE fio=? AND rank=? AND subunit=? AND duty=?''',
                                   (fio, rank, subunit, duty))

                    # Remove the row from the GUI
                    self.ui.table_personnel.removeRow(row)

            conn.commit()
            conn.close()
        else:
            QMessageBox.warning(None, "Ошибка", "Выберите строки для удаления")


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создание экземпляра приложения
    window = MainWindow()  # Создание экземпляра главного окна
    window.show()  # Отображение главного окна
    sys.exit(app.exec_())  # Запуск цикла обработки событий приложения
