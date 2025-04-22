import random
import time
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout
)
from board import Board

LEVELS = [
    (8, 10),
    (16, 40),
    (24, 99)
]

STATUS_READY = 0
STATUS_PLAYING = 1
STATUS_FAILED = 2
STATUS_SUCCESS = 3

STATUS_ICONS = {
    STATUS_READY: "./images/plus.png",
    STATUS_PLAYING: "./images/smile.png",
    STATUS_FAILED: "./images/cross.png",
    STATUS_SUCCESS: "./images/smile.png",
}


class GameWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.images = {
            "bomb": QPixmap(QImage("./images/bug.png")),
            "flag": QPixmap(QImage("./images/flag.png")),
            "start": QPixmap(QImage("./images/rocket.png")),
            "clock": QPixmap(QImage("./images/clock.png"))
        }

        self.init_window()

    def init_window(self):
        self.b_size, self.n_mines = LEVELS[1]

        w = QWidget()
        hb = QHBoxLayout()

        self.mines = QLabel()
        self.clock = QLabel()
        self.mines.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.clock.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        font = self.mines.font()
        font.setPointSize(24)
        font.setWeight(75)
        self.mines.setFont(font)
        self.clock.setFont(font)

        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)
        self._timer.start(1000)

        self.mines.setText("%03d" % self.n_mines)
        self.clock.setText("000")

        self.button = QPushButton()
        self.button.setFixedSize(QSize(32, 32))
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon("./images/smile.png"))
        self.button.setFlat(True)
        self.button.pressed.connect(self.button_pressed)

        bomb_icon = QLabel()
        bomb_icon.setPixmap(self.images["bomb"])
        bomb_icon.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        hb.addWidget(bomb_icon)
        hb.addWidget(self.mines)
        hb.addWidget(self.button)
        hb.addWidget(self.clock)

        clock_icon = QLabel()
        clock_icon.setPixmap(self.images["clock"])
        clock_icon.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        hb.addWidget(clock_icon)

        vb = QVBoxLayout()
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        vb.addLayout(self.grid)

        w.setLayout(vb)
        self.setCentralWidget(w)

        self.init_map()
        self.update_status(STATUS_READY)
        self.reset_map()
        self.update_status(STATUS_READY)
        self.show()

    def init_map(self):
        for x in range(self.b_size):
            for y in range(self.b_size):
                w = Board(x, y, self.images)
                self.grid.addWidget(w, y, x)
                w.clicked.connect(self.trigger_start)
                w.expandable.connect(self.expand_reveal)
                w.ohno.connect(self.game_over)

    def reset_map(self):
        for x in range(self.b_size):
            for y in range(self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reset()

        positions = []
        while len(positions) < self.n_mines:
            x, y = random.randint(0, self.b_size - 1), random.randint(0, self.b_size - 1)
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_mine = True
                positions.append((x, y))

        def get_adjacency_n(x, y):
            return sum(1 for w in self.get_surrounding(x, y) if w.is_mine)

        for x in range(self.b_size):
            for y in range(self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.adjacent_n = get_adjacency_n(x, y)

        while True:
            x, y = random.randint(0, self.b_size - 1), random.randint(0, self.b_size - 1)
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_start = True
                for s in self.get_surrounding(x, y):
                    if not s.is_mine:
                        s.click()
                break

    def get_surrounding(self, x, y):
        positions = []
        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                positions.append(self.grid.itemAtPosition(yi, xi).widget())
        return positions

    def button_pressed(self):
        if self.status == STATUS_PLAYING:
            self.update_status(STATUS_FAILED)
            self.reveal_map()
        elif self.status == STATUS_FAILED:
            self.update_status(STATUS_READY)
            self.reset_map()

    def reveal_map(self):
        for x in range(self.b_size):
            for y in range(self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reveal()

    def expand_reveal(self, x, y):
        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                w = self.grid.itemAtPosition(yi, xi).widget()
                if not w.is_mine:
                    w.click()

    def trigger_start(self, *args):
        if self.status != STATUS_PLAYING:
            self.update_status(STATUS_PLAYING)
            self._timer_start_nsecs = int(time.time())

    def update_status(self, status):
        self.status = status
        self.button.setIcon(QIcon(STATUS_ICONS[self.status]))

    def update_timer(self):
        if self.status == STATUS_PLAYING:
            n_secs = int(time.time()) - self._timer_start_nsecs
            self.clock.setText("%03d" % n_secs)

    def game_over(self):
        self.reveal_map()
        self.update_status(STATUS_FAILED)


if __name__ == '__main__':
    app = QApplication([])
    window = GameWindow()
    app.exec()
