from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import (QPainter, QPainterPath, QColor, QPen, QBrush, 
    QColorConstants, QTransform, QConicalGradient
)
from PyQt6.QtCore import Qt, QTimer, QRect, QRectF, QPointF, QMarginsF
import math

class WaitingArrowSpinnerWidget(QWidget):
    _norm_width = 500.0
    _norm_rect = QRectF(-_norm_width, -_norm_width, _norm_width * 2, _norm_width * 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._angle = 0.0
        self._hue_offset = 0.0
        self._rotation_increment = 2
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.updateRotation)
        self._timer.setInterval(16)
        self._isSpinning = False
        self._arrow_count = 3
        self._sweep = (360 / self._arrow_count) - 15 # Span in degrees
        self._thickness_ratio = 5
        self._arrow_length_ratio = 2.0
        self._arrow_width_ratio =  2 / (1 + math.sqrt(5))
        self.buildArrowArcPaths()
        self.buildComponents()

    def updateRotation(self):
        self._angle = (self._angle + self._rotation_increment) % 360
        self._hue_offset = (self._hue_offset + 1.0) % 360  # Increment hue by 1° per tick
        self.buildGradient()
        self.update()

    def buildArrowArcPaths(self):
        """Create normalized QPainterPath for the arrow and its mirrored version."""
        width = self._norm_width
        rect = self._norm_rect
        thickness = width / self._thickness_ratio
        barb_margin = QMarginsF(*[thickness * self._arrow_width_ratio] * 4)
        thickness_margin = QMarginsF(*[thickness] * 4)
        indent_arc = 3

        outer_ring_rect = rect - barb_margin
        mid_ring_rect = outer_ring_rect - (0.5 * thickness_margin)
        inner_ring_rect = outer_ring_rect - thickness_margin
        inner_arrow_rect = inner_ring_rect - barb_margin

        arrow_tip = QPointF(mid_ring_rect.right(), thickness * 2.0)
        self._norm_arc_start_angle = math.degrees(math.atan2(-arrow_tip.y(), arrow_tip.x()))

        adj_sweep = self._sweep + self._norm_arc_start_angle

        # Create path
        path = QPainterPath()
        path.moveTo(inner_arrow_rect.right(), 0)
        path.lineTo(arrow_tip)
        path.lineTo(rect.right(), 0)
        path.arcTo(outer_ring_rect, -indent_arc, 0)
        path.arcTo(outer_ring_rect, -indent_arc, indent_arc + adj_sweep)
        path.arcTo(inner_ring_rect, adj_sweep, 0)
        path.arcTo(inner_ring_rect, adj_sweep, -(adj_sweep + indent_arc))
        path.closeSubpath()

        self._paths = [path]
        for arrow in range(1, self._arrow_count):
            rotated = QTransform().rotate(arrow * 360 / self._arrow_count).map(path)
            self._paths.append(rotated)


    def buildScaleTransform(self):
        """Create QTransform to scale normalized path to widget rect."""
        rect = self.rect()

        scale_x = rect.width() / self._norm_rect.width()
        scale_y = rect.height() / self._norm_rect.height()

        self._scale_transform = QTransform().scale(scale_x, scale_y)

    def buildTranslateTransform(self):
        """Create QTransform to translate normalized path to widget rect."""
        rect = self.rect()
        translate_x = rect.x() - self._norm_rect.x()
        translate_y = rect.y() - self._norm_rect.y()
        self._translate_transform = QTransform().translate(translate_x, translate_y)


    def buildGradient(self):
        arc_start_angle = self._arc_start_angle
        """Create QConicalGradient for the arc."""
        gradient = QConicalGradient(QPointF(0, 0), self._norm_arc_start_angle)

        cyan_hue = (180 + self._hue_offset) % 360
        blue_hue = (240 + self._hue_offset) % 360
        trans_hue = (120 + self._hue_offset) % 360

        ch = QColor.fromHsvF(cyan_hue / 360, 1.0, 1.0, 1.0)  # Cyan, full alpha
        bh = QColor.fromHsvF(blue_hue / 360, 1.0, 1.0, 1.0)  # Blue, full alpha
        th = QColor.fromHsvF(trans_hue / 360, 1.0, 1.0, 0.0)  # Transparent
        th.setAlpha(0)


        for arrow in range(0, self._arrow_count):
            gradient.setColorAt((arrow / self._arrow_count), ch)
            gradient.setColorAt((arrow / self._arrow_count)  +  0.5 * (self._sweep / 360), bh)
            gradient.setColorAt((arrow / self._arrow_count)  +  (self._sweep / 360), th)

        gradient.setColorAt(1.0, ch)

        self._gradient = gradient

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.buildComponents()

    def buildComponents(self):

        self.buildScaleTransform()
        self.buildTranslateTransform()
        self._transform = self._translate_transform * self._scale_transform

        scaled_pointf = self._scale_transform.map(
            QPointF(math.cos(self._norm_arc_start_angle), math.sin(self._norm_arc_start_angle))
        )

        self._arc_start_angle = math.atan2(scaled_pointf.x(), scaled_pointf.y())

        self.buildGradient()

    def mousePressEvent(self, event):
        """Toggle animation on mouse click."""
        if event.button() == Qt.MouseButton.LeftButton:
            if self._isSpinning:
                self.stop()
            else:
                self.start()

            event.accept()
            return
        event.ignore()

    def drawArrowPaths(self, painter):
        """Draw the precomputed arrow paths with scaling and gradient."""
        painter.save()
        # Apply scaling and translation
        # transform = self._scale_transform
        # scaled_paths = [transform.map(path) for path in self._paths]
        scaled_paths = self._paths

        # Apply gradient
        gradient = self._gradient
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)

        for path in scaled_paths:
            painter.drawPath(path)

        painter.restore()

    def paintEvent(self, event):
        if self._isSpinning:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            painter.save()
            painter.setTransform( QTransform().rotate(self._angle) * self._transform)
            self.drawArrowPaths(painter)

            painter.restore()

    def start(self):
        self._isSpinning = True
        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    def stop(self):
        self._isSpinning = False
        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0
        self.update()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    widget = WaitingArrowSpinnerWidget()
    widget.resize(400, 400)
    widget.start()
    widget.show()
    sys.exit(app.exec())