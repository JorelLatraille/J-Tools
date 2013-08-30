# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Import selected images into layer or channel and rename layer/channel to match image name
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

class importImagesGUI(QDialog):
    
    def __init__(self, parent=None):
        super(importImagesGUI, self).__init__(parent)
        
        main_layout = QVBoxLayout()
        path_layout = QGridLayout()
        button_layout = QGridLayout()
        
        #Add path line input and button
        path_label = QLabel('Path:')
        self.path = QLineEdit()
        self.path.connect("textChanged()", lambda: self.getWalk())
        path_label.setBuddy(self.path)
        path_pixmap = QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QIcon(path_pixmap)
        path_button = QPushButton(icon, "")
        path_button.connect("clicked()", lambda: self.getPath())
        
        ok_button = QPushButton("&OK")
        cancel_button = QPushButton("Cancel")
        
        path_layout.addWidget(path_label, 0, 0)
        path_layout.addWidget(self.path, 0, 1)
        path_layout.addWidget(path_button, 0, 2)
        button_layout.addWidget(ok_button, 0, 0)
        button_layout.addWidget(cancel_button, 0, 1)
        
        main_layout.addLayout(path_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        self.setWindowTitle("Import Images")
        
        ok_button.connect("clicked()", lambda: self.accepted())
        cancel_button.connect("clicked()", self.reject)

    def getPath(self):
        file_path = mari.utils.misc.getExistingDirectory(parent=self, caption='Import Images', dir='')
        if file_path == "":
            return False
        else:
            self.path.setText(file_path)
    
    def getWalk(self):
        print self.path.text
        print "hello"
        try:
            for root, subdirs, files in os.walk(self.path.text):
                for file in files:
                    print file
                    # absfile = os.path.join(root, file)
                    # relfile = absfile[len(path)+len(os.sep):]
                    # zip.write(absfile, relfile)
                    # _progress()
        except:
            pass
        
    def accepted(self):
        print "accepted"
        self.accept()
    
    def returnPath(self):
        return self.path.text

def importImages():
    dialog = importImagesGUI()
    if dialog.exec_():
        path = dialog.returnPath()
        print path
    
# NOTES:

# import $CHANNEL.$UDIM.tif
# import $LAYER.$UDIM.tif
# import $CHANNEL.$LAYER.$UDIM.tif

if __name__ == "__main__":
    importImages()
