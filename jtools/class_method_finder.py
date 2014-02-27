# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Class method finder for Mari class methods
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

import mari, inspect
import PythonQt.QtGui as QtGui

version = "0.02"

USER_ROLE_01 = 34          # PythonQt.Qt.UserRole

# ------------------------------------------------------------------------------        
class classMethodFinderGUI(QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(classMethodFinderGUI, self).__init__(parent)
        
        self.setWindowTitle("Class Method Finder")
        
        #Create geometrys layout, label, and widget. Finally populate.
        class_method_layout = QtGui.QVBoxLayout()
        class_method_header_layout = QtGui.QHBoxLayout()
        class_method_label = QtGui.QLabel("Class Methods")
        setBold(class_method_label)
        class_method_list = QtGui.QListWidget()
        
        filter_class_method_box = QtGui.QLineEdit()
        mari.utils.connect(filter_class_method_box.textEdited, lambda: updateClassMethodFilter(filter_class_method_box, class_method_list))
        
        class_method_header_layout.addWidget(class_method_label)
        class_method_header_layout.addStretch()
        class_method_search_icon = QtGui.QLabel()
        search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
        class_method_search_icon.setPixmap(search_pixmap)
        class_method_header_layout.addWidget(class_method_search_icon)
        class_method_header_layout.addWidget(filter_class_method_box)
        
        def getClasses():
            return [c for s, c in inspect.getmembers(mari)]

        class_list = getClasses()
        class_string_list = dir(mari)
        
        class_methods = []
        for i in range(len(class_list)):
            methods = []
            methods.extend(dir(class_list[i]))
            for method in methods:
                class_methods.append('mari.' + class_string_list[i] + '.' + method)
        for method in class_methods:
            class_method_list.addItem(method)
            class_method_list.item(class_method_list.count - 1).setData(USER_ROLE_01, method)
       
        selected_class_method_box = QtGui.QLineEdit()
        class_method_list.connect('currentTextChanged(QString)', selected_class_method_box, 'setText(QString)')
        
        class_method_layout.addLayout(class_method_header_layout)
        class_method_layout.addWidget(class_method_list)
        class_method_layout.addWidget(selected_class_method_box)
        
        self.setLayout(class_method_layout)
        
# ------------------------------------------------------------------------------
def updateClassMethodFilter(filter_class_method_box, class_method_list):
    "For each item in the channel list display, set it to hidden if it doesn't match the filter text."
    match_words = filter_class_method_box.text.lower().split()
    for item_index in range(class_method_list.count):
        item = class_method_list.item(item_index)
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
def classMethodFinder():
    "Import images using template given and rename layers to match file image names"
    if not isProjectSuitable():
        return

    #Create dialog
    dialog = classMethodFinderGUI()
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

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    classMethodFinder()

# ------------------------------------------------------------------------------
# Add action to Mari menu.
action = mari.actions.create(
    "Class Method Finder", "mari.jtools.classMethodFinder()"
    )
mari.menus.addAction(action, 'MainWindow/P&ython', "&Examples")
icon_filename = "Zoom.png"
icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
action.setIconPath(icon_path)