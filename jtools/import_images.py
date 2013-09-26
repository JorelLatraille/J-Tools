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
tokens = ['$ENTITY', '$CHANNEL', '$LAYER', '$UDIM']
channel_resolution_options = ['256', '512', '1024', '2048', '4096', '8192', '16384', '32768']
channel_bit_depth_options = ['8', '16', '32']
layer_import_options = ['Update', 'Create New', 'Skip']
resize_options = ['Patch', 'Image']

# ------------------------------------------------------------------------------ 
class ImportImagesGUI(QDialog):
    
    def __init__(self, parent=None):
        super(ImportImagesGUI, self).__init__(parent)
        
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
        
        #Add import resize options, channel creation options and layer import options
        channel_res_label = QLabel('Channel Resolution:')
        self.channel_res_options = QComboBox()
        for option in channel_resolution_options:
            self.channel_res_options.addItem(option)
        self.channel_res_options.setCurrentIndex(self.channel_res_options.findText('2048'))
        channel_bit_label = QLabel('Channel Bit Depth:')
        self.channel_bit_options = QComboBox()
        for option in channel_bit_depth_options:
            self.channel_bit_options.addItem(option)
        self.channel_bit_options.setCurrentIndex(self.channel_bit_options.findText('16'))
        layer_import_label = QLabel('Layer Import Option:')
        self.layer_import_options = QComboBox()
        for option in layer_import_options:
            self.layer_import_options.addItem(option)
        self.layer_import_options.setCurrentIndex(self.layer_import_options.findText('Update'))
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
        options_layout.addWidget(channel_res_label)
        options_layout.addWidget(self.channel_res_options)
        options_layout.addWidget(channel_bit_label)
        options_layout.addWidget(self.channel_bit_options)
        options_layout.addWidget(layer_import_label)
        options_layout.addWidget(self.layer_import_options)
        options_layout.addWidget(resize_label)
        options_layout.addWidget(self.resize_options)
        button_layout.addWidget(ok_button, 1, 0)
        button_layout.addWidget(cancel_button, 1, 1)
        
        #Add layouts to main QDialog layout
        main_layout.addLayout(path_layout)
        main_layout.addLayout(import_layout)
        main_layout.addLayout(options_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        self.setWindowTitle("Import Images")
        self.setMinimumSize(640, 140)
        
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
        
        #Create template list and remove any tokens
        import_template = import_template[:-len(self.type)]
        if '.' in import_template:
            self.template = import_template.split('.')
            spliter = '.'
        elif '_' in import_template:
            self.template = import_template.split('_')
            spliter = '_'
        self.template_no_token = list(self.template)
        for item in self.template:
            if item in tokens:
                i = self.template_no_token.index(item)
                self.template_no_token.pop(i)
        
        #Get list of files in directory and check that type given matches files
        self.file_dict = {}
        self.file_path_dict = {}
        try:
            for root, subdirs, files in os.walk(file_path):
                for file in files:
                    if file.lower().endswith(type):
                        found = False
                        if len(self.template_no_token) > 0:
                            for item in self.template_no_token:
                                if item in file:
                                    found = True
                                else:
                                    pass
                        else:
                            found = True
                        if found:
                            self.file_dict[file] = os.path.abspath(os.path.join(root, file))
                            self.file_path_dict[file] = os.path.abspath(root)
            if len(self.file_dict) == 0:
                mari.utils.message('No files match import template %s' %self.import_template.text)
                return
        except:
            raise
        
        #Check import_template and image name match
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
                    copy_split_names = list(self.split_names[file])
                    copy_split_names.pop(it)
                    join_names = ".".join(copy_split_names)
                    if join_names in self.file_names_short:
                        pass
                    else:
                        self.file_names_short.append(join_names)
                        self.file_names_long.append(file)
                    if tuple(copy_split_names) in self.image_template:
                        pass
                    else:
                        self.image_template.append(tuple(copy_split_names))
                self.match_image_template[file] = self.split_names[file]
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
        #Iterate through match_image_template and file_dict, compare and run appropriate command
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
        
        #Accept the inputs and close the dialog
        self.accept()
        
    def returnImportTemplate(self):
        return self.import_template.text
        
    def returnChannelResOption(self):
        return int(self.channel_res_options.currentText)
        
    def returnChannelBitOption(self):
        return int(self.channel_bit_options.currentText)
        
    def returnLayerImportOption(self):
        if self.layer_import_options.currentText == 'Update':
            layer_import_option = 1
        elif self.layer_import_options.currentText == 'Create New':
            layer_import_option = 2
        else:
            layer_import_option = 3
        return layer_import_option
        
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
        
    def returnFileNamesShort(self):
        return self.file_names_short
        
    def returnFilePaths(self):
        return self.file_paths
        
    def returnImageTemplate(self):
        return self.image_template
        
# ------------------------------------------------------------------------------       
class SearchingGUI(QDialog):

    def __init__(self, parent=None):
        super(SearchGUI, self).__init__(parent)
        
        main_layout = QVBoxLayout()
        self.windowTitle('Search')
        
        #Add path line input and button
        path_label = QLabel('Searching for images...')
        self.progressBar = QProgressBar()
        
        self.progressBar.setMaximum(10)
        
    def setProgressBar(self, value):
        self.progressBar.setValue(value)
        
    def updateProgressBar(self):
        current_value = self.progressBar.currentValue()
        
# ------------------------------------------------------------------------------        
def importImages():
    "Import images using template given and rename layers to match file image names"
    if not isProjectSuitable():
        return

    #Create dialog and return inputs
    dialog = ImportImagesGUI()
    if dialog.exec_():
        import_template = dialog.returnImportTemplate()
        channel_res = dialog.returnChannelResOption()
        channel_bit = dialog.returnChannelBitOption()
        layer_option = dialog.returnLayerImportOption()
        resize_option = dialog.returnResizeOption()
        template = dialog.returnTemplate()
        geo_dict = dialog.returnGeoDict()
        file_names_short = dialog.returnFileNamesShort()
        file_paths = dialog.returnFilePaths()
        image_template = dialog.returnImageTemplate()
        
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
                        old_layer_list = channel.layerList()
                        channel.importImages(os.path.join(file_paths[ifile], import_template), resize_option, layer_option)
                        layer_list = channel.layerList()
                        if len(old_layer_list) != len(layer_list):
                            if '$LAYER' in template:
                                ilay = template.index('$LAYER')
                                layer_list[0].setName(image_template[ifile][ilay])
                            else:
                                layer_list[0].setName(file_names_short[ifile])
                    else:
                        channel = geo_dict[entity][0].createChannel(channel, channel_res, channel_res, channel_bit)
                        old_layer_list = channel.layerList()
                        channel.importImages(os.path.join(file_paths[ifile], import_template), resize_option, layer_option)
                        layer_list = channel.layerList()
                        if len(old_layer_list) != len(layer_list):
                            if '$LAYER' in template:
                                ilay = template.index('$LAYER')
                                layer_list[0].setName(image_template[ifile][ilay])
                            else:
                                layer_list[0].setName(file_names_short[ifile])
                else:
                    channel = geo_dict[entity][0].createChannel(file, channel_res, channel_res, channel_bit)
                    old_layer_list = channel.layerList()
                    channel.importImages(os.path.join(file_paths[ifile], import_template), resize_option, layer_option)
                    layer_list = channel.layerList()
                    if len(old_layer_list) != len(layer_list):
                        if '$LAYER' in template:
                            ilay = template.index('$LAYER')
                            layer_list[0].setName(image_template[ifile][ilay])
                        else:
                            layer_list[0].setName(file_names_short[ifile])
                        
            elif '$CHANNEL' in template:
                ichan = template.index('$CHANNEL')
                channel = image_template[ifile][ichan]
                item_list = []
                for item in mari.geo.current().channelList():
                    item_list.append(item.name())
                if channel in item_list:
                    ilist = item_list.index(channel)
                    channel = mari.geo.current().channelList()[ilist]
                    channel.makeCurrent()
                    old_layer_list = channel.layerList()
                    channel.importImages(os.path.join(file_paths[ifile], import_template), resize_option, layer_option)
                    layer_list = channel.layerList()
                    if len(old_layer_list) != len(layer_list):
                        if '$LAYER' in template:
                            ilay = template.index('$LAYER')
                            layer_list[0].setName(image_template[ifile][ilay])
                        else:
                            layer_list[0].setName(file_names_short[ifile])
                else:
                    channel = mari.geo.current().createChannel(channel, channel_res, channel_res, channel_bit)
                    old_layer_list = channel.layerList()
                    channel.importImages(os.path.join(file_paths[ifile], import_template), resize_option, layer_option)
                    layer_list = channel.layerList()
                    if len(old_layer_list) != len(layer_list):
                        if '$LAYER' in template:
                            ilay = template.index('$LAYER')
                            layer_list[0].setName(image_template[ifile][ilay])
                        else:
                            layer_list[0].setName(file_names_short[ifile])
                    
            elif '$LAYER' in template:
                ilay = template.index('$LAYER')
                channel = mari.geo.current().currentChannel()
                old_layer_list = channel.layerList()
                channel.importImages(os.path.join(file_paths[ifile], import_template), resize_option, layer_option)
                layer_list = channel.layerList()
                if len(old_layer_list) != len(layer_list):
                    layer_list[0].setName(image_template[ifile][ilay])
                
            else:
                channel = mari.geo.current().currentChannel()
                old_layer_list = channel.layerList()
                channel.importImages(os.path.join(file_paths[ifile], import_template), resize_option, layer_option)
                layer_list = channel.layerList()
                if len(old_layer_list) != len(layer_list):
                    layer_list[0].setName(file)
                    
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

if __name__ == "__main__":
    importImages()