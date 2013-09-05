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
image_file_types = ['.bmp', '.jpg', '.jpeg', '.png', '.ppm', '.psd', '.tga', '.tif', '.tiff', '.xbm', '.xpm', '.exr']
resize_options = ['Patch', 'Image']
tokens = ['$ENTITY', '$CHANNEL', '$LAYER', '$UDIM']

class importImagesGUI(QDialog):
    
    def __init__(self, parent=None):
        super(importImagesGUI, self).__init__(parent)
        
        main_layout = QVBoxLayout()
        path_layout = QGridLayout()
        import_layout = QHBoxLayout()
        resize_layout = QHBoxLayout()
        button_layout = QGridLayout()
        
        #Add path line input and button
        path_label = QLabel('Path:')
        self.path = QLineEdit()
        path_pixmap = QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QIcon(path_pixmap)
        path_button = QPushButton(icon, "")
        path_button.connect("clicked()", lambda: self.getPath())
        
        #Add import template line input and validator
        import_label = QLabel('Import Template:')
        self.import_template = QLineEdit()
        self.import_template.setPlaceholderText('e.g. $CHANNEL.$LAYER.$UDIM.tif')
        
        #Add import resize options
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
        resize_layout.addWidget(resize_label)
        resize_layout.addWidget(self.resize_options)
        resize_layout.addStretch()
        button_layout.addWidget(ok_button, 1, 0)
        button_layout.addWidget(cancel_button, 1, 1)
        
        #Add layouts to main QDialog layout
        main_layout.addLayout(path_layout)
        main_layout.addLayout(import_layout)
        main_layout.addLayout(resize_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        self.setWindowTitle("Import Images")
        self.setMinimumSize(400, 140)
        
        ok_button.connect("clicked()", lambda: self.accepted())
        cancel_button.connect("clicked()", self.reject)
        
    def getPath(self):
        file_path = mari.utils.misc.getExistingDirectory(parent=self, caption='Import Images', dir='')
        if file_path == "":
            return
        else:
            self.path.setText(file_path)
    
    # def getWalk(self):
        # print self.path.text
        # path = os.path.abspath(self.path.text)
        # print path
        # file_list = []
        # try:
            # for root, subdirs, files in os.walk(path):
                # for file in files:
                    # if file.lower().endswith(image_file_types):
                        # file_list.append(file)
            # print file_list
        # except:
            # raise
        
    def accepted(self):
        "Accepted validation"
        #Check path provided exists
        file_path = os.path.abspath(self.path.text)
        if file_path == '':
            mari.utils.message('Must provide a valid directory.')
            return
        if not os.path.exists(file_path):
            mari.utils.message('Must provide a valid directory.')
            return
            
        #Check import template has supported image file type extension
        import_template = self.import_template.text
        if import_template == '':
            mari.utils.message('Must provide import template.')
            return
        type_found = False
        for type in image_file_types:
            if import_template.endswith(type):
                type_found = True
                self.type = type
                break
        if not type_found:
            self.import_template.selectAll()
            return
        #Check import template contains tokens
        self.token_dict = {}
        for token in tokens:
            if token in import_template:
                self.token_dict[token] = True
            else:
                self.token_dict[token] = False
        print "accepted"
        self.accept()
    
    def returnPath(self):
        return self.path.text
        
    def returnImportTemplate(self):
        return self.import_template.text
    
    def returnType(self):
        return self.type
    
    def returnTokens(self):
        return self.token_dict

    def returnResizeOption(self):
        return self.resize_options.currentText        
        
def importImages():
    dialog = importImagesGUI()
    if dialog.exec_():
        path = dialog.returnPath()
        import_template = dialog.returnImportTemplate()
        type = dialog.returnType()
        tokens = dialog.returnTokens()
        resize_option = dialog.returnResizeOption()
        print path
        print import_template
        print type
        print tokens
        print resize_option
        
        file_list = []
        try:
            for root, subdirs, files in os.walk(path):
                for file in files:
                    # file_list.append(file)
                    if file.lower().endswith(type):
                        file_list.append(file)
            print file_list
        except:
            raise
    
    

if __name__ == "__main__":
    importImages()
