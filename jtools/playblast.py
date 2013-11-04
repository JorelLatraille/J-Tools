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
from PythonQt.QtCore import QRegExp, Qt

version = "0.01"

lighting_mode_list = ['Flat', 'Basic', 'Full']
color_depth_list = ['8bit (Byte)', '16bit (Half)', '32bit (Float)']
size_list = ['2048 x 2048', '4096 x 4096', '8192 x 8192', '16384 x 16384', '32768 x 32768']
image_file_types = ['.bmp', '.jpg', '.jpeg', '.png', '.ppm', '.psd', '.tga', '.tif', '.tiff', '.xbm', '.xpm', '.exr']

# ------------------------------------------------------------------------------
class playblastGUI(QDialog):
    "Create ImportImagesGUI"
    def __init__(self, parent=None):
        super(playblastGUI, self).__init__(parent)

        #Set title and create the major layouts
        self.setWindowTitle('Playblast')
        main_layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        middle_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()
        final_layout = QVBoxLayout()

        #Create time widgets and hook them up
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

        #Create padding widgets and hook them up
        padding_label = QLabel('Frame padding:')
        punctuation_re = QRegExp(r"[0-4]") #Force the line edit to only be able to enter numbers from 0-4
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

        #Create grid layout called time_layout
        time_layout = QGridLayout()

        #Add time widgets to time_layout
        time_layout.addWidget(time_label, 0, 0, Qt.AlignRight)
        time_layout.addWidget(self.time_slider, 0, 1, Qt.AlignCenter)
        time_layout.addWidget(self.start_end, 0, 2, Qt.AlignLeft)
        time_layout.addWidget(start_label, 1, 0, Qt.AlignRight)
        time_layout.addWidget(self.start_time, 1, 1, Qt.AlignCenter)
        time_layout.addWidget(end_label, 2, 0, Qt.AlignRight)
        time_layout.addWidget(self.end_time, 2, 1, Qt.AlignCenter)
        time_layout.addWidget(padding_label, 3, 0, Qt.AlignRight)
        time_layout.addWidget(self.frame_padding, 3, 1, Qt.AlignCenter)
        time_layout.addWidget(self.padding_slider, 3, 2, Qt.AlignLeft)
        time_layout.setColumnStretch(0, 2)
        time_layout.setColumnStretch(1, 2)
        time_layout.setColumnStretch(2, 2)
        time_layout.setColumnStretch(3, 2)

        #Add time_layout to time_group (Group Box) widget and add the widget to top_layout
        time_group = QGroupBox()
        time_group.setLayout(time_layout)
        top_layout.addWidget(time_group)

        #Widgets for unproject settings
        clamp_label = QLabel('Clamp:')
        self.clamp = QCheckBox()
        self.original_clamp = mari.projectors.current().clampColors()
        self.clamp.setChecked(self.original_clamp)
        shader_used_label = QLabel('Shader Used:')
        self.shader_used = QComboBox()
        shader_list = mari.projectors.current().useShaderList()
        self.original_shader = mari.projectors.current().useShader()
        for shader in shader_list:
            self.shader_used.addItem(shader)
        self.shader_used.setCurrentIndex(self.shader_used.findText(self.original_shader))
        lighting_mode_label = QLabel('Lighting mode:')
        self.lighting_mode = QComboBox()
        self.original_mode = mari.projectors.current().lightingMode()
        for mode in lighting_mode_list:
            self.lighting_mode.addItem(mode)
        self.lighting_mode.setCurrentIndex(self.original_mode)
        color_depth_label = QLabel('Color depth:')
        self.color_depth = QComboBox()
        self.original_depth = mari.projectors.current().bitDepth()
        for depth in color_depth_list:
            self.color_depth.addItem(depth)
        self.color_depth.setCurrentIndex(self.color_depth.findText(([bit for bit in color_depth_list if str(self.original_depth) in bit])[0]))
        size_label = QLabel('Size:')
        self._size = QComboBox()
        self.original_size = mari.projectors.current().width()
        for size in size_list:
            self._size.addItem(size)
        self._size.setCurrentIndex(self._size.findText(([bit for bit in size_list if str(self.original_size) in bit])[0]))

        #Create unproject_layout
        unproject_layout = QGridLayout()

        unproject_layout.addWidget(clamp_label, 0, 0, Qt.AlignRight)
        unproject_layout.addWidget(self.clamp, 0, 1, Qt.AlignLeft)
        unproject_layout.addWidget(shader_used_label, 1, 0, Qt.AlignRight)
        unproject_layout.addWidget(self.shader_used, 1, 1, Qt.AlignLeft)
        unproject_layout.addWidget(lighting_mode_label, 2, 0, Qt.AlignRight)
        unproject_layout.addWidget(self.lighting_mode, 2, 1, Qt.AlignLeft)
        unproject_layout.addWidget(color_depth_label, 3, 0, Qt.AlignRight)
        unproject_layout.addWidget(self.color_depth, 3, 1, Qt.AlignLeft)
        unproject_layout.addWidget(size_label, 4, 0, Qt.AlignRight)
        unproject_layout.addWidget(self._size, 4, 1, Qt.AlignLeft)
        unproject_layout.setColumnStretch(1, 1)
        unproject_layout.setColumnStretch(2, 1)
        unproject_layout.setColumnStretch(3, 1)
        unproject_layout.setColumnStretch(4, 1)

        #Add unproject_layout to middle_layout
        middle_layout.addLayout(unproject_layout)

        #Add path line input and button
        path_label = QLabel('Path:')
        self.path = QLineEdit()
        path = os.path.abspath(mari.resources.path(mari.resources.DEFAULT_EXPORT)) #Get the default export directory from Mari
        template = mari.projectors.current().name() + '.$FRAME.tif'
        self.export_path_template = os.path.join(path, template)
        self.path.setText(self.export_path_template)
        path_pixmap = QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QIcon(path_pixmap)
        path_button = QPushButton(icon, "")
        path_button.connect('clicked()', lambda: self._getPath())

        #Create path_layout
        path_layout = QHBoxLayout()

        #Add widgets to path_layout
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path)
        path_layout.addWidget(path_button)

        #Add path_layout to middle_layout
        middle_layout.addLayout(path_layout)

        #Add OK/Cancel buttons
        ok_button = QPushButton("&Playblast")
        cancel_button = QPushButton("Cancel")

        #Hook up OK/Cancel buttons
        ok_button.connect("clicked()", self.accepted)
        cancel_button.connect("clicked()", self.reject)

        #Add buttons to bottom_layout
        bottom_layout.addWidget(ok_button)
        bottom_layout.addWidget(cancel_button)

        #Add layouts to main_group (Group Box) widget and add it to final_layout
        #Then set the GUI layout to final_layout
        main_group = QGroupBox()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_group.setLayout(main_layout)
        final_layout.addWidget(main_group)
        final_layout.addLayout(bottom_layout)
        self.setLayout(final_layout)

    def _timeSliderToggle(self, _bool):
        "Make the time line edit boxes read only depending on which radio button is toggled"
        if _bool:
            self.start_time.setReadOnly(True)
            self.end_time.setReadOnly(True)
        else:
            self.start_time.setReadOnly(False)
            self.end_time.setReadOnly(False)

    def _updateFramePadding(self, _int):
        "Set the text in the frame padding line edit box using the padding slider value"
        self.frame_padding.setText(_int)

    def _updateSliderPosition(self):
        "Set the padding slider value using the text in the frame padding line edit box"
        self.padding_slider.setValue(int(self.frame_padding.text))

    def _getPath(self):
        "Get file path and set the text in path LineEdit widget"
        file_path = mari.utils.misc.getSaveFileName(parent=self, caption='Save As', dir='', filter='', selected_filter=None, options=0, save_filename='playblast.$FRAME.tif')
        if file_path == "":
            return
        else:
            self.path.setText(file_path)

    def _getOriginalClamp(self):
        "Return original clamp setting"
        return self.original_clamp

    def _getCurrentClamp(self):
        "Return original clamp setting"
        return self.clamp

    def _getOriginalShader(self):
        "Return original shader setting"
        return self.original_shader

    def _getCurrentShader(self):
        "Return original shader setting"
        return self.shader_used

    def _getOriginalMode(self):
        "Return original lighting mode"
        return self.original_mode

    def _getCurrentMode(self):
        "Return original lighting mode"
        return self.lighting_mode

    def _getOriginalDepth(self):
        "Return original bit depth setting"
        return self.original_depth

    def _getCurrentDepth(self):
        "Return original bit depth setting"
        return self.color_depth

    def _getOriginalSize(self):
        "Return original size setting"
        return self.original_size

    def _getCurrentSize(self):
        "Return original size setting"
        return self._size

    def accepted(self):
        "Check user settings provided before accepting"
        if self.path.text == '':
            mari.utils.message("Please provide a path and image template, e.g. '%s'" %self.export_path_template)
            return

        image_file_types = ('.bmp', '.jpg', '.jpeg', '.png', '.ppm', '.psd', '.tga', '.tif', '.tiff', '.xbm', '.xpm', '.exr')
        path_template = self.path.text
        if not os.path.exists(os.path.split(path_template)[0]):
            make_dir = makeDirGUI(os.path.split(path_template)[0])
            if not make_dir.exec_():
                return
        if not '$FRAME' in os.path.split(path_template)[1]:
            mari.utils.message("Please include the $FRAME token in template, e.g. '%s'" %self.export_path_template)
            return
        if not path_template.endswith(image_file_types):
            mari.utils.message("File type is not supported: '%s'" %(os.path.split(path_template)[1]))
            return

        self.accept()

