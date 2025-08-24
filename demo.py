#!/usr/bin/python

"""
The MIT License (MIT)

Copyright (c) 2016 Luca Weiss
Copyright (c) 2025 Graham Cole

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys

# from PyQt6.QtCore import *
from PyQt6.QtCore import Qt

# from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import (QApplication, QWidget, QCheckBox, QDoubleSpinBox,
    QSpinBox, QPushButton, QGridLayout, QGroupBox, QHBoxLayout, QSizePolicy,
    QLabel
)

from waitingarrowspinnerwidget import WaitingArrowSpinnerWidget

class Demo(QWidget):
    sb_roundness = None
    sb_gap_ratio = None
    sb_arrow_count = None
    sb_line_length = None
    sb_line_width = None
    sb_inner_radius = None
    sb_rev_s = None

    btn_start = None
    btn_stop = None
    btn_pick_color = None

    spinner = None

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        groupbox1 = QGroupBox()
        groupbox1_layout = QHBoxLayout()
        groupbox2 = QGroupBox()
        groupbox2_layout = QGridLayout()
        button_hbox = QHBoxLayout()
        self.setLayout(grid)
        self.setWindowTitle("WaitingArrowSpinner Demo")
        self.setWindowFlags(Qt.WindowType.Dialog)

        # SPINNER
        self.spinner = WaitingArrowSpinnerWidget(self)
        self.spinner.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        # Spinboxes
        self.sb_arrow_count = QSpinBox()
        self.sb_gap_ratio = QDoubleSpinBox()
        self.sb_thickness_ratio = QDoubleSpinBox()
        self.sb_arrow_width_ratio = QDoubleSpinBox()
        self.sb_arrow_length_ratio = QDoubleSpinBox()
        self.sb_barb_indent_ratio = QDoubleSpinBox()
        self.sb_line_length = QDoubleSpinBox()
        self.sb_line_width = QDoubleSpinBox()
        self.sb_inner_radius = QDoubleSpinBox()
        self.sb_rev_s = QDoubleSpinBox()
        self.sb_frame_rate = QSpinBox()
        self.sb_clockwise = QCheckBox()
        self.sb_enabled = QCheckBox()

        # set spinbox default values
        self.sb_arrow_count.setValue(3)
        self.sb_arrow_count.setRange(1, 20)
        self.sb_gap_ratio.setValue(0.2)
        self.sb_gap_ratio.setRange(0.001, 1.0)
        self.sb_gap_ratio.setSingleStep(0.001)
        self.sb_gap_ratio.setDecimals(3)
        self.sb_thickness_ratio.setValue(0.1)  # Example default
        self.sb_thickness_ratio.setRange(0.0, 1.0)
        self.sb_thickness_ratio.setSingleStep(0.01)
        self.sb_thickness_ratio.setDecimals(3)
        self.sb_arrow_width_ratio.setValue(0.1)  # Example default
        self.sb_arrow_width_ratio.setRange(0.0, 1.0)
        self.sb_arrow_width_ratio.setSingleStep(0.01)
        self.sb_arrow_width_ratio.setDecimals(3)
        self.sb_arrow_length_ratio.setValue(0.2)  # Example default
        self.sb_arrow_length_ratio.setRange(0.0, 1.0)
        self.sb_arrow_length_ratio.setSingleStep(0.01)
        self.sb_arrow_length_ratio.setDecimals(3)
        self.sb_barb_indent_ratio.setValue(0.05)  # Example default
        self.sb_barb_indent_ratio.setRange(0.0, 1.0)
        self.sb_barb_indent_ratio.setSingleStep(0.01)
        self.sb_barb_indent_ratio.setDecimals(3)
        self.sb_rev_s.setValue(0.4)
        self.sb_rev_s.setRange(0.1, 10.0)
        self.sb_rev_s.setSingleStep(0.1)
        self.sb_rev_s.setDecimals(2)
        self.sb_frame_rate.setValue(60)
        self.sb_frame_rate.setRange(1, 240)
        self.sb_clockwise.setChecked(True)
        self.sb_enabled.setChecked(True)

        # Buttons
        self.btn_start = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.btn_pick_color = QPushButton("Pick Color")

        # Connects
        self.sb_arrow_count.valueChanged.connect(self.set_arrow_count)
        self.sb_gap_ratio.valueChanged.connect(self.set_gap_ratio)
        self.sb_thickness_ratio.valueChanged.connect(self.set_thickness_ratio)
        self.sb_arrow_width_ratio.valueChanged.connect(self.set_arrow_width_ratio)
        self.sb_arrow_length_ratio.valueChanged.connect(self.set_arrow_length_ratio)
        self.sb_barb_indent_ratio.valueChanged.connect(self.set_barb_indent_ratio)
        self.sb_rev_s.valueChanged.connect(self.set_rev_s)
        self.sb_frame_rate.valueChanged.connect(self.set_frame_rate)
        self.sb_clockwise.stateChanged.connect(self.set_clockwise)
        self.sb_enabled.stateChanged.connect(self.set_enabled)

        self.btn_start.clicked.connect(self.spinner_start)
        self.btn_stop.clicked.connect(self.spinner_stop)
        self.btn_pick_color.clicked.connect(self.show_color_picker)

        # Layout adds
        groupbox1_layout.addWidget(self.spinner)
        groupbox1.setLayout(groupbox1_layout)
        groupbox2_layout.addWidget(QLabel("Arrow Count:"), 1, 1)
        groupbox2_layout.addWidget(self.sb_arrow_count, 1, 2)
        groupbox2_layout.addWidget(QLabel("Gap Ratio:"), 2, 1)
        groupbox2_layout.addWidget(self.sb_gap_ratio, 2, 2)
        groupbox2_layout.addWidget(QLabel("Thickness Ratio:"), 3, 1)
        groupbox2_layout.addWidget(self.sb_thickness_ratio, 3, 2)
        groupbox2_layout.addWidget(QLabel("Arrow Width Ratio:"), 4, 1)
        groupbox2_layout.addWidget(self.sb_arrow_width_ratio, 4, 2)
        groupbox2_layout.addWidget(QLabel("Arrow Length Ratio:"), 5, 1)
        groupbox2_layout.addWidget(self.sb_arrow_length_ratio, 5, 2)
        groupbox2_layout.addWidget(QLabel("Barb Indent Ratio:"), 6, 1)
        groupbox2_layout.addWidget(self.sb_barb_indent_ratio, 6, 2)
        groupbox2_layout.addWidget(QLabel("Rev/s:"), 7, 1)
        groupbox2_layout.addWidget(self.sb_rev_s, 7, 2)
        groupbox2_layout.addWidget(QLabel("Frames/s:"), 8, 1)
        groupbox2_layout.addWidget(self.sb_frame_rate, 8, 2)
        groupbox2_layout.addWidget(QLabel("Clockwise:"), 9, 1)
        groupbox2_layout.addWidget(self.sb_clockwise, 9, 2)
        groupbox2_layout.addWidget(QLabel("Enabled:"), 10, 1)
        groupbox2_layout.addWidget(self.sb_enabled, 10, 2)


        groupbox2.setLayout(groupbox2_layout)

        button_hbox.addWidget(self.btn_start)
        button_hbox.addWidget(self.btn_stop)
        button_hbox.addWidget(self.btn_pick_color)
        grid.addWidget(groupbox1, *(1, 1))
        grid.addWidget(groupbox2, *(1, 2))
        grid.layout().addLayout(button_hbox, *(2, 1))

        self.spinner.start()
        self.show()

    def set_arrow_count(self):
        self.spinner.setArrowCount(self.sb_arrow_count.value())

    def set_gap_ratio(self):
        self.spinner.setGapRatio(self.sb_gap_ratio.value())

    def set_thickness_ratio(self):
        self.spinner.setThicknessRatio(self.sb_thickness_ratio.value())
        self.spinner.update()  # Trigger repaint

    def set_arrow_width_ratio(self):
        self.spinner.setArrowWidthRatio(self.sb_arrow_width_ratio.value())
        self.spinner.update()

    def set_arrow_length_ratio(self):
        self.spinner.setArrowLengthRatio(self.sb_arrow_length_ratio.value())  # Fixed typo
        self.spinner.update()

    def set_barb_indent_ratio(self):
        self.spinner.setBarbIndentRatio(self.sb_barb_indent_ratio.value())
        self.spinner.update()

    def set_rev_s(self):
        self.spinner.setRevolutionsPerSecond(self.sb_rev_s.value())

    def set_frame_rate(self):
        self.spinner.setFrameRate(self.sb_frame_rate.value())

    def set_clockwise(self):
        self.spinner.setClockwise(self.sb_clockwise.isChecked())

    def set_enabled(self):
        # self.spinner.setEnabled(self.sb_enabled.isChecked())
        self.spinner.setDisabled(not self.sb_enabled.isChecked())

    def spinner_start(self):
        self.spinner.start()

    def spinner_stop(self):
        self.spinner.stop()

    def show_color_picker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.spinner.setColor(color)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Demo()
    sys.exit(app.exec())
