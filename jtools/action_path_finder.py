# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Action path finder for Mari actions
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

USER_ROLE_01 = 34          # PythonQt.Qt.UserRole

# ------------------------------------------------------------------------------        
class actionPathFinderGUI(QDialog):
    
    def __init__(self, parent=None):
        super(actionPathFinderGUI, self).__init__(parent)
        
        self.setWindowTitle("Action Path Finder")
        
        #Create geometrys layout, label, and widget. Finally populate.
        action_layout = QVBoxLayout()
        action_header_layout = QHBoxLayout()
        action_label = QLabel("Action Paths")
        setBold(action_label)
        action_list = QListWidget()
        
        filter_action_box = QLineEdit()
        mari.utils.connect(filter_action_box.textEdited, lambda: updateActionPathFilter(filter_action_box, action_list))
        
        action_header_layout.addWidget(action_label)
        action_header_layout.addStretch()
        action_search_icon = QLabel()
        search_pixmap = QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
        action_search_icon.setPixmap(search_pixmap)
        action_header_layout.addWidget(action_search_icon)
        action_header_layout.addWidget(filter_action_box)
        
        action_path_list = mari.actions.list()
        for action in action_path_list:
            action_list.addItem(action)
            action_list.item(action_list.count - 1).setData(USER_ROLE_01, action)
        
        selected_action_box = QLineEdit
        selected_action_box.setText(
        
        action_layout.addLayout(action_header_layout)
        action_layout.addWidget(action_list)
        
        self.setLayout(action_layout)

# ------------------------------------------------------------------------------
def updateActionPathFilter(filter_action_box, action_list):
    "For each item in the channel list display, set it to hidden if it doesn't match the filter text."
    match_words = filter_action_box.text.lower().split()
    for item_index in range(action_list.count):
        item = action_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)        
        
# ------------------------------------------------------------------------------  
def setBold(widget):
    "Sets text to bold."
    font = widget.font
    font.setWeight(75)
    widget.setFont(font)        
        
# ------------------------------------------------------------------------------        
def actionPathFinder():
    "Import images using template given and rename layers to match file image names"
    if not isProjectSuitable():
        return

    #Create dialog and return inputs
    dialog = actionPathFinderGUI()
    dialog.show()
        
# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state."
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
        return True
    
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False

if __name__ == "__main__":
    actionPathFinder()