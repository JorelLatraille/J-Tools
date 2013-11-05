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
        path_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        #Add path line input and button
        path_label = QLabel('Path:')
        self.path = QLineEdit()
        path = mari.geo.current().currentVersion().path()
        self.path.setText(path)
        path_pixmap = QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QIcon(path_pixmap)
        path_button = QPushButton(icon, "")
        path_button.connect('clicked()', lambda: self._getPath())

        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path)
        path_layout.addWidget(path_button)

        ok = QPushButton('&OK')
        cancel = QPushButton('&Cancel')
        ok.connect('clicked()', self.accepted)
        cancel.connect('clicked()', self.reject)

        button_layout.addWidget(ok)
        button_layout.addWidget(cancel)

        main_layout.addLayout(path_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def _getPath(self):
        "Get file path and set the text in path LineEdit widget"
        file_path = mari.utils.misc.getSaveFileName(parent=self, caption='New Path', dir='', filter='', selected_filter=None, options=0, save_filename='model.obj')
        if file_path == "":
            return
        else:
            self.path.setText(file_path)

    def accepted(self):
        "Check file path provided exists"
        if not os.path.isfile(self.path.text):
            mari.utils.message("Cannot find: '%s'" %self.path.text)
            return

        mari.geo.current().currentVersion().setPath(r'%s' %self.path.text)

        self.accept()

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