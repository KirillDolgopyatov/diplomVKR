from PyQt5 import QtCore, QtGui, QtWidgets
import Designer.log_res


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(700, 500)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        Form.setMinimumSize(QtCore.QSize(700, 500))
        Form.setStyleSheet("QFrame#frame{\n"
                           "border-image: url(:/images/images/mchs1.jpg);\n"
                           "border-top-left-radius: 80px;\n"
                           "border-bottom-right-radius: 40px;\n"
                           "}\n"
                           "\n"
                           "QFrame#frame_2{\n"
                           "background-color: rgba(0, 0, 0, 100);\n"
                           "border-bottom-right-radius: 40px;\n"
                           "}\n"
                           "")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(-1, 5, 5, 5)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(200, 0))
        self.frame_2.setStyleSheet("")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_close = QtWidgets.QPushButton(self.frame_2)
        self.btn_close.setStyleSheet("QPushButton {\n"
                                     "border-radius: 5px;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:Hover {\n"
                                     "    background-color: rgba(91, 91, 91, 150);\n"
                                     "border-radius: 5px;\n"
                                     "}")
        self.btn_close.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/images/close.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_close.setIcon(icon)
        self.btn_close.setIconSize(QtCore.QSize(20, 20))
        self.btn_close.setObjectName("btn_close")
        self.verticalLayout_3.addWidget(self.btn_close, 0, QtCore.Qt.AlignRight)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_login = QtWidgets.QLineEdit(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_login.setFont(font)
        self.lineEdit_login.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                          "border: none;\n"
                                          "border-radius: none;\n"
                                          "border-bottom: 3px solid rgba(105, 118, 132, 255);\n"
                                          "color: rgba(255, 255, 255, 230);\n"
                                          "padding-bottom:7px;\n"
                                          "")
        self.lineEdit_login.setText("")
        self.lineEdit_login.setObjectName("lineEdit_login")
        self.verticalLayout_5.addWidget(self.lineEdit_login)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_password = QtWidgets.QLineEdit(self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_password.setFont(font)
        self.lineEdit_password.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                             "border: none;\n"
                                             "border-radius: none;\n"
                                             "border-bottom: 3px solid rgba(105, 118, 132, 255);\n"
                                             "color: rgba(255, 255, 255, 230);\n"
                                             "padding-bottom:7px;\n"
                                             "")
        self.lineEdit_password.setText("")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.verticalLayout_4.addWidget(self.lineEdit_password)
        self.verticalLayout_3.addWidget(self.frame_4)
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem)
        self.btn_signin = QtWidgets.QPushButton(self.frame_2)
        self.btn_signin.setMinimumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.btn_signin.setFont(font)
        self.btn_signin.setStyleSheet("QPushButton {\n"
                                      "    background-color: rgb(155, 75, 12);\n"
                                      "color: rgba(0, 0, 0, 200);\n"
                                      "border-radius: 10px;\n"
                                      "    color: rgba(0, 0, 0, 180);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:Hover {\n"
                                      "    background-color: rgb(255, 124, 20);\n"
                                      "color: rgba(0, 0, 0, 200);\n"
                                      "border-radius: 10px;\n"
                                      "    color: rgba(0, 0, 0, 255);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:Pressed {\n"
                                      "    background-color: rgb(255, 124, 20);\n"
                                      "color: rgba(0, 0, 0, 200);\n"
                                      "border-radius: 5px;\n"
                                      "color: rgba(0, 0, 0, 255);\n"
                                      "}\n"
                                      "\n"
                                      "")
        self.btn_signin.setObjectName("btn_signin")
        self.verticalLayout_3.addWidget(self.btn_signin, 0, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.frame_2, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout_2.addWidget(self.widget)

        shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(30)
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(0)
        shadow_effect.setColor(QtGui.QColor(171, 85, 220, 100))
        self.frame.setGraphicsEffect(shadow_effect)

        shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(25)
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(0)
        shadow_effect.setColor(QtGui.QColor(234, 221, 186, 100))
        self.btn_signin.setGraphicsEffect(shadow_effect)


        self.translateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def translateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Логин"))
        self.lineEdit_login.setPlaceholderText(_translate("Form", " Введите логин"))
        self.label_2.setText(_translate("Form", "Пароль"))
        self.lineEdit_password.setPlaceholderText(_translate("Form", " Введите пароль"))
        self.btn_signin.setText(_translate("Form", "Войти"))


