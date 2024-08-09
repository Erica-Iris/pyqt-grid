from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class Grid(QWidget):
    cBASELINE = Qt.yellow
    pBorderLine = QPen(Qt.black, 2, Qt.SolidLine)
    pBaseLine = QPen(cBASELINE, 0.3, Qt.SolidLine)

    def __init__(self):
        super().__init__()
        self.h = self.size().width()
        self.w = self.size().height()
        self.current_center_pos_offset_x = 0
        self.current_center_pos_offset_y = 0
        self.initUI()
        self.last_drag_x = 0  # previous X drag position
        self.last_drag_y = 0  # previous Y drag position

        self.zoom_level = 1
        self._zoom_factor = 1.05
        self._zoom_clamp = [0.3, 4]

    def initUI(self):
        self.setAutoFillBackground(True)
        print("init ui down")

    def mouseMoveEvent(self, a0):
        print("=" * 60)
        print("mouse pos: ", a0.pos())
        mx = a0.x()
        my = a0.y()

        delta_x = self.last_drag_x - mx
        delta_y = self.last_drag_y - my

        self.current_center_pos_offset_x -= delta_x
        self.current_center_pos_offset_y -= delta_y

        self.last_drag_x = mx
        self.last_drag_y = my

        self.repaint()

    def mousePressEvent(self, a0):
        print("=" * 60)
        print("mouse press event")
        mx, my = a0.x(), a0.y()
        button = a0.button()

        if button == Qt.LeftButton:
            self.last_drag_x = mx
            self.last_drag_y = my

    def mouseReleaseEvent(self, a0):
        print("mouse release")

    def wheelEvent(self, a0):
        zoom_factor = 1
        delta_x = self.current_center_pos_offset_x + self.w / 2 - a0.pos().x()
        delta_y = self.current_center_pos_offset_y + self.h / 2 - a0.pos().y()
        if a0.angleDelta().y() > 0 and self.zoom_level < self._zoom_clamp[1]:
            print("zoom in")
            zoom_factor = self._zoom_factor
            self.current_center_pos_offset_x += int(delta_x * (self._zoom_factor - 1))
            self.current_center_pos_offset_y += int(delta_y * (self._zoom_factor - 1))

        elif a0.angleDelta().y() < 0 and self.zoom_level > self._zoom_clamp[0]:
            print("zoom out")
            zoom_factor = 1 / self._zoom_factor
            self.current_center_pos_offset_x -= int(delta_x * (self._zoom_factor - 1))
            self.current_center_pos_offset_y -= int(delta_y * (self._zoom_factor - 1))

        self.zoom_level *= zoom_factor
        if self.zoom_level < self._zoom_clamp[0]:
            self.zoom_level = self._zoom_clamp[0]
        elif self.zoom_level > self._zoom_clamp[1]:
            self.zoom_level = self._zoom_clamp[1]
        # self.repaint()
        self.update()

    def draw_grid(self, qp):
        # draw grid
        for x in range(
            int(self.w / 2 + self.current_center_pos_offset_x),
            self.w,
            int(50 * self.zoom_level),
        ):
            qp.drawLine(int(x), 0, int(x), self.h)
        for x in range(
            int(self.w / 2 + self.current_center_pos_offset_x),
            0,
            -int(50 * self.zoom_level),
        ):
            qp.drawLine(int(x), 0, int(x), self.h)
        for y in range(
            int(self.h / 2 + self.current_center_pos_offset_y),
            self.h,
            int(50 * self.zoom_level),
        ):
            qp.drawLine(0, int(y), self.w, int(y))
        for y in range(
            int(self.h / 2 + self.current_center_pos_offset_y),
            0,
            -int(50 * self.zoom_level),
        ):
            qp.drawLine(0, int(y), self.w, int(y))
        if (
            self.current_center_pos_offset_x < -self.w / 2
            or self.current_center_pos_offset_x > self.w / 2
        ):
            pass

    def draw_baseline(self, qp):
        qp.setPen()
        if 0 < self.current_center_pos_offset_x + self.w / 2 < self.w:
            qp.drawLine(
                int(self.w / 2 + self.current_center_pos_offset_x),
                0,
                int(self.w / 2 + self.current_center_pos_offset_x),
                self.h,
            )
        if 0 < self.current_center_pos_offset_y + self.h / 2 < self.h:
            qp.drawLine(
                0,
                int(self.h / 2 + self.current_center_pos_offset_y),
                self.w,
                int(self.h / 2 + self.current_center_pos_offset_y),
            )

    def draw_info(self, qp):
        qp.drawText(20, 20, "last drag x: " + str(self.last_drag_x))
        qp.drawText(20, 30, "last drag y: " + str(self.last_drag_y))
        qp.drawText(
            20,
            40,
            "current center pos offset x: " + str(self.current_center_pos_offset_x),
        )
        qp.drawText(
            20,
            50,
            "current center pos offset y: " + str(self.current_center_pos_offset_y),
        )
        qp.drawText(20, 60, "center pos : " + str(self.last_drag_x))

    def draw_border(self, qp):
        # draw border

        qp.setPen(self.pBorderLine)
        qp.drawLine(0, 0, 0, self.h)
        qp.drawLine(0, self.h, self.w, self.h)
        qp.drawLine(self.w, self.h, self.w, 0)
        qp.drawLine(self.w, 0, 0, 0)

    def paintEvent(self, a0):
        qp = QPainter()
        qp.begin(self)

        size = self.size()
        self.w = size.width()
        self.h = size.height()

        qp.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.white, 0.25, Qt.DotLine)
        qp.setPen(pen)
        qp.setBrush(Qt.blue)

        self.draw_grid(qp)
        self.draw_baseline(qp)
        self.draw_border(qp)
        self.draw_info(qp)
        self.draw_center_point(qp)

        qp.end()

    def mouseDoubleClickEvent(self, a0):
        self.current_center_pos_offset_x = 0
        self.current_center_pos_offset_y = 0
        self.repaint()

    def draw_center_point(self, qp):
        qp.setPen(QPen(Qt.red, 3, Qt.DashLine))
        qp.drawPoint(int(self.w / 2), int(self.h / 2))
