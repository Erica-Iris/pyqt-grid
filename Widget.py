from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QWidget


class Widget(QWidget):
    def __init__(self, view):
        super().__init__()
        self.setWindowTitle("grid demo")
        self.view = view

        self.center()

    def center(self):
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        center_point = screen_geometry.center()

        self.move(center_point - self.rect().center())

    def update_grid(self):
        visible_rect = self.rect()
        self.draw_grid(visible_rect)

    def draw_grid(self,rect):
        # Get the dimensions of the rect
        width = rect.width()
        height = rect.height()

        # Define grid properties
        grid_size = 50  # Size of each grid cell
        line_color = QColor(200, 200, 200)  # Light gray color for grid lines

        # Create a QPainter to draw on the widget
        painter = QPainter(self)
        painter.setPen(line_color)

        # Draw vertical lines
        for x in range(0, width, grid_size):
            painter.drawLine(x, 0, x, height)

        # Draw horizontal lines
        for y in range(0, height, grid_size):
            painter.drawLine(0, y, width, y)

        # End the painting
        painter.end()
