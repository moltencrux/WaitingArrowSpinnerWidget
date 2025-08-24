from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import (QPainter, QPainterPath, QColor, QPen, QBrush, 
    QColorConstants, QTransform, QConicalGradient
)
from PyQt6.QtCore import Qt, QTimer, QRect, QRectF, QPointF, QMarginsF
import math

class WaitingArrowSpinnerWidget(QWidget):
    _norm_width = 1000.0
    _norm_rect = QRectF(-_norm_width / 2, -_norm_width / 2, _norm_width, _norm_width)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._angle = 0.0
        self._hue_offset = 0.0
        self._flip = 1
        self._revolutions_per_second = 60
        self._rotation_increment = 2
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.updateRotation)
        self._timer.setInterval(16)
        self._isSpinning = False
        self._grayed_out = False  # Track grayed-out state
        self._gap_ratio = 0.2
        self._arrow_count = 3
        self._sweep = (1 - self._gap_ratio) * (360 / self._arrow_count) # Span in degrees
        self._thickness_ratio = 0.1  # thickness of the arrow body as a ratio of widget dimensions
        self._arrow_width_ratio = 0.075  # width of the arrow barbs as a ratio of the screen dimensions
        self._arrow_length_ratio = 0.3 # ratio of the arrow as a proportion of the body
        self._barb_indent_ratio = 0.03  # ratio of the whole arrow
        self.buildArrowArcPaths()
        self.buildComponents()


    def setClockwise(self, clockwise):
        self._flip = 1 if clockwise else -1

    def setFrameRate(self, rate):
        self._timer.setInterval(1000 // rate)
        self._rotation_increment = self._revolutions_per_second * self._timer.interval() * 360 / 1000

    def setRevolutionsPerSecond(self, rps):
        self._revolutions_per_second = rps
        self._rotation_increment = rps * self._timer.interval() * 360 / 1000

    def setGapRatio(self, gap_ratio):
        self._gap_ratio = gap_ratio
        self._sweep = (1 - self._gap_ratio) * (360 / self._arrow_count)
        self.buildArrowArcPaths()
        self.buildComponents()

    def setArrowCount(self, arrow_count):
        self._arrow_count = arrow_count
        self._sweep = (1 - self._gap_ratio) * (360 / self._arrow_count)
        self.buildArrowArcPaths()
        self.buildComponents()

    def setThicknessRatio(self, thickness_ratio):
        self._thickness_ratio = thickness_ratio
        self.buildArrowArcPaths()
        self.buildComponents()

    def setArrowWidthRatio(self, arrow_width_ratio):
        self._arrow_width_ratio = arrow_width_ratio
        self.buildArrowArcPaths()
        self.buildComponents()

    def setArrowLengthRatio(self, arrow_length_ratio):
        self._arrow_length_ratio = arrow_length_ratio
        self.buildArrowArcPaths()
        self.buildComponents()

    def setBarbIndentRatio(self, barb_indent_ratio):
        self._barb_indent_ratio = barb_indent_ratio
        self.buildArrowArcPaths()
        self.buildComponents()

    def updateRotation(self):
        self._angle = (self._angle + self._rotation_increment) % 360
        self._hue_offset = (self._hue_offset + 1.0) % 360  # Increment hue by 1° per tick
        self.buildGradient()
        self.update()

    def buildArrowArcPaths(self):
        """Create normalized QPainterPath for the arrow and its duplicates."""
        width = self._norm_width
        rect = self._norm_rect
        thickness = self._norm_width * self._thickness_ratio
        barb_extension = self._arrow_width_ratio * self._norm_width
        barb_margin = QMarginsF(*[barb_extension] * 4)
        thickness_margin = QMarginsF(*[thickness] * 4)
        indent_arc = self._sweep * self._barb_indent_ratio

        outer_ring_rect = rect - barb_margin
        mid_ring_rect = outer_ring_rect - (0.5 * thickness_margin)
        inner_ring_rect = outer_ring_rect - thickness_margin
        inner_arrow_rect = inner_ring_rect - barb_margin

        mid_ring_rect.right() * math.tan(self._sweep * self._arrow_length_ratio)

        arrow_tip = QPointF(mid_ring_rect.right(), mid_ring_rect.right() * math.tan(math.radians(self._sweep * self._arrow_length_ratio)))

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
        """Create QConicalGradient for the arc, grayed out if disabled."""
        gradient = QConicalGradient(QPointF(0, 0), self._norm_arc_start_angle)
        if self._grayed_out:
            # Grayscale gradient
            gray1 = QColor.fromHsvF(0, 0, 0.7, 1.0)  # Light gray
            gray2 = QColor.fromHsvF(0, 0, 0.3, 1.0)  # Dark gray
            transparent = QColor.fromHsvF(0, 0, 0, 0.0)  # Transparent
            for arrow in range(self._arrow_count):
                gradient.setColorAt(arrow / self._arrow_count, gray1)
                gradient.setColorAt((arrow / self._arrow_count) + 0.5 * (self._sweep / 360), gray2)
                gradient.setColorAt((arrow / self._arrow_count) + (self._sweep / 360), transparent)
            gradient.setColorAt(1.0, gray1)
        else:
            # Colorful gradient
            cyan_hue = (180 + self._hue_offset) % 360
            blue_hue = (240 + self._hue_offset) % 360
            trans_hue = (120 + self._hue_offset) % 360
            ch = QColor.fromHsvF(cyan_hue / 360, 1.0, 1.0, 1.0)
            bh = QColor.fromHsvF(blue_hue / 360, 1.0, 1.0, 1.0)
            th = QColor.fromHsvF(trans_hue / 360, 1.0, 1.0, 0.0)
            th.setAlpha(0)
            for arrow in range(self._arrow_count):
                gradient.setColorAt(arrow / self._arrow_count, ch)
                gradient.setColorAt((arrow / self._arrow_count) + 0.5 * (self._sweep / 360), bh)
                gradient.setColorAt((arrow / self._arrow_count) + (self._sweep / 360), th)
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


    def drawArrowPaths(self, painter):
        """Draw the precomputed arrow paths with scaling and gradient."""
        painter.save()

        scaled_paths = self._paths

        # Apply gradient
        gradient = self._gradient
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)

        for path in scaled_paths:
            painter.drawPath(path)

        painter.restore()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.save()
        painter.setTransform(QTransform().scale(self._flip, 1).rotate(self._angle) * self._transform)
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

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self._grayed_out = not enabled
        if enabled:
            self.start()
        else:
            self.stop()
        self.buildGradient()
        self.update()

    def setDisabled(self, disabled):
        self.setEnabled(not disabled)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    widget = WaitingArrowSpinnerWidget()
    widget.resize(400, 400)
    widget.start()
    widget.show()
    sys.exit(app.exec())