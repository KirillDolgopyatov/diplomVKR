import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow)

from Designer.designerVKR import Ui_MainWindow


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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
