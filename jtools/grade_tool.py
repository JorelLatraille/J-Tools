# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Grade tool
# coding: utf-8
# Written by Jorel Latraille
# ------------------------------------------------------------------------------
# DISCLAIMER & TERMS OF USE:
#
# Copyright (c) The Foundry 2014.
# All rights reserved.
#
# This software is provided as-is with use in commercial projects permitted.
# Redistribution in commercial projects is also permitted
# provided that the above copyright notice and this paragraph are
# duplicated in accompanying documentation,
# and acknowledge that the software was developed
# by The Foundry.  The name of the
# The Foundry may not be used to endorse or promote products derived
# from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

import mari
import PythonQt.QtGui as QtGui
from PythonQt.QtCore import QRegExp, Qt

version = "0.01"

# ------------------------------------------------------------------------------
class GradeToolGUI(QtGui.QDialog):
    "Create GradeToolGUI"
    def __init__(self, parent=None):
        super(GradeToolGUI, self).__init__(parent)

        self.setWindowTitle('Grade Tool')
        main_layout = QtGui.QVBoxLayout()
        blackpoint_layout = QtGui.QHBoxLayout()
        whitepoint_layout = QtGui.QHBoxLayout()
        lift_layout = QtGui.QHBoxLayout()
        gain_layout = QtGui.QHBoxLayout()
        multiply_layout = QtGui.QHBoxLayout()
        offset_layout = QtGui.QHBoxLayout()
        gamma_layout = QtGui.QHBoxLayout()

        punctuation_re_0 = QRegExp(r"-?[0-1]?[.]?\d?\d?") #Force the line edit to only be able to enter the numbers set
        punctuation_re_1 = QRegExp(r"-?[0-1]?[.]?\d?\d?") #Force the line edit to only be able to enter the numbers set
        punctuation_re_2 = QRegExp(r"[0-5]?[.]?\d?\d?") #Force the line edit to only be able to enter the numbers set

        blackpoint_label = QtGui.QLabel('Blackpoint')
        self.blackpoint_line_0 = QtGui.QLineEdit()
        self.blackpoint_line_0.setFixedSize(40,20)
        self.blackpoint_line_1 = QtGui.QLineEdit()
        self.blackpoint_line_1.setFixedSize(40,20)
        self.blackpoint_line_1.setHidden(True)
        self.blackpoint_line_2 = QtGui.QLineEdit()
        self.blackpoint_line_2.setFixedSize(40,20)
        self.blackpoint_line_2.setHidden(True)
        self.blackpoint_line_3 = QtGui.QLineEdit()
        self.blackpoint_line_3.setFixedSize(40,20)
        self.blackpoint_line_3.setHidden(True)
        self.blackpoint_line_4 = QtGui.QLineEdit()
        self.blackpoint_line_4.setFixedSize(40,20)
        self.blackpoint_line_4.setHidden(True)
        self.blackpoint_line_0.setValidator(QtGui.QRegExpValidator(punctuation_re_0, self))
        self.blackpoint_slider = QtGui.QSlider(Qt.Orientation(Qt.Horizontal))
        self.blackpoint_slider.setMinimum(-100)
        self.blackpoint_slider.setMaximum(100)
        self.blackpoint_slider.connect('valueChanged(int)', self._updateBlackpointLine)
        self.blackpoint_line_0.connect('editingFinished()', self._updateBlackpointSlider)
        self.blackpoint_line_0.setText('0.00')
        self.blackpoint_s = QtGui.QPushButton('S')
        self.blackpoint_s.setFixedSize(20,20)
        self.blackpoint_s.connect('clicked()', lambda: _updateInput(self.blackpoint_s, self.blackpoint_line_0, self.blackpoint_slider, self.blackpoint_line_1, self.blackpoint_line_2, self.blackpoint_line_3, self.blackpoint_line_4))
        self.blackpoint_r = QtGui.QPushButton('R')
        self.blackpoint_r.setFixedSize(20,20)

        whitepoint_label = QtGui.QLabel('Whitepoint')
        self.whitepoint_line_0 = QtGui.QLineEdit()
        self.whitepoint_line_0.setFixedSize(40,20)
        self.whitepoint_line_1 = QtGui.QLineEdit()
        self.whitepoint_line_1.setFixedSize(40,20)
        self.whitepoint_line_2 = QtGui.QLineEdit()
        self.whitepoint_line_2.setFixedSize(40,20)
        self.whitepoint_line_3 = QtGui.QLineEdit()
        self.whitepoint_line_3.setFixedSize(40,20)
        self.whitepoint_line_4 = QtGui.QLineEdit()
        self.whitepoint_line_4.setFixedSize(40,20)
        self.whitepoint_line_0.setValidator(QtGui.QRegExpValidator(punctuation_re_1, self))
        self.whitepoint_slider = QtGui.QSlider(Qt.Orientation(Qt.Horizontal))
        self.whitepoint_slider.setMinimum(-100)
        self.whitepoint_slider.setMaximum(400)
        self.whitepoint_slider.connect('valueChanged(int)', self._updateWhitepointLine)
        self.whitepoint_line_0.connect('editingFinished()', self._updateWhitepointSlider)
        self.whitepoint_line_0.setText('1.00')
        self.whitepoint_s = QtGui.QPushButton('S')
        self.whitepoint_s.setFixedSize(20,20)
        self.whitepoint_s.connect('clicked()', lambda: _updateInput(self.blackpoint_s, self.blackpoint_line_0, self.blackpoint_slider, self.blackpoint_line_1, self.blackpoint_line_2, self.blackpoint_line_3, self.blackpoint_line_4))
        self.whitepoint_r = QtGui.QPushButton('R')
        self.whitepoint_r.setFixedSize(20,20)
        
        blackpoint_layout.addWidget(blackpoint_label)
        blackpoint_layout.addStretch()
        blackpoint_layout.addWidget(self.blackpoint_line_0)
        blackpoint_layout.addWidget(self.blackpoint_slider)
        blackpoint_layout.addWidget(self.blackpoint_line_1)
        blackpoint_layout.addWidget(self.blackpoint_line_2)
        blackpoint_layout.addWidget(self.blackpoint_line_3)
        blackpoint_layout.addWidget(self.blackpoint_line_4)
        blackpoint_layout.addWidget(self.blackpoint_s)
        blackpoint_layout.addWidget(self.blackpoint_r)
        whitepoint_layout.addWidget(whitepoint_label)
        whitepoint_layout.addStretch()
        whitepoint_layout.addWidget(self.whitepoint_line_0)
        whitepoint_layout.addWidget(self.whitepoint_slider)
        whitepoint_layout.addWidget(self.whitepoint_s)
        whitepoint_layout.addWidget(self.whitepoint_r)

        main_layout.addLayout(blackpoint_layout)
        main_layout.addLayout(whitepoint_layout)
        self.setLayout(main_layout)

    def _updateBlackpointLine(self, _int):
        "Set the text in the frame padding line edit box using the padding slider value"
        self.blackpoint_line_0.setText("%.2f" %float((_int + 0.00) / (100 + 0.00)))

    def _updateBlackpointSlider(self):
        "Set the padding slider value using the text in the frame padding line edit box"
        self.blackpoint_slider.setValue(int(float(self.blackpoint_line_0.text)*100))

    def _updateWhitepointLine(self, _int):
        "Set the text in the frame padding line edit box using the padding slider value"
        self.whitepoint_line_0.setText("%.2f" %float((_int + 0.00) / (100 + 0.00)))

    def _updateWhitepointSlider(self):
        "Set the padding slider value using the text in the frame padding line edit box"
        self.whitepoint_slider.setValue(int(float(self.whitepoint_line_0.text)*100))

# ------------------------------------------------------------------------------
def _updateInput(button_s, line_0, slider, line_1, line_2, line_3, line_4):
    print button_s, line_0, slider, line_1, line_2, line_3, line_4
    _bool = not button_s.isFlat()
    button_s.setFlat(_bool)
    line_0.setHidden(_bool)
    slider.setHidden(_bool)
    line_1.setHidden(not _bool)
    line_2.setHidden(not _bool)
    line_3.setHidden(not _bool)
    line_4.setHidden(not _bool)

# ------------------------------------------------------------------------------
def gradeTool():

	dialog = GradeToolGUI()
	if dialog.exec_():
		pass

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    gradeTool()