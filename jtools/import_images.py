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
from PythonQt.QtCore import QRegExp

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
        punctuation_re = QRegExp(r"[a-zA-Z0-9\$\._]*")
        import_label = QLabel('Import Template:')
        self.import_template = QLineEdit()
        self.import_template.setValidator(QRegExpValidator(punctuation_re, self))
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
        "Get file path and set the text in path LineEdit widget"
        file_path = mari.utils.misc.getExistingDirectory(parent=self, caption='Import Images', dir='')
        if file_path == "":
            return
        else:
            self.path.setText(file_path)
        
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
        
        #Get list of files in directory and check that type given matches files
        self.file_dict = {}
        try:
            for root, subdirs, files in os.walk(file_path):
                for file in files:
                    # file_list.append(file)
                    if file.lower().endswith(type):
                        self.file_dict[file] = os.path.abspath(os.path.join(root, file))
            if len(self.file_dict) == 0:
                mari.utils.message('Files of type %s do not exist in this directory' %type)
                return
        except:
            raise
        
        #Check import_template and image name match
        #Get split import_template to compare
        import_template = import_template[:-len(self.type)]
        if '.' in import_template:
            self.template = import_template.split('.')
            spliter = '.'
        elif '_' in import_template:
            self.template = import_template.split('_')
            spliter = '_'
        #Get a list of split image names to compare
        image_names = {}
        for file in self.file_dict:
            image_names[file] = file[:-len(self.type)]
        split_names = {}
        for file in image_names:
            split_names[file] = image_names.get(file).split(spliter)
        self.match_image_template = {}
        for file in split_names:
            if len(self.template) == len(split_names.get(file)):
                self.match_image_template[file] = split_names.get(file)
        if len(self.match_image_template) == 0:
            mari.utils.misc.message('Import template and image name(s) do not match')
            return
            
        #Iterate through match_image_template and file_dict, compare token_dict and run appropriate command
        geo_list = mari.geo.list()
        self.geo_dict = {}
        #Create geo dictionary with geo name as key, and geo dictionary index 0 as geo and subsequent indexes as channels
        for geo in geo_list:
            geo_info = []
            geo_info.append(geo)
            geo_info.extend(geo.channelList())
            self.geo_dict[geo.name()] = geo_info
        for mkey in self.match_image_template:
            for fkey in self.file_dict:
                if fkey == mkey:
                    for index in range(len(self.template)):
                        if self.template[index] == '$ENTITY':
                            entity = self.match_image_template[mkey][index]
                            if entity in self.geo_dict:
                                self.geo_dict[entity][0].setSelected(True)
                            else:
                                mari.utils.misc.message("Import template $ENTITY image file name '%s' does not match geo name(s) in project" %entity)
                                return
        
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
        if self.resize_options.currentText == 'Patch':
            resize_option = 0
        else:
            resize_option = 1
        return resize_option
        
    def returnTemplate(self):
        return self.template
        
    def returnGeoDict(self):
        return self.geo_dict
        
    def returnMatchImageTemplate(self):
        return self.match_image_template
        
    def returnFileDict(self):
        return self.file_dict

# ------------------------------------------------------------------------------        
def importImages():
    dialog = importImagesGUI()
    if dialog.exec_():
        path = dialog.returnPath()
        import_template = dialog.returnImportTemplate()
        type = dialog.returnType()
        tokens = dialog.returnTokens()
        resize_option = dialog.returnResizeOption()
        template = dialog.returnTemplate()
        geo_dict = dialog.returnGeoDict()
        match_image_template = dialog.returnMatchImageTemplate()
        file_dict = dialog.returnFileDict()
        print path
        print import_template
        print type
        print tokens
        print resize_option
        print template
        print geo_dict
        print match_image_template
        print file_dict
        
        #Import images onto corresponding token info
        for mkey in match_image_template:
            for fkey in file_dict:
                if fkey == mkey:
                    if '$ENTITY' in template:
                        for it in range(len(template)):
                            if template[it] == '$ENTITY':
                                entity = match_image_template[mkey][it]
                                geo_dict[entity][0].setSelected(True)
                                if '$CHANNEL' in template:
                                    for ic in range(len(geo_dict.get(entity))):
                                        if ic == 0:
                                            pass
                                        if geo_dict[ic].name() in match_image_template[mkey]:
                                            geo_dict[ic].makeCurrent()
                                            geo_dict[ic].importImages(file_dict[fkey])

if __name__ == "__main__":
    importImages()
