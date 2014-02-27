# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Change the current geo version's path
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
import PythonQt.QtGui as QtGui
import PythonQt.QtCore as QtCore

version = "0.04"

# ------------------------------------------------------------------------------
class ChangeGeoVersionPathUI(QtGui.QDialog):
    "Create ImportImagesGUI"
    def __init__(self, filter_types, parent=None):
        super(ChangeGeoVersionPathUI, self).__init__(parent)

        #Set title and create the major layouts
        self.filter_types = filter_types
        self.setWindowTitle('Change Current Geo Version Path')
        main_layout = QtGui.QVBoxLayout()
        current_path_layout = QtGui.QHBoxLayout()
        path_layout = QtGui.QHBoxLayout()
        button_layout = QtGui.QHBoxLayout()

        #Create label to display current geo version path
        current_path_label = QtGui.QLabel("Current Geo Version Path:")
        self.current_path = QtGui.QLineEdit(mari.geo.current().currentVersion().path())
        self.current_path.setReadOnly(True)
        self.current_path.setMinimumWidth(600)

        current_path_layout.addWidget(current_path_label)
        current_path_layout.addWidget(self.current_path)

        #Create path line input and button
        path_label = QtGui.QLabel('New Path:')
        self.path = QtGui.QLineEdit(mari.geo.current().currentVersion().path())
        path_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QtGui.QIcon(path_pixmap)
        path_button = QtGui.QPushButton(icon, "")
        path_button.connect('clicked()', lambda: self._getPath())

        #Add path widgets to path_layout
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path)
        path_layout.addWidget(path_button)

        #Create buttons and hook them up
        _apply = QtGui.QPushButton('&Apply')
        close = QtGui.QPushButton('&Close')
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
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        #Connect mari geo entity current selection changed to self._updatePath
        mari.utils.signal_helpers.connect(mari.geo.entityMadeCurrent, self._updatePath)

    def _updatePath(self):
        "Update current path to geo version path"
        self.current_path.setText(mari.geo.current().currentVersion().path())
        self.path.setText(mari.geo.current().currentVersion().path())

    def _getPath(self):
        "Get file path and set the text in path LineEdit widget"
        file_path = mari.utils.misc.getOpenFileName(parent=self, caption='New Path', dir='', filter=self.filter_types, selected_filter=0, options=0) # If you wish to add more filters either '*.obj *.mb' or '*.obj *.mb;;*.txt' will work
        if file_path == "":
            return
        else:
            self.path.setText(file_path)

    def _accepted(self):
        "Check file path provided exists and ends with filter_types"
        if not os.path.isfile(self.path.text) and not self.path.text.endswith((self.filter_types)):
            self.path.selectAll()
            return

        #Change the geo version path
        mari.geo.current().currentVersion().setPath(r'%s' %self.path.text)
        self._updatePath()

# ------------------------------------------------------------------------------
def changeGeoVersionPath():
    "Change the current geo version's path"
    if not isProjectSuitable():
        return

    #Create dialog and return inputs
    if mari.app.version().number() >= 20599999:
        filter_types = '*.' + ' *.'.join(mari.geo.supportedReadFormats())
    else:
        filter_types = '*.obj'
    dialog = ChangeGeoVersionPathUI(filter_types)
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

# ------------------------------------------------------------------------------
# Add action to Mari menu.
action = mari.actions.create(
    "Change Geo Version Path", "mari.jtools.changeGeoVersionPath()"
    )
mari.menus.addAction(action, 'MainWindow/&Objects')
mari.menus.addSeparator('MainWindow/&Objects', 'Change Geo Version Path')
mari.menus.addAction(action, 'MriGeoEntity/ItemContext')
mari.menus.addSeparator('MriGeoEntity/ItemContext', 'Change Geo Version Path')
icon_filename = "ImportFile.png"
icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
action.setIconPath(icon_path)