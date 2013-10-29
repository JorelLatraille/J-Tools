# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Playblast uses the timeline to unproject from the current projector
# coding: utf-8
# Written by Jorel Latraille
# ------------------------------------------------------------------------------
# DISCLAIMER & TERMS OF USE:
#
# Copyright (c) The Foundry 2013.
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

import mari, os
from PythonQt.QtGui import *
from PythonQt.QtCore import QRegExp

version = "0.01"

image_file_types = ['.bmp', '.jpg', '.jpeg', '.png', '.ppm', '.psd', '.tga', '.tif', '.tiff', '.xbm', '.xpm', '.exr']

# ------------------------------------------------------------------------------
class playblastGUI(QDialog):
    "Create ImportImagesGUI"
    def __init__(self, parent=None):
        super(playblastGUI, self).__init__(parent)

        self.setWindowTitle('Playblast')
        main_layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        middle_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()

        time_label = QLabel('Time range:')
        self.time_slider = QRadioButton('Time Slider')
        self.start_end = QRadioButton('Start/End')
        start_label = QLabel('Start time:')
        end_label = QLabel('End time:')
        self.start_time = QLineEdit()
        self.start_time.setReadOnly(True)
        self.start_time.setText('0')
        self.end_time = QLineEdit()
        self.end_time.setReadOnly(True)
        self.end_time.setText('10')
        self.time_slider.connect('toggled(bool)', self._timeSliderToggle)
        self.time_slider.setChecked(True)

        padding_label = QLabel('Frame padding:')
        punctuation_re = QRegExp(r"[0-4]")
        self.frame_padding = QLineEdit()
        self.frame_padding.setValidator(QRegExpValidator(punctuation_re, self))
        self.padding_slider = QSlider(Qt.Orientation(Qt.Horizontal))
        self.padding_slider.setMinimum(0)
        self.padding_slider.setMaximum(4)
        self.padding_slider.setTickInterval(1)
        self.padding_slider.setTickPosition(0)
        self.padding_slider.connect('valueChanged(int)', self._updateFramePadding)      
        self.padding_slider.setValue(4)
        self.frame_padding.connect('editingFinished()', self._updateSliderPosition)

        time_layout = QGridLayout()

        time_layout.addWidget(time_label, 0, 0)
        time_layout.addWidget(self.time_slider, 0, 1)
        time_layout.addWidget(self.start_end, 0, 2)
        time_layout.addWidget(start_label, 1, 0)
        time_layout.addWidget(self.start_time, 1, 1)
        time_layout.addWidget(end_label, 2, 0)
        time_layout.addWidget(self.end_time, 2, 1)
        time_layout.addWidget(padding_label, 3, 0)
        time_layout.addWidget(self.frame_padding, 3, 1)
        time_layout.addWidget(self.padding_slider, 3, 2)

        top_layout.addLayout(time_layout)

        #Add path line input and button
        path_label = QLabel('Path:')
        self.path = QLineEdit()
        path_pixmap = QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QIcon(path_pixmap)
        path_button = QPushButton(icon, "")
        path_button.connect("clicked()", lambda: self._getPath())

        path_layout = QHBoxLayout()

        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path)
        path_layout.addWidget(path_button)

        #Add OK/Cancel buttons
        ok_button = QPushButton("&Playblast")
        cancel_button = QPushButton("Cancel")

        ok_button.connect("clicked()", lambda: self.accepted())
        cancel_button.connect("clicked()", self.reject)

        bottom_layout.addWidget(ok_button)
        bottom_layout.addWidget(cancel_button)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(path_layout)
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

    def _timeSliderToggle(self, _bool):
        if _bool:
            self.start_time.setReadOnly(True)
            self.end_time.setReadOnly(True)
        else:
            self.start_time.setReadOnly(False)
            self.end_time.setReadOnly(False)

    def _updateFramePadding(self, _int):
        self.frame_padding.setText(_int)

    def _updateSliderPosition(self):
        self.padding_slider.setValue(int(self.frame_padding.text))

    def _getPath(self):
        "Get file path and set the text in path LineEdit widget"
        file_path = mari.utils.misc.getSaveFileName(parent=self, caption='Save As', dir='', filter='', selected_filter=None, options=0, save_filename='playblast.$FRAME.tif')
        if file_path == "":
            return
        else:
            self.path.setText(file_path)

# ------------------------------------------------------------------------------
def playblast():

    if not isProjectSuitable():
        return

    #Create dialog and return inputs
    dialog = playblastGUI()
    if dialog.exec_():
        pass

        # projector = mari.projectors.list()[0]
        # path = mari.utils.misc.getSaveFileName(parent=None, caption='Playblast', dir='', filter='', selected_filter=None, options=0, save_filename='')
        # if path == '':
        #   return
        # else:
        #   path = os.path.abspath(path)

        # frame_range = mari.clock.frameCount()
        # for frame in range(frame_range):
        #   projector.unprojectToFile(path + '.%s.tif' %(str(frame)))
        #   mari.clock.stepForward()

# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state."
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
    
        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False

        return True
    
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    playblast()