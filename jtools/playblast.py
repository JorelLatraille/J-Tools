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

version = "0.01"

image_file_types = ['.bmp', '.jpg', '.jpeg', '.png', '.ppm', '.psd', '.tga', '.tif', '.tiff', '.xbm', '.xpm', '.exr']

# ------------------------------------------------------------------------------
class playblastGUI(QDialog):
    "Create ImportImagesGUI"
    def __init__(self, parent=None):
        super(playblastGUI, self).__init__(parent)
        
        main_layout = QVBoxLayout()
        path_layout = QHBoxLayout()
        import_layout = QHBoxLayout()
        options_layout = QHBoxLayout()
        button_layout = QGridLayout()
        
        #Add path line input and button
        path_label = QLabel('Path:')
        self.path = QLineEdit()
        path_pixmap = QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QIcon(path_pixmap)
        path_button = QPushButton(icon, "")
        path_button.connect("clicked()", lambda: self.getPath())
        
        #Add import template line input and validator
        punctuation_re = QRegExp(r"[a-zA-Z0-9\$\._]*")
        import_label = QLabel('Import Template:')
        self.import_template = QLineEdit()
        self.import_template.setValidator(QRegExpValidator(punctuation_re, self))
        self.import_template.setPlaceholderText('e.g. $CHANNEL.$LAYER.$UDIM.tif')
        
        #Add import resize options, channel creation options and layer import options
        channel_res_label = QLabel('Channel Resolution:')
        self.channel_res_options = QComboBox()
        for option in channel_resolution_options:
            self.channel_res_options.addItem(option)
        self.channel_res_options.setCurrentIndex(self.channel_res_options.findText('2048'))
        channel_bit_label = QLabel('Channel Bit Depth:')
        self.channel_bit_options = QComboBox()
        for option in channel_bit_depth_options:
            self.channel_bit_options.addItem(option)
        self.channel_bit_options.setCurrentIndex(self.channel_bit_options.findText('16'))
        layer_import_label = QLabel('Layer Import Option:')
        self.layer_import_options = QComboBox()
        for option in layer_import_options:
            self.layer_import_options.addItem(option)
        self.layer_import_options.setCurrentIndex(self.layer_import_options.findText('Update'))
        resize_label = QLabel('Resize:')
        self.resize_options = QComboBox()
        for option in resize_options:
            self.resize_options.addItem(option)
        self.resize_options.setCurrentIndex(self.resize_options.findText('Patch'))
        
        #Add OK/Cancel buttons
        ok_button = QPushButton("&OK")
        cancel_button = QPushButton("Cancel")
        
        #Add widgets to respective layouts
        path_layout.addWidget(path_label, 0, 0)
        path_layout.addWidget(self.path, 0, 1)
        path_layout.addWidget(path_button, 0, 2)
        import_layout.addWidget(import_label)
        import_layout.addWidget(self.import_template)
        options_layout.addWidget(channel_res_label)
        options_layout.addWidget(self.channel_res_options)
        options_layout.addWidget(channel_bit_label)
        options_layout.addWidget(self.channel_bit_options)
        options_layout.addWidget(layer_import_label)
        options_layout.addWidget(self.layer_import_options)
        options_layout.addWidget(resize_label)
        options_layout.addWidget(self.resize_options)
        button_layout.addWidget(ok_button, 1, 0)
        button_layout.addWidget(cancel_button, 1, 1)
        
        #Add layouts to main QDialog layout
        main_layout.addLayout(path_layout)
        main_layout.addLayout(import_layout)
        main_layout.addLayout(options_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        self.setWindowTitle("Import Images")
        self.setMinimumSize(640, 140)
        
        ok_button.connect("clicked()", lambda: self.accepted())
        cancel_button.connect("clicked()", self.reject)

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