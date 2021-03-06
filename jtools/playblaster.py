# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Playblast uses the timeline to unproject from the current projector
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

import mari, os
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

version = "0.04"

lighting_mode_list = ['Flat', 'Basic', 'Full']
color_depth_list = ['8bit (Byte)', '16bit (Half)', '32bit (Float)']
size_list = ['2048 x 2048', '4096 x 4096', '8192 x 8192', '16384 x 16384', '32768 x 32768']

# ------------------------------------------------------------------------------
class playblastUI(QtGui.QDialog):
    "Create ImportImagesUI"
    def __init__(self, parent=None):
        super(playblastUI, self).__init__(parent)

        #Set title and create the major layouts
        self.setWindowTitle('Playblast')
        main_layout = QtGui.QVBoxLayout()
        top_layout = QtGui.QVBoxLayout()
        middle_layout = QtGui.QVBoxLayout()
        bottom_layout = QtGui.QHBoxLayout()
        final_layout = QtGui.QVBoxLayout()

        #Create time widgets and hook them up
        time_label = QtGui.QLabel('Time range:')
        self.time_slider = QtGui.QRadioButton('Time Slider')
        self.start_end = QtGui.QRadioButton('Start/End')
        self.start_label = QtGui.QLabel('Start time:')
        self.end_label = QtGui.QLabel('End time:')
        self.start_time = QtGui.QLineEdit()
        self.original_start_time = mari.clock.startFrame()
        self.start_time.setText(str(self.original_start_time))
        self.end_time = QtGui.QLineEdit()
        self.original_end_time = mari.clock.stopFrame()
        self.end_time.setText(str(self.original_end_time))
        self.time_slider.toggled.connect(self._timeSliderToggle)
        self.time_slider.setChecked(True)

        #Create padding widgets and hook them up
        padding_label = QtGui.QLabel('Frame padding:')
        punctuation_re = QtCore.QRegExp(r"[0-4]") #Force the line edit to only be able to enter numbers from 0-4
        self.frame_padding = QtGui.QLineEdit()
        self.frame_padding.setValidator(QtGui.QRegExpValidator(punctuation_re, self))
        self.padding_slider = QtGui.QSlider(QtCore.Qt.Orientation(QtCore.Qt.Horizontal))
        self.padding_slider.setMinimum(0)
        self.padding_slider.setMaximum(4)
        self.padding_slider.setTickInterval(1)
        self.padding_slider.setTickPosition(QtGui.QSlider.NoTicks)
        self.padding_slider.valueChanged.connect(self._updateFramePadding)      
        self.padding_slider.setValue(4)
        self.frame_padding.editingFinished.connect(self._updateSliderPosition)

        #Create grid layout called time_layout
        time_layout = QtGui.QGridLayout()

        #Add time widgets to time_layout
        time_layout.addWidget(time_label, 0, 0, QtCore.Qt.AlignRight)
        time_layout.addWidget(self.time_slider, 0, 1, QtCore.Qt.AlignCenter)
        time_layout.addWidget(self.start_end, 0, 2, QtCore.Qt.AlignLeft)
        time_layout.addWidget(self.start_label, 1, 0, QtCore.Qt.AlignRight)
        time_layout.addWidget(self.start_time, 1, 1, QtCore.Qt.AlignCenter)
        time_layout.addWidget(self.end_label, 2, 0, QtCore.Qt.AlignRight)
        time_layout.addWidget(self.end_time, 2, 1, QtCore.Qt.AlignCenter)
        time_layout.addWidget(padding_label, 3, 0, QtCore.Qt.AlignRight)
        time_layout.addWidget(self.frame_padding, 3, 1, QtCore.Qt.AlignCenter)
        time_layout.addWidget(self.padding_slider, 3, 2, QtCore.Qt.AlignLeft)
        time_layout.setColumnStretch(0, 2)
        time_layout.setColumnStretch(1, 2)
        time_layout.setColumnStretch(2, 2)
        time_layout.setColumnStretch(3, 2)

        #Add time_layout to time_group (Group Box) widget and add the widget to top_layout
        time_group = QtGui.QGroupBox()
        time_group.setLayout(time_layout)
        top_layout.addWidget(time_group)

        #Widgets for unproject settings
        clamp_label = QtGui.QLabel('Clamp:')
        self.clamp = QtGui.QCheckBox()
        self.original_clamp = mari.projectors.current().clampColors()
        self.clamp.setChecked(self.original_clamp)
        shader_used_label = QtGui.QLabel('Shader Used:')
        self.shader_used = QtGui.QComboBox()
        shader_list = mari.projectors.current().useShaderList()
        self.original_shader = mari.projectors.current().useShader()
        for shader in shader_list:
            self.shader_used.addItem(shader)
        self.shader_used.setCurrentIndex(self.shader_used.findText(self.original_shader))
        lighting_mode_label = QtGui.QLabel('Lighting mode:')
        self.lighting_mode = QtGui.QComboBox()
        self.original_mode = mari.projectors.current().lightingMode()
        for mode in lighting_mode_list:
            self.lighting_mode.addItem(mode)
        self.lighting_mode.setCurrentIndex(self.original_mode)
        color_depth_label = QtGui.QLabel('Color depth:')
        self.color_depth = QtGui.QComboBox()
        self.original_depth = mari.projectors.current().bitDepth()
        for depth in color_depth_list:
            self.color_depth.addItem(depth)
        self.color_depth.setCurrentIndex(self.color_depth.findText(([bit for bit in color_depth_list if str(self.original_depth) in bit])[0]))
        size_label = QtGui.QLabel('Size:')
        self._size = QtGui.QComboBox()
        self.original_size = mari.projectors.current().width()
        for size in size_list:
            self._size.addItem(size)
        self._size.setCurrentIndex(self._size.findText(([bit for bit in size_list if str(self.original_size) in bit])[0]))

        #Create unproject_layout
        unproject_layout = QtGui.QGridLayout()

        unproject_layout.addWidget(clamp_label, 0, 0, QtCore.Qt.AlignRight)
        unproject_layout.addWidget(self.clamp, 0, 1, QtCore.Qt.AlignLeft)
        unproject_layout.addWidget(shader_used_label, 1, 0, QtCore.Qt.AlignRight)
        unproject_layout.addWidget(self.shader_used, 1, 1, QtCore.Qt.AlignLeft)
        unproject_layout.addWidget(lighting_mode_label, 2, 0, QtCore.Qt.AlignRight)
        unproject_layout.addWidget(self.lighting_mode, 2, 1, QtCore.Qt.AlignLeft)
        unproject_layout.addWidget(color_depth_label, 3, 0, QtCore.Qt.AlignRight)
        unproject_layout.addWidget(self.color_depth, 3, 1, QtCore.Qt.AlignLeft)
        unproject_layout.addWidget(size_label, 4, 0, QtCore.Qt.AlignRight)
        unproject_layout.addWidget(self._size, 4, 1, QtCore.Qt.AlignLeft)
        unproject_layout.setColumnStretch(1, 1)
        unproject_layout.setColumnStretch(2, 1)
        unproject_layout.setColumnStretch(3, 1)
        unproject_layout.setColumnStretch(4, 1)

        #Add unproject_layout to middle_layout
        middle_layout.addLayout(unproject_layout)

        #Add path line input and button
        path_label = QtGui.QLabel('Path:')
        self.path = QtGui.QLineEdit()
        if mari.projectors.current().exportPath() == '':
            path = os.path.abspath(mari.resources.path(mari.resources.DEFAULT_EXPORT)) #Get the default export directory from Mari
        else:
            path = mari.projectors.current().exportPath()
        template = mari.projectors.current().name() + '.$FRAME.tif'
        self.export_path_template = os.path.join(path, template)
        self.path.setText(self.export_path_template)
        path_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QtGui.QIcon(path_pixmap)
        path_button = QtGui.QPushButton(icon, "")
        path_button.clicked.connect(self._getSavePath)

        #Create path_layout
        path_layout = QtGui.QHBoxLayout()

        #Add widgets to path_layout
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path)
        path_layout.addWidget(path_button)

        #Add path_layout to middle_layout
        middle_layout.addLayout(path_layout)

        #Add OK/Cancel buttons
        ok_button = QtGui.QPushButton("&Playblast")
        cancel_button = QtGui.QPushButton("Cancel")

        #Hook up OK/Cancel buttons
        ok_button.clicked.connect(self.accepting)
        cancel_button.clicked.connect(self.reject)

        #Add buttons to bottom_layout
        bottom_layout.addWidget(ok_button)
        bottom_layout.addWidget(cancel_button)

        #Add layouts to main_group (Group Box) widget and add it to final_layout
        #Then set the UI layout to final_layout
        main_group = QtGui.QGroupBox()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_group.setLayout(main_layout)
        final_layout.addWidget(main_group)
        final_layout.addLayout(bottom_layout)
        self.setLayout(final_layout)

    def _timeSliderToggle(self, _bool):
        "Make the time line edit boxes hidden depending on which radio button is toggled"
        if _bool:
            self.start_label.setHidden(True)
            self.start_time.setHidden(True)
            self.end_label.setHidden(True)
            self.end_time.setHidden(True)
        else:
            self.start_label.setHidden(False)
            self.start_time.setHidden(False)
            self.end_label.setHidden(False)
            self.end_time.setHidden(False)

    def _updateFramePadding(self, _int):
        "Set the text in the frame padding line edit box using the padding slider value"
        self.frame_padding.setText(str(_int))

    def _updateSliderPosition(self):
        "Set the padding slider value using the text in the frame padding line edit box"
        self.padding_slider.setValue(int(self.frame_padding.text()))

    def _getSavePath(self):
        "Get file path and set the text in path LineEdit widget"
        file_path = mari.utils.misc.getSaveFileName(
            parent=None,
            caption='Save As',
            dir='',
            filter='',
            selected_filter=None,
            options=0,
            save_filename='playblast.$FRAME.tif'
        )
        if file_path == "":
            return
        else:
            self.path.setText(file_path)

    def accepting(self):
        "Check user settings provided before accepting"
        if self.path.text() == '':
            mari.utils.message("Please provide a path and image template, e.g. '%s'" %self.export_path_template)
            return

        file_types = ['.' + format for format in mari.images.supportedWriteFormats()]
        path_template = self.path.text()
        if not os.path.exists(os.path.split(path_template)[0]):
            make_dir = makeDirUI(os.path.split(path_template)[0])
            if not make_dir.exec_():
                return
        if not '$FRAME' in os.path.split(path_template)[1]:
            mari.utils.message("Please include the $FRAME token in template, e.g. '%s'" %self.export_path_template)
            return
        if not path_template.endswith(tuple(file_types)):
            mari.utils.message("File type is not supported: '%s'" %(os.path.split(path_template)[1]))
            return

        self.accept()

    def _getTime(self):
        "Return True if time_slider is checked, else False"
        if self.time_slider.isChecked():
            return True #True to use time slider
        else:
            return False #False to use start end time

    def _getOriginalStartEndTime(self):
        "Return original start and end times as a list"
        return [self.original_start_time, self.original_end_time]

    def _getStartEndTime(self):
        "Return start and end times as a list"
        return [self.start_time.text(), self.end_time.text()]

    def _getFramePadding(self):
        "Return frame padding number as int"
        return int(self.frame_padding.text())

    def _getOriginalClamp(self):
        "Return original clamp setting"
        return self.original_clamp

    def _getClamp(self):
        "Return clamp setting"
        return self.clamp.isChecked()

    def _getOriginalShader(self):
        "Return original shader setting"
        return self.original_shader

    def _getShader(self):
        "Return shader setting"
        return self.shader_used.currentText()

    def _getOriginalMode(self):
        "Return original lighting mode"
        return self.original_mode

    def _getLightingMode(self):
        "Return lighting mode"
        return self.lighting_mode.currentIndex()

    def _getOriginalDepth(self):
        "Return original bit depth setting"
        return self.original_depth

    def _getColorDepth(self):
        "Return color bit depth setting"
        return self.color_depth.currentText()

    def _getOriginalSize(self):
        "Return original size setting"
        return self.original_size

    def _getSize(self):
        "Return size setting"
        return self._size.currentText()

    def _getPath(self):
        "Return path"
        return self.path.text()

