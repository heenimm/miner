from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPixmap, QFont
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QSize, Qt
from typing import Dict


NUM_COLORS = {
    1: QColor('#f44336'),
    2: QColor('#9C27B0'),
    3: QColor('#3F51B5'),
    4: QColor('#03A9F4'),
    5: QColor('#00BCD4'),
    6: QColor('#4CAF50'),
    7: QColor('#E91E63'),
    8: QColor('#FF9800')
}


class Board(QWidget):
    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal()
    ohno = pyqtSignal()

    def __init__(self, x, y, images: Dict[str, QPixmap], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = images
        self.setFixedSize(QSize(20, 20))
        self.x = x
        self.y = y
        self.reset()

    def reset(self):
        self.is_start = False
        self.is_mine = False
        self.adjacent_n = 0
        self.is_revealed = False
        self.is_flagged = False
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = event.rect()
        if self.is_revealed:
            color = self.palette().color(self.backgroundRole())
            outer, inner = color, color
        else:
            outer, inner = Qt.GlobalColor.gray, Qt.GlobalColor.lightGray
        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed:
            if self.is_start:
                p.drawPixmap(r, self.images["start"])
            elif self.is_mine:
                p.drawPixmap(r, self.images["bomb"])
            elif self.adjacent_n > 0:
                pen = QPen(NUM_COLORS[self.adjacent_n])
                p.setPen(pen)
                f = QFont()
                f.setBold(True)
                p.setFont(f)
                p.drawText(r, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, str(self.adjacent_n))
        elif self.is_flagged:
            p.drawPixmap(r, self.images["flag"])

    def flag(self):
        self.is_flagged = True
        self.update()
        self.clicked.emit()

    def reveal(self):
        self.is_revealed = True
        self.update()

    def click(self):
        if not self.is_revealed:
            self.reveal()
            if self.adjacent_n == 0:
                self.expandable.emit(self.x, self.y)
        self.clicked.emit()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton and not self.is_revealed:
            self.flag()
        elif e.button() == Qt.MouseButton.LeftButton:
            self.click()
            if self.is_mine:
                self.ohno.emit()
