from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class Grid(QWidget):
    def __init__(self):
        super().__init__()
        # self.current_center_pos_offset = QPoint(0, 0)
        self.h = self.size().width()
        self.w = self.size().height()
        self.current_center_pos_offset_x = 0
        self.current_center_pos_offset_y = 0
        self.initUI()
        self.last_drag_x = 0  # previous X drag position
        self.last_drag_y = 0  # previous Y drag position

        self.zoom_level = 1
        self._zoom_factor = 1.05
        self._zoom_clamp = [0.2, 4]

        self.info_list = []
        self.info_list.append(self.last_drag_x)
        self.info_list.append(self.last_drag_y)
        self.info_list.append(self.current_center_pos_offset_x)
        self.info_list.append(self.current_center_pos_offset_y)
        self.info_list.append(self.zoom_level)

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
        # print("=" * 60)
        # print("angleDelta: ", a0.angleDelta().y())
        # print("pixelDelta: ", a0.pixelDelta())
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
        pen = QPen(Qt.yellow, 0.3, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(
            int(self.w / 2 + self.current_center_pos_offset_x),
            0,
            int(self.w / 2 + self.current_center_pos_offset_x),
            self.h,
        )
        qp.drawLine(
            0,
            int(self.h / 2 + self.current_center_pos_offset_y),
            self.w,
            int(self.h / 2 + self.current_center_pos_offset_y),
        )
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        # draw border
        qp.drawLine(0, 0, 0, self.h)
        qp.drawLine(0, self.h, self.w, self.h)
        qp.drawLine(self.w, self.h, self.w, 0)
        qp.drawLine(self.w, 0, 0, 0)
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
        qp.drawPoint(int(self.w / 2), int(self.h / 2))
        qp.end()

    def mouseDoubleClickEvent(self, a0):
        self.current_center_pos_offset_x = 0
        self.current_center_pos_offset_y = 0
        self.repaint()
