import sys

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QVBoxLayout

from grid import Grid


class PyGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = Grid()
        self.initUI()
        self.center()

    def initUI(self):
        hbox = QVBoxLayout()
        hbox.addWidget(self.grid)

        self.setLayout(hbox)
        self.setWindowTitle("python grid demo")
        self.show()

    def center(self):
        available_rect = QDesktopWidget().availableGeometry()
        screen = QDesktopWidget().screenGeometry()
        width = int(available_rect.width() * 0.5)
        height = int(available_rect.height() * 0.5)
        left = (screen.width() - width) // 2
        top = (
            (screen.height() - height) // 2 + screen.height() - available_rect.height()
        )

        self.setGeometry(left, top, width, height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pygrid = PyGrid()
    sys.exit(app.exec_())
