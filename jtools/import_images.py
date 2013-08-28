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
        
        layout = QVBoxLayout()
        self.input = QLineEdit()
        
        ok_button = QPushButton("&OK")
        cancel_button = QPushButton("Cancel")
        
        layout.addWidget(self.input)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)
        
        self.setLayout(layout)
        self.setWindowTitle("Import Images")
        
        ok_button.connect("clicked()", self.accept)
        cancel_button.connect("clicked()", self.reject)
    
    def returnInput(self):
        return self.input.text

def importImages():
    dialog = importImagesGUI()
    if dialog.exec_():
        input = dialog.returnInput()
        print input
    # mari.utils.misc.getOpenFileName(parent=None, caption='Import Images', dir='', filter='bmp', 'jpg', 'jpeg', 'png', 'ppm', 'psd', 'tga', 'tif', 'tiff', 'xbm', 'xpm', selected_filter=None, options=0)
    
    
    
# NOTES:

# import $CHANNEL.$UDIM.tif
# import $LAYER.$UDIM.tif
# import $CHANNEL.$LAYER.$UDIM.tif

if __name__ == "__main__":
    importImages()
