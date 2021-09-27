from PyQt5 import QtCore, QtGui, QtWidgets
import cv2, imutils


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(743, 478)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(450, 0))
        self.label.setStyleSheet("border:1px solid rgb(0, 0, 0);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 3, 6, 1)
        self.openBtn = QtWidgets.QPushButton(self.centralwidget)
        self.openBtn.setObjectName("openBtn")
        self.gridLayout.addWidget(self.openBtn, 4, 0, 1, 1)
        self.brightSlide = QtWidgets.QSlider(self.centralwidget)
        self.brightSlide.setMinimumSize(QtCore.QSize(170, 0))
        self.brightSlide.setMaximumSize(QtCore.QSize(170, 16777215))
        self.brightSlide.setOrientation(QtCore.Qt.Horizontal)
        self.brightSlide.setObjectName("brightSlide")
        self.gridLayout.addWidget(self.brightSlide, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 2, 1)
        self.blurSlide = QtWidgets.QSlider(self.centralwidget)
        self.blurSlide.setMinimumSize(QtCore.QSize(170, 0))
        self.blurSlide.setMaximumSize(QtCore.QSize(170, 16777215))
        self.blurSlide.setOrientation(QtCore.Qt.Horizontal)
        self.blurSlide.setObjectName("blurSlide")
        self.gridLayout.addWidget(self.blurSlide, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.saveBtn = QtWidgets.QPushButton(self.centralwidget)
        self.saveBtn.setMaximumSize(QtCore.QSize(75, 16777215))
        self.saveBtn.setObjectName("saveBtn")
        self.gridLayout.addWidget(self.saveBtn, 5, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 743, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.blurSlide.valueChanged['int'].connect(self.label.setNum)
        self.brightSlide.valueChanged['int'].connect(self.label.clear)
        self.openBtn.clicked.connect(self.label.clear)
        self.saveBtn.clicked.connect(self.label.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.filename = None
        self.tmpdir = None
        self.bright_val = 0
        self.blur_val = 0

        self.blurSlide.valueChanged['int'].connect(self.blurVal)
        self.brightSlide.valueChanged['int'].connect(self.brightValue)
        self.openBtn.clicked.connect(self.openImage)
        self.saveBtn.clicked.connect(self.save)

    def brightValue(self, value):
        if self.filename is not None:
            self.bright_val = value
            self.update()

    def blurVal(self, val):
        if self.filename is not None:
            self.blur_val = val
            self.update()

    def openImage(self):
        self.filename = QtWidgets.QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.image = cv2.imread(self.filename)
        self.setImage(self.image)

    def setImage(self, image):
        self.tmpdir = image
        image = imutils.resize(image, width=640)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def changeBrightness(self, img, value):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        print(h)
        return img

    def changeBlur(self, img, value):
        kernel_size = (value + 1, value + 1)
        img = cv2.blur(img, kernel_size)
        return img

    def update(self) -> None:
        img = self.changeBrightness(self.image, self.bright_val)
        img = self.changeBlur(img, self.blur_val)
        self.setImage(img)

    def save(self):
        if self.filename is not None:
            cv2.imwrite(self.filename, self.tmpdir)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Blur"))
        self.label.setText(_translate("MainWindow", "Öffnen"))
        self.openBtn.setText(_translate("MainWindow", "Öffnen"))
        self.label_3.setText(_translate("MainWindow", "Helligkeit"))
        self.saveBtn.setText(_translate("MainWindow", "Speichern"))


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    mw = Ui_MainWindow()
    mw.setupUi(MainWindow)
    MainWindow.show()
    app.exec()
