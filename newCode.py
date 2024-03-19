import sqlite3  # Импорт модуля для работы с SQLite
import sys  # Импорт системного модуля

import PyQt5
from PyQt5.QtCore import QDateTime, QSize, QTimer, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, \
    QMessageBox, QCompleter, QTableWidget, QLineEdit, QPushButton, QLabel, \
    QHBoxLayout, QFrame, QVBoxLayout, QWidget, QSizePolicy  # Импорт необходимых классов из PyQt5

from Designer.des import Ui_MainWindow  # Импорт дизайна интерфейса, созданного в Qt Designer
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
class MainWindow(QMainWindow):  # Определение класса MainWindow, наследующего QMainWindow
    def __init__(self):
        super().__init__()  # Вызов конструктора базового класса
        self.animation = None
        self.ui = Ui_MainWindow()  # Создание экземпляра дизайна интерфейса
        self.ui.setupUi(self)  # Настройка интерфейса в текущем окне

        self.function_switch_between_stack_widgets()  # Инициализация переключения между виджетами
        self.function_add_table_personnel()  # Инициализация функционала таблицы персонала

        self.ui.helpBtn.clicked.connect(self.slideRightSubMenu)
        self.ui.closeCenterMenu_2.clicked.connect(self.slideRightSubMenu)
        self.installEventFilter(self)

        self.db_connection = sqlite3.connect('saveData/personnel.db')  # Подключение к базе данных SQLite
        self.cursor = self.db_connection.cursor()  # Создание курсора для работы с базой данных
        self.load_data_from_sqlite()  # Загрузка данных из базы данных при запуске приложения

        self.ui.table_personnel.itemChanged.connect(self.save_data_to_sqlite)

        self.setup_completer()
        self.create_tables_in_toolbox()
        self.load_tables_at_startup()

        self.ui.btn_new_task.clicked.connect(self.addTask)

        #   Для обновления дедлайн в задачах
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

    def fetch_names_from_db(self):
        self.cursor.execute("SELECT fio FROM personnel")
        rows = self.cursor.fetchall()
        names = [row[0] for row in rows]  # Извлекаем имена из первого столбца
        return names

    def populate_combobox(self):
        names = self.fetch_names_from_db()
        self.ui.comboBox.clear()  # Очищаем comboBox перед заполнением
        self.ui.comboBox.addItems(names)  # Добавляем имена в comboBox
    ####################################################################################################################
    def load_tables_at_startup(self):
        cursor = self.db_connection.cursor()
        # Получаем список всех таблиц в базе данных
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table_name in tables:
            # Пропускаем системные таблицы SQLite, если они есть
            if table_name[0].startswith('sqlite_'):
                continue

            # Проверяем, начинается ли имя таблицы с 'table_data_page_'
            if not table_name[0].startswith('table_data_page_'):
                continue

            # Для каждой таблицы загружаем данные
            cursor.execute(f"SELECT * FROM {table_name[0]}")
            rows = cursor.fetchall()

            # Находим соответствующий QTableWidget для текущей таблицы
            try:
                page_index = int(table_name[0].split('_')[-1])  # Получаем индекс страницы из имени таблицы
                page = self.ui.toolBox.widget(page_index)
                tableWidget = self.find_table_widget(page)
                tableWidget.setStyleSheet("""
                            QTableWidget {
                            }
                            QTableWidget QHeaderView::section {
                                color: black;
                                background-color: rgb(173, 142, 57);
                                padding-left: 5px;
                                padding-right: 5px;
                            }
                            QTableWidget::item {
                                color:black;
                                background-color: rgb(217, 217, 217);
                            }
                        """)
            except (ValueError, IndexError):
                continue  # Если не удается найти соответствующий виджет, пропускаем таблицу

            if tableWidget is None:
                continue

            # Очищаем виджет таблицы перед заполнением
            tableWidget.setRowCount(0)
            tableWidget.setColumnCount(len(rows[0]) - 1 if rows else 0)  # Уменьшаем количество столбцов на один

            # Заполняем виджет таблицы данными, пропуская первый столбец
            for row_data in rows:
                row_position = tableWidget.rowCount()
                tableWidget.insertRow(row_position)
                for column, value in enumerate(row_data[1:]):  # Начинаем с 1, чтобы пропустить первый столбец
                    tableWidget.setItem(row_position, column, QTableWidgetItem(str(value)))

    ####################################################################################################################
    def save_tables_data(self):
        cursor = self.db_connection.cursor()
        # Предполагаем, что у нас есть отдельные таблицы для каждой страницы в QToolBox
        for page_index in range(self.ui.toolBox.count()):
            page = self.ui.toolBox.widget(page_index)
            tableWidget = self.find_table_widget(page)
            if tableWidget:
                table_name = f"table_data_page_{page_index}"
                # Определяем количество столбцов для текущей таблицы
                num_columns = tableWidget.columnCount()
                # Формируем строку с описанием столбцов для SQL запроса
                columns_description = ", ".join([f"column{i + 2} TEXT" for i in range(num_columns)])
                # Создаем новую таблицу для каждой страницы QToolBox, если она не существует
                cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                                    id INTEGER PRIMARY KEY,
                                    {columns_description}
                                  )''')
                # Очищаем таблицу перед сохранением новых данных
                cursor.execute(f'DELETE FROM {table_name}')
                for row in range(tableWidget.rowCount()):
                    # Собираем данные из всех столбцов текущей строки
                    row_data = []
                    for column in range(num_columns):
                        item = tableWidget.item(row, column)
                        row_data.append(item.text() if item else "")
                    # Формируем строку значений для SQL запроса
                    values_placeholder = ", ".join(["?"] * num_columns)
                    cursor.execute(
                        f'''INSERT INTO {table_name} ({", ".join([f"column{i + 2}" for i in range(num_columns)])})
                                      VALUES ({values_placeholder})''', row_data)
        self.db_connection.commit()

    ####################################################################################################################
    def update_toolbox_tables(self):
        # Получаем данные из table_personnel
        data = self.load_data_from_first_column()
        # Обновляем таблицы в QToolBox
        for i in range(self.ui.toolBox.count()):
            page = self.ui.toolBox.widget(i)
            tableWidget = self.find_table_widget(page)
            if tableWidget:
                # Получаем текущее количество строк в таблице
                currentRowCount = tableWidget.rowCount()
                for index, row_data in enumerate(data):
                    if index < currentRowCount:
                        # Обновляем существующую строку
                        tableWidget.item(index, 0).setText(str(row_data))
                    else:
                        # Добавляем новую строку, если данных больше, чем строк в таблице
                        row_position = tableWidget.rowCount()
                        tableWidget.insertRow(row_position)
                        tableWidget.setStyleSheet("""
                                                    QTableWidget {
                                                    }
                                                    QTableWidget QHeaderView::section {
                                                        color: black;
                                                        background-color: rgb(173, 142, 57);
                                                        padding-left: 5px;
                                                        padding-right: 5px;
                                                    }
                                                    QTableWidget::item {
                                                        color:black;
                                                        background-color: rgb(217, 217, 217);
                                                    }
                                                """)
                        tableWidget.setItem(row_position, 0, QTableWidgetItem(str(row_data)))
                # Если в таблице больше строк, чем данных, удаляем лишние строки с конца
                while tableWidget.rowCount() > len(data):
                    tableWidget.removeRow(tableWidget.rowCount() - 1)

    def load_data_from_first_column(self):
        """Загрузка данных из первого столбца таблицы базы данных."""
        self.cursor.execute("SELECT fio FROM personnel")
        return [item[0] for item in self.cursor.fetchall()]

    def create_tables_in_toolbox(self):
        """Создание таблиц в каждой странице QToolBox с данными из столбца fio."""
        data = self.load_data_from_first_column()
        count_tem = self.load_count_tem()
        self.ui.toolBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for i in range(self.ui.toolBox.count()):
            page = self.ui.toolBox.widget(i)
            # Предполагается, что функция load_count_tem возвращает количество столбцов для каждой таблицы
            num_columns = next(count_tem)  # Получаем количество столбцов из генератора
            tableWidget = QTableWidget(len(data), num_columns + 1)  # Создаем таблицу с нужным количеством столбцов
            tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Устанавливаем политику размеров
            tableWidget.setStyleSheet("color:black;")
            tableWidget.setColumnWidth(0, 400)
            # Устанавливаем заголовки столбцов, первый столбец - "ФИО", остальные - согласно количеству
            tableWidget.setHorizontalHeaderLabels(['ФИО'] + [f'Тема {i}' for i in range(1, num_columns + 1)])
            for row, item in enumerate(data):
                tableWidget.setItem(row, 0, QTableWidgetItem(item))

            # Добавляем созданную таблицу на страницу
            page.layout().addWidget(tableWidget)

    ####################################################################################################################
    def setup_completer(self):
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

    ####################################################################################################################
    def save_data_to_sqlite(self):
        # Метод для сохранения данных из таблицы в базу данных SQLite
        conn = sqlite3.connect('saveData/personnel.db')  # Подключение к базе данных
        cursor = conn.cursor()  # Создание курсора

        # Создание таблицы, если она не существует, с добавлением столбца id
        cursor.execute('''CREATE TABLE IF NOT EXISTS personnel (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            fio TEXT,
                            rank TEXT,
                            subunit TEXT,
                            duty TEXT
                        )''')

        # Остальная часть метода...

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

    def load_data_from_sqlite(self):
        # Метод для загрузки данных из базы данных SQLite в таблицу интерфейса
        conn = sqlite3.connect('saveData/personnel.db')  # Подключение к базе данных
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

    ####################################################################################################################
    def function_switch_between_stack_widgets(self):
        # Метод для инициализации переключения между виджетами
        self.ui.btnHome.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(0))
        self.ui.btnPerson.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(1))
        self.ui.btnTopic.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(2))
        self.ui.helpBtn.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(3))

    ####################################################################################################################
    def function_add_table_personnel(self):
        # Метод для инициализации функционала таблицы персонала
        self.ui.le_fio.returnPressed.connect(self.save_personnel)
        self.ui.le_zvanie.returnPressed.connect(self.save_personnel)
        self.ui.le_subunit.returnPressed.connect(self.save_personnel)
        self.ui.le_duty.returnPressed.connect(self.save_personnel)

        self.ui.btn_save_personnel.clicked.connect(self.save_personnel)
        self.ui.btn_delete_personnel.clicked.connect(self.delete_personnel)

        self.table_widget()

    ####################################################################################################################
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

        self.update_toolbox_tables()

    def delete_personnel(self):
        selected_ranges = self.ui.table_personnel.selectedRanges()
        if len(selected_ranges) > 0:
            conn = sqlite3.connect('saveData/personnel.db')
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

        self.update_toolbox_tables()

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
    @staticmethod
    def load_count_tem():
        count_tem = [4, 6, 6, 4, 40, 60, 6, 4, 20, 4, 30, 10, 4, 10, 54, 16, 10, 8]
        while True:  # Создаем бесконечный цикл
            for num in count_tem:
                yield num  # Возвращаем число из списка и приостанавливаем выполнение

    ####################################################################################################################
    @staticmethod
    def find_table_widget(page):
        """
        Находит и возвращает первый найденный QTableWidget на указанной странице QToolBox.
        :param page: Страница QToolBox, на которой необходимо найти QTableWidget.
        :return: Экземпляр QTableWidget, если найден, иначе None.
        """
        # Проверяем, есть ли у страницы layout
        if page.layout() is not None:
            # Проходимся по всем элементам layout
            for i in range(page.layout().count()):
                widget = page.layout().itemAt(i).widget()
                # Если виджет является экземпляром QTableWidget, возвращаем его
                if isinstance(widget, QTableWidget):
                    return widget
        return None

    ####################################################################################################################
    def closeEvent(self, event):
        """Override the close event to save table data before closing."""
        self.save_tables_data()
        super().closeEvent(event)

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
        self.animation.setEasingCurve(QEasingCurve.InQuart)
        self.animation.start()


########################################################################################################################
########################################################################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    window = MainWindow()
    form.show()
    sys.exit(app.exec_())
