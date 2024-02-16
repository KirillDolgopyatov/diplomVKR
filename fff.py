import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow)

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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnHome.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(0))
        self.ui.btnPerson.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(1))
        self.ui.btnTopic.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(2))
        self.ui.helpBtn.clicked.connect(lambda: self.ui.MainStack.setCurrentIndex(3))

    ####################################################################################################################

    def closeEvent(self, event):
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    window = MainWindow()
    form.show()
    sys.exit(app.exec_())
