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
layer_import_options = ['Update', 'Create New', 'Skip']

class importImagesGUI(QDialog):
    
    def __init__(self, parent=None):
        super(importImagesGUI, self).__init__(parent)
        
        main_layout = QVBoxLayout()
        path_layout = QGridLayout()
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
        
        #Add import resize options and layer import options
        resize_label = QLabel('Resize:')
        self.resize_options = QComboBox()
        for option in resize_options:
            self.resize_options.addItem(option)
        self.resize_options.setCurrentIndex(self.resize_options.findText('Patch'))
        layer_import_label = QLabel('Layer Import Option:')
        self.layer_import_options = QComboBox()
        for option in layer_import_options:
            self.layer_import_options.addItem(option)
        self.layer_import_options.setCurrentIndex(self.layer_import_options.findText('Update'))
        
        #Add OK/Cancel buttons
        ok_button = QPushButton("&OK")
        cancel_button = QPushButton("Cancel")
        
        #Add widgets to respective layouts
        path_layout.addWidget(path_label, 0, 0)
        path_layout.addWidget(self.path, 0, 1)
        path_layout.addWidget(path_button, 0, 2)
        import_layout.addWidget(import_label)
        import_layout.addWidget(self.import_template)
        options_layout.addWidget(resize_label)
        options_layout.addWidget(self.resize_options)
        options_layout.addStretch()
        options_layout.addWidget(layer_import_label)
        options_layout.addWidget(self.layer_import_options)
        button_layout.addWidget(ok_button, 1, 0)
        button_layout.addWidget(cancel_button, 1, 1)
        
        #Add layouts to main QDialog layout
        main_layout.addLayout(path_layout)
        main_layout.addLayout(import_layout)
        main_layout.addLayout(options_layout)
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
        self.file_path_dict = {}
        try:
            for root, subdirs, files in os.walk(file_path):
                for file in files:
                    if file.lower().endswith(type):
                        self.file_dict[file] = os.path.abspath(os.path.join(root, file))
                        self.file_path_dict[file] = os.path.abspath(root)
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
        self.split_names = {}
        for file in image_names:
            self.split_names[file] = image_names[file].split(spliter)
        self.match_image_template = {}
        self.image_template = []
        self.file_names_short = []
        self.file_names_long = []
        for file in self.split_names:
            if len(self.template) == len(self.split_names[file]):
                if '$UDIM' in self.template:
                    it = self.template.index('$UDIM')
                    copy_split_names = self.split_names[file]
                    copy_split_names.pop(it)
                    join_names = ".".join(copy_split_names)
                    if join_names in self.file_names_short:
                        pass
                    else:
                        self.file_names_short.append(join_names)
                        self.file_names_long.append(file)
                self.match_image_template[file] = self.split_names[file]
                if tuple(self.split_names[file]) in self.image_template:
                    pass
                else:
                    self.image_template.append(tuple(self.split_names[file]))
        if len(self.match_image_template) == 0:
            mari.utils.misc.message('Import template and image name(s) do not match')
            return
        
        #Create geo dictionary with geo name as key, and geo dictionary index 0 as geo and subsequent indexes as channels        
        geo_list = mari.geo.list()
        self.geo_dict = {}
        for geo in geo_list:
            geo_info = []
            geo_info.append(geo)
            geo_info.extend(geo.channelList())
            self.geo_dict[geo.name()] = geo_info
        #Iterate through match_image_template and file_dict, compare token_dict and run appropriate command
        for mkey in self.match_image_template:
            for fkey in self.file_dict:
                if fkey == mkey:
                    for index in range(len(self.template)):
                        if self.template[index] == '$ENTITY':
                            entity = self.match_image_template[mkey][index]
                            if entity in self.geo_dict:
                                pass
                            else:
                                mari.utils.misc.message("Import template $ENTITY image file name '%s' does not match geo name(s) in project" %entity)
                                return
        
        #Get a list of file paths that co-inside with file names
        self.file_paths = []
        for name in self.file_names_long:
            if name in self.file_path_dict:
                self.file_paths.append(self.file_path_dict[name])
                
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
        
    def returnFilePathDict(self):
        return self.file_path_dict
        
    def returnFileNamesShort(self):
        return self.file_names_short
        
    def returnFileNamesLong(self):
        return self.file_names_long
        
    def returnFilePaths(self):
        return self.file_paths
        
    def returnImageTemplate(self):
        return self.image_template

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
        file_path_dict = dialog.returnFilePathDict()
        file_names_short = dialog.returnFileNamesShort()
        file_names_long = dialog.returnFileNamesLong()
        file_paths = dialog.returnFilePaths()
        image_template = dialog.returnImageTemplate()
        print path
        print import_template
        print type
        print tokens
        print resize_option
        print template
        print geo_dict
        print '==============AHAHAHHAA===================='
        print match_image_template
        print file_dict
        print file_path_dict
        print '********************BALLS********************'
        print file_names_short
        print file_names_long
        print "\n".join(file_names_short)
        print "\n".join(file_names_long)
        print "\n".join(file_paths)
        print image_template
        
        #Import images onto corresponding token info
        for file in file_names_short:
            ifile = file_names_short.index(file)
            if '$ENTITY' in template:
                ient = template.index('$ENTITY')
                entity = image_template[ifile][ient]
                geo_dict[entity][0].setSelected(True)
                if '$CHANNEL' in template:
                    ichan = template.index('$CHANNEL')
                    channel = image_template[ifile][ichan]
                    item_list = []
                    for item in geo_dict[entity]:
                        item_list.append(item.name())
                    if channel in item_list:
                        ilist = item_list.index(channel)
                        channel = geo_dict[entity][ilist]
                        channel.makeCurrent()
                        channel.importImages(os.path.join(file_paths[ifile], import_template), resize_option)
                        layer_list = channel.layerList()
                        if '$LAYER' in template:
                            ilay = template.index('$LAYER')
                            layer_list[0].setName(image_template[ifile][ilay])
                        else:
                            layer_list[0].setName(file_names_short[ifile])
                    else:
                        channel = geo_dict[entity][0].createChannel(channel, 2048, 2048, 16)
                        channel.importImages(os.path.join(file_paths[ifile], import_template), resize_option)

if __name__ == "__main__":
    importImages()
