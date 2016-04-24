#!/usr/bin/env python
import sys

from PyQt4 import QtCore, QtGui


class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        #left dwg
        self.scene = QtGui.QGraphicsScene()
        self.view = QtGui.QGraphicsView(self.scene)
        #right dwg
        self.scene2 = QtGui.QGraphicsScene()
        self.view2 = QtGui.QGraphicsView(self.scene2)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.view2)
        self.setLayout(layout)
        self.pixmap_item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap('pic.JPG'), None, self.scene)
        self.pixmap2_item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap('pic.JPG'), None, self.scene2)
        self.pixmap_item.setScale(0.5)
        self.pixmap2_item.setScale(0.5)

        self.newy = 0
        self.pixmap_item.mousePressEvent = self.pixelSelect


    def paintEvent(self, event):

        point = event.pos()
        self.newy = point.y()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.drawRect(0,newy,300,newy+50)
        qp.end()


    def pixelSelect(self, event):
        # self.click_positions.append(event.pos())
        # if len(self.click_positions) < 4:
        #     return
        # pen = QtGui.QPen(QtCore.Qt.red)
        # self.scene.addPolygon(QtGui.QPolygonF(self.click_positions), pen)
        # for point in self.click_positions:
        #     self.scene.addEllipse(point.x(), point.y(), 2, 2, pen)
        # self.click_positions = []



        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.drawRect(0,self.newy,300,self.newy+50)
        qp.end()






if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = MainWidget()
    widget.resize(1024, 768)
    widget.show()
    sys.exit(app.exec_())