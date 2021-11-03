from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YANDEX.PAINT")

        self.setGeometry(100, 100, 800, 600)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.b_size = 2
        self.b_color = Qt.black
        self.lastPoint = QPoint()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("Файл")
        b_size = mainMenu.addMenu("Размер кисти")
        b_color = mainMenu.addMenu("Цвет кисти")
        figure = mainMenu.addMenu('Фигуры')
        lastik = mainMenu.addMenu('Ластик')

        saveAction = QAction("Сохранить", self)
        saveAction.setShortcut("Ctrl + S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction("Очистить", self)
        clearAction.setShortcut("Ctrl+Del")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        last_4pix = QAction('4px', self)
        lastik.addAction(last_4pix)
        last_4pix.triggered.connect(self.whiteColor)
        last_4pix.triggered.connect(self.latfour)

        pix_4 = QAction("4px", self)
        b_size.addAction(pix_4)
        pix_4.triggered.connect(self.fourPixel)

        pix_7 = QAction("7px", self)
        b_size.addAction(pix_7)
        pix_7.triggered.connect(self.sevenPixel)

        pix_9 = QAction("9px", self)
        b_size.addAction(pix_9)
        pix_9.triggered.connect(self.ninePixel)

        pix_12 = QAction("12px", self)
        b_size.addAction(pix_12)
        pix_12.triggered.connect(self.twelvePixel)

        black = QAction("Черный", self)
        b_color.addAction(black)
        black.triggered.connect(self.blackColor)

        red = QAction("Красный", self)
        b_color.addAction(red)
        red.triggered.connect(self.redColor)

        green = QAction("Зеленый", self)
        b_color.addAction(green)
        green.triggered.connect(self.greenColor)

        yellow = QAction("Желтый", self)
        b_color.addAction(yellow)
        yellow.triggered.connect(self.yellowColor)

        square = QAction('Квадрат', self)
        figure.addAction(square)

        triangle = QAction('Треугольник', self)
        figure.addAction(triangle)

        circle = QAction('Круг', self)
        figure.addAction(circle)

        star = QAction('Звезда', self)
        figure.addAction(star)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.b_color, self.b_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def latfour(self):
        self.lastik = 4
        self.lastik = Qt.white

    def fourPixel(self):
        self.b_size = 4

    def fivePixel(self):
        self.b_size = 5

    def sevenPixel(self):
        self.b_size = 7

    def ninePixel(self):
        self.b_size = 9

    def twelvePixel(self):
        self.b_size = 12

    def blackColor(self):
        self.b_color = Qt.black

    def whiteColor(self):
        self.b_color = Qt.white

    def redColor(self):
        self.b_color = Qt.red

    def greenColor(self):
        self.b_color = Qt.green

    def yellowColor(self):
        self.b_color = Qt.yellow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()