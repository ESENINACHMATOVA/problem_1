from PyQt5.QtWidgets import (QWidget, QGridLayout, QRadioButton, QMainWindow, QApplication, QCheckBox,
                             QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsRectItem, QGraphicsLineItem,
                             QGraphicsEllipseItem,
                             )
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QTransform
from random import randint


def get_color():
    r, g, b, a = [25 * randint(4, 10) for i in range(4)]
    return QColor(r, g, b, a)


class GraphicsScene(QGraphicsScene):
    _draw = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pos = QPointF()
        self._name = None
        self._item = None
        self._mode = False

    def mousePressEvent(self, event):
        if not self._mode:
            super().mousePressEvent(event)
            return
        if self._name == 'Rect':
            self._item = QGraphicsRectItem()
        elif self._name == 'Ellipse':
            self._item = QGraphicsEllipseItem()
        elif self._name == 'Line':
            self._item = QGraphicsLineItem()
        else:
            return
        if not self.itemAt(event.scenePos(), QTransform()):
            self._pos = event.scenePos()
            if type(self._item) is QGraphicsLineItem:
                self._item.setLine(QLineF(self._pos, self._pos))
            else:
                self._item.setRect(QRectF(self._pos, self._pos))
            self._item.setPen(QPen(Qt.black, 1.0, Qt.DotLine))
            self.addItem(self._item)
            self._draw.emit(True)

    def mouseMoveEvent(self, event):
        if not self._mode:
            super().mouseMoveEvent(event)
            return
        if self._item:
            if type(self._item) is QGraphicsLineItem:
                self._item.setLine(QLineF(self._pos, event.scenePos()))
            else:
                rect = QRectF(self._pos, event.scenePos()).normalized()
                self._item.setRect(rect)

    def mouseReleaseEvent(self, event):
        if not self._mode:
            super().mouseReleaseEvent(event)
            return
        if self._item:
            self._item.setPen(QPen(get_color(), 2.0, Qt.SolidLine))
            try:
                self._item.setBrush(get_color())
            except:
                pass
            self._item.setFlag(QGraphicsItem.ItemIsMovable)
            self._item.setFlag(QGraphicsItem.ItemIsSelectable)
            self._item = None
            self._draw.emit(False)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.scene = GraphicsScene(self)
        view = QGraphicsView(self.scene)
        view.setRenderHint(QPainter.Antialiasing)
        view.setSceneRect(QRectF(0, 0, 600, 400))
        grid = QGridLayout(self)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(view, 0, 0, 8, 8)
        self.btns = []
        for x, i in enumerate(('Line', 'Rect', 'Ellipse')):
            btn = QRadioButton(i)
            btn.setObjectName(i)
            self.btns.append(btn)
            grid.addWidget(btn, x, 8, 2, 1)
            btn.toggled.connect(self.on_toggled)
        self.box = QCheckBox('Draw Mode')
        grid.addWidget(self.box, x + 1, 8, 2, 1)
        self.box.toggled.connect(self.on_box)
        self.box.setChecked(True)
        self.btns[0].toggle()
        self.scene._draw.connect(self.on_draw)

    def on_draw(self, value):
        if value:
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def on_toggled(self):
        self.scene._name = self.sender().objectName()

    def on_box(self, value):
        self.scene._mode = value


if __name__ == '__main__':
    app = QApplication([])
    w = Window()
    w.show()
    app.exec_()