# ------------------------------------------------------------------------------
class makeDirGUI(QDialog):
    "Create ImportImagesGUI"
    def __init__(self, path, parent=None):
        super(makeDirGUI, self).__init__(parent)

        #Set title and create the major layouts
        self.path = path
        self.setModal(True)
        self.setWindowTitle('Make Directory')
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        text = QLabel("Path does not exist '%s' make path?" %self.path)
        create = QPushButton('Create')
        cancel = QPushButton('Cancel')
        create.connect('clicked()', self.accepted)
        cancel.connect('clicked()', self.reject)

        main_layout.addWidget(text)
        button_layout.addWidget(create)
        button_layout.addWidget(cancel)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def accepted(self):
        "Try to make the directory"
        rejected = False
        try:
            os.mkdir(self.path)
        except:
            mari.utils.message("Unable to create path '%s'" %self.path)
            rejected = True
        if rejected:
            self.reject()
        else:
            self.accept()

# ------------------------------------------------------------------------------
def playblast():

    if not isProjectSuitable():
        return

    #Create dialog and return inputs
    dialog = playblastGUI()
    if dialog.exec_():
        pass

    original_clamp = dialog._getOriginalClamp
    clamp = dialog._getCurrentClamp
    original_shader = dialog._getOriginalShader
    shader = dialog._getCurrentShader
    original_mode = dialog._getOriginalMode
    lighting_mode = dialog._getCurrentMode
    original_depth = dialog._getOriginalDepth
    color_depth = dialog._getCurrentDepth
    original_size = dialog._getOriginalSize
    _size = dialog._getCurrentSize

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