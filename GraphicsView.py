from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
import time


class GraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test grid draw")
        self.setGeometry(0,0,800,680)
        self.setScene(QGraphicsScene(self))
        self.setBackgroundBrush(QColor(52, 160, 164))

        self.timer = QTimer(self)
        self.timer.setInterval(int(1000/50))  # Set interval to 1000 ms (1 second)
        self.timer.timeout.connect(self.update_grid)
        self.timer.start()  # Start the timer

        print("finsh init graphicsView")

    def draw_grid(self, visible_rect):
        # Clear the previous grid
        self.scene().clear()

        # Get the grid size
        grid_size = 20  # Size of each grid cell

        # Draw vertical lines
        for x in range(int(visible_rect.left()), int(visible_rect.right()), grid_size):
            self.scene().addLine(x, visible_rect.top(), x, visible_rect.bottom(), QColor(0, 0, 0))

        # Draw horizontal lines
        for y in range(int(visible_rect.top()), int(visible_rect.bottom()), grid_size):
            self.scene().addLine(visible_rect.left(), y, visible_rect.right(), y, QColor(0, 0, 0))

    def update_grid(self):
        rect = self.sceneRect()
        self.draw_grid(rect)