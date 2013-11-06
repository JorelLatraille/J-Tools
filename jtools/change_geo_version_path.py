# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Change the current geo version's path
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

import mari
from PythonQt.QtGui import *

version = "0.01"

# ------------------------------------------------------------------------------
class changeGeoVersionPathGUI(QDialog):
    "Create ImportImagesGUI"
    def __init__(self, parent=None):
        super(changeGeoVersionPathGUI, self).__init__(parent)

        #Set title and create the major layouts
        self.setWindowTitle('Playblast')
        main_layout = QVBoxLayout()
        current_path_layout = QHBoxLayout()
        path_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        #Create label to display current geo version path
        current_path_label = QLabel("Current Geo Version Path:")
        self.current_path = QLineEdit(mari.geo.current().currentVersion().path())
        self.current_path.setReadOnly(True)
        self.current_path.setMinimumWidth(600)

        current_path_layout.addWidget(current_path_label)
        current_path_layout.addWidget(self.current_path)

        #Create path line input and button
        path_label = QLabel('New Path:')
        self.path = QLineEdit(mari.geo.current().currentVersion().path())
        path_pixmap = QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QIcon(path_pixmap)
        path_button = QPushButton(icon, "")
        path_button.connect('clicked()', lambda: self._getPath())

        #Add path widgets to path_layout
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path)
        path_layout.addWidget(path_button)

        #Create buttons and hook them up
        _apply = QPushButton('&Apply')
        close = QPushButton('&Close')
        _apply.connect('clicked()', self._accepted)
        close.connect('clicked()', self.reject)

        #Add buttons to button_layout
        button_layout.addWidget(_apply)
        button_layout.addWidget(close)

        #Add layouts to dialog
        main_layout.addLayout(current_path_layout)
        main_layout.addLayout(path_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        #Keep dialog on top
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        #Connect mari geo entity current selection changed to self._updatePath
        mari.utils.signal_helpers.connect(mari.geo.entityMadeCurrent, self._updatePath)

    def _updatePath(self):
        "Update current path to geo version path"
        self.current_path.setText(mari.geo.current().currentVersion().path())
        self.path.setText(mari.geo.current().currentVersion().path())

    def _getPath(self):
        "Get file path and set the text in path LineEdit widget"
        file_path = mari.utils.misc.getSaveFileName(parent=self, caption='New Path', dir='', filter='', selected_filter=None, options=0, save_filename='model.obj')
        if file_path == "":
            return
        else:
            self.path.setText(file_path)

    def _accepted(self):
        "Check file path provided exists"
        if not os.path.isfile(self.path.text):
            mari.utils.message("Cannot find: '%s'" %self.path.text)
            return

        #Change the geo version path
        mari.geo.current().currentVersion().setPath(r'%s' %self.path.text)
        self._updatePath()

# ------------------------------------------------------------------------------
def changeGeoVersionPath():
    "Change the current geo version's path"
    if not isProjectSuitable:
        return

    #Create dialog and return inputs
    dialog = changeGeoVersionPathGUI()
    dialog.show()

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
    changeGeoVersionPath()