# ------------------------------------------------------------------------------
class makeDirUI(QtGui.QDialog):
    "Create ImportImagesUI"
    def __init__(self, path, parent=None):
        super(makeDirUI, self).__init__(parent)

        #Set title and create the major layouts
        self.path = path
        self.setModal(True)
        self.setWindowTitle('Make Directory')
        main_layout = QtGui.QVBoxLayout()
        button_layout = QtGui.QHBoxLayout()

        text = QtGui.QLabel("Path does not exist '%s' make path?" %self.path)
        create = QtGui.QPushButton('Create')
        cancel = QtGui.QPushButton('Cancel')
        create.clicked.connect(self.accepted)
        cancel.clicked.connect(self.reject)

        main_layout.addWidget(text)
        button_layout.addWidget(create)
        button_layout.addWidget(cancel)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def accepted(self):
        "Try to make the directory"
        rejected = False
        try:
            os.makedirs(self.path)
        except:
            mari.utils.message("Unable to create path '%s'" %self.path)
            rejected = True
        if rejected:
            self.reject()
        else:
            self.accept()

# ------------------------------------------------------------------------------
def playblast():
    "Playblast uses the timeline to unproject from the current projector"
    if not isProjectSuitable():
        return

    #Create dialog and return inputs
    dialog = playblastUI()
    if dialog.exec_():
        #Get all inputs/settings from dialog
        time = dialog._getTime()
        original_start_end_time = dialog._getOriginalStartEndTime()
        start_end_time = dialog._getStartEndTime()
        frame_padding = dialog._getFramePadding()
        original_clamp = dialog._getOriginalClamp()
        clamp = dialog._getClamp()
        original_shader = dialog._getOriginalShader()
        shader = dialog._getShader()
        original_mode = dialog._getOriginalMode()
        lighting_mode = dialog._getLightingMode()
        original_depth = dialog._getOriginalDepth()
        color_depth = dialog._getColorDepth()
        original_size = dialog._getOriginalSize()
        _size = dialog._getSize()
        path_template = dialog._getPath()

        #Get the current projector and its export path
        projector = mari.projectors.current()
        original_path = projector.exportPath()

        #Setup the projector using the input/settings from the dialog
        projector.setClampColors(clamp)
        projector.setUseShader(shader)
        projector.setLightingMode(lighting_mode)
        if '8' in color_depth:
            projector.setBitDepth(8)
        elif '16' in color_depth:
            projector.setBitDepth(16)
        else:
            projector.setBitDepth(32)
        size = _size.split('x')
        projector.setSize(int(size[0]), int(size[1]))
        
        #Get the path and template
        path = os.path.split(path_template)[0]
        template = os.path.split(path_template)[1]

        #Throw the export process into a try, just in case writing to disk fails
        #Use the input/settings from the dialog to decide whether to use the current time slider numbers or not
        #Itterate through the frame range and export accordingly, also use zfill to pad the numbers
        try:
            if time:
                mari.clock.rewind()
                for frame in range(int(start_end_time[0]), int(start_end_time[1]) + 1):
                    frame = str(frame).zfill(frame_padding)
                    projector.unprojectToFile(os.path.join(path, template.replace('$FRAME', frame)))
                    mari.clock.stepForward()

            else:
                mari.clock.setFrameRange(int(start_end_time[0]), int(start_end_time[1]))
                mari.clock.rewind()
                for frame in range(int(start_end_time[0]), int(start_end_time[1]) + 1):
                    frame = str(frame).zfill(frame_padding)
                    projector.unprojectToFile(os.path.join(path, template.replace('$FRAME', frame)))
                    mari.clock.stepForward()
        
            #Reset the projector and time slider back to its original settings
            projector.setClampColors(original_clamp)
            projector.setUseShader(original_shader)
            projector.setLightingMode(original_mode)
            projector.setBitDepth(original_depth)
            projector.setSize(original_size, original_size)
            projector.setExportPath(original_path)
            mari.clock.setFrameRange(original_start_end_time[0], original_start_end_time[1])
            mari.clock.rewind()

        except Exception, e:
            #Reset the projector and time slider back to its original settings
            mari.utils.message("Playblast failed: '%s'" %str(e))
            projector.setClampColors(original_clamp)
            projector.setUseShader(original_shader)
            projector.setLightingMode(original_mode)
            projector.setBitDepth(original_depth)
            projector.setSize(original_size, original_size)
            projector.setExportPath(original_path)
            mari.clock.setFrameRange(original_start_end_time[0], original_start_end_time[1])
            mari.clock.rewind()

# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state."
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
    
        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False

        if len(mari.projectors.list()) == 0:
            mari.utils.message("Please create/load a projector before running.")
            return False

        return True
    
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    playblast()

# ------------------------------------------------------------------------------
# Add action to Mari menu.
action = mari.actions.create(
    "Playblast", "mari.jtools.playblast()"
    )
mari.menus.addAction(action, 'MainWindow/&Camera')
mari.menus.addSeparator('MainWindow/&Camera', 'Playblast')
mari.menus.addAction(action, 'MriProjector/ItemContext')
mari.menus.addSeparator('MriProjector/ItemContext', 'Playblast')
icon_filename = "MoveToCamera.png"
icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
action.setIconPath(icon_path)