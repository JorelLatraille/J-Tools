# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Import images into geo layer or channel and rename layer/channel to match image name
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
from PythonQt.QtCore import QRegExp

version = "0.02"

image_file_types = ['.' + format for format in mari.images.supportedReadFormats()]
tokens = ['$ENTITY', '$CHANNEL', '$LAYER', '$UDIM']
channel_resolution_options = [str(QSize.width()) for QSize in mari.images.supportedTextureSizes()]
channel_bit_depth_options = ['8', '16', '32']
layer_import_options = ['Update', 'Create New', 'Skip']
resize_options = ['Patch', 'Image']

# ------------------------------------------------------------------------------
class importImagesUI(QtGui.QDialog):
    "Create ImportImagesGUI"
    def __init__(self, parent=None):
        super(importImagesUI, self).__init__(parent)

        # Get user config from settings
        settings = mari.Settings()
        resolution = int(settings.value('jtoolsImportImagesUI/resolution')) if settings.value('jtoolsImportImagesUI/resolution') != None else 2
        bit_depth = int(settings.value('jtoolsImportImagesUI/bitDepth')) if settings.value('jtoolsImportImagesUI/bitDepth') != None else 1
        layer_option = int(settings.value('jtoolsImportImagesUI/layerOption')) if settings.value('jtoolsImportImagesUI/layerOption') != None else 0
        resize = int(settings.value('jtoolsImportImagesUI/resize')) if settings.value('jtoolsImportImagesUI/resize') != None else 0

        main_layout = QtGui.QVBoxLayout()
        path_layout = QtGui.QGridLayout()
        import_layout = QtGui.QHBoxLayout()
        options_layout = QtGui.QHBoxLayout()
        button_layout = QtGui.QGridLayout()
        
        #Add path line input and button
        path_label = QtGui.QLabel('Path:')
        self.path = QtGui.QLineEdit()
        path_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QtGui.QIcon(path_pixmap)
        path_button = QtGui.QPushButton(icon, "")
        path_button.connect("clicked()", lambda: self.getPath())
        
        #Add import template line input and validator
        punctuation_re = QRegExp(r"[a-zA-Z0-9\$\._]*")
        import_label = QtGui.QLabel('Import Template:')
        self.import_template = QtGui.QLineEdit()
        self.import_template.setValidator(QtGui.QRegExpValidator(punctuation_re, self))
        self.import_template.setPlaceholderText('e.g. $CHANNEL.$LAYER.$UDIM.tif')
        
        #Add import resize options, channel creation options and layer import options
        channel_res_label = QtGui.QLabel('Channel Resolution:')
        self.channel_res_options = QtGui.QComboBox()
        for option in channel_resolution_options:
            self.channel_res_options.addItem(option)
        self.channel_res_options.setCurrentIndex(resolution)
        channel_bit_label = QtGui.QLabel('Channel Bit Depth:')
        self.channel_bit_options = QtGui.QComboBox()
        for option in channel_bit_depth_options:
            self.channel_bit_options.addItem(option)
        self.channel_bit_options.setCurrentIndex(bit_depth)
        layer_import_label = QtGui.QLabel('Layer Import Option:')
        self.layer_import_options = QtGui.QComboBox()
        for option in layer_import_options:
            self.layer_import_options.addItem(option)
        self.layer_import_options.setCurrentIndex(layer_option)
        resize_label = QtGui.QLabel('Resize:')
        self.resize_options = QtGui.QComboBox()
        for option in resize_options:
            self.resize_options.addItem(option)
        self.resize_options.setCurrentIndex(resize)
        
        #Add OK/Cancel buttons
        ok_button = QtGui.QPushButton("&OK")
        cancel_button = QtGui.QPushButton("Cancel")
        
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
        
        #Add layouts to main QtGui.QDialog layout
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
        "Get file_ path and set the text in path LineEdit widget"
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
            mari.utils.message('Please provide a valid directory.')
            return
        if not os.path.exists(file_path):
            mari.utils.message('Please provide a valid directory.')
            return
            
        #Check import template has supported image file_ type extension
        import_template = self.import_template.text
        if import_template == '':
            mari.utils.message('Please provide import template.')
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
        else:
            self.template = import_template
            spliter = ''
        self.template_no_token = list(self.template)
        for item in self.template:
            if item in tokens:
                i = self.template_no_token.index(item)
                self.template_no_token.pop(i)
        
        #Get list of files in directory and check that type given matches files
        searching = SearchingGUI()
        searching.show()
        self.file_dict = {}
        self.file_path_dict = {}
        try:
            for root, subdirs, files in os.walk(file_path):
                for file_ in files:
                    if not searching.getRejected():
                        searching.updateProgressBar()
                        if file_.lower().endswith(type):
                            found = False
                            if len(self.template_no_token) > 0:
                                for item in self.template_no_token:
                                    if item in file_:
                                        found = True
                                    else:
                                        pass
                            else:
                                found = True
                            if found:
                                self.file_dict[file_] = os.path.abspath(os.path.join(root, file_))
                                self.file_path_dict[file_] = os.path.abspath(root)
                    else:
                        searching.reject()
                        mari.utils.message('Searching for files cancelled.')
                        return
        except:
            raise
        searching.reject()
        if len(self.file_dict) == 0:
            mari.utils.message('No files match import template %s' %self.import_template.text)
            return
        
        #Check import_template and image name match
        #Get a list of split image names to compare
        image_names = {}
        for file_ in self.file_dict:
            image_names[file_] = file_[:-len(self.type)]
        self.split_names = {}
        for file_ in image_names:
            if not spliter == '':
                self.split_names[file_] = image_names[file_].split(spliter)
            elif file_ == self.import_template.text:
                self.split_names[file_] = image_names[file_]
        if len(self.split_names) == 0:
            mari.utils.message('No files match import template %s' %self.import_template.text)
            return
        self.match_image_template = {}
        self.image_template = []
        self.file_names_short = []
        self.file_names_long = []
        self.except_template = []
        for file_ in self.split_names:
            if len(self.template) == len(self.split_names[file_]):
                if '$UDIM' in self.template:
                    it = self.template.index('$UDIM')
                    copy_split_names = list(self.split_names[file_])
                    copy_split_names.pop(it)
                    join_names = ".".join(copy_split_names)
                    if join_names in self.file_names_short:
                        pass
                    else:
                        self.file_names_short.append(join_names)
                        self.file_names_long.append(file_)
                        self.match_image_template[file_] = self.split_names[file_]
                    if tuple(copy_split_names) in self.image_template:
                        pass
                    else:
                        self.image_template.append(tuple(copy_split_names))
                else:
                    self.file_names_short.append(file_)
                    self.file_names_long.append(file_)
                    self.match_image_template[file_] = self.split_names[file_]
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
        
        #Get a list of file_ paths that co-inside with file_ names
        self.file_paths = []
        for name in self.file_names_long:
            if name in self.file_path_dict:
                self.file_paths.append(self.file_path_dict[name])

        self.accept()
        
    def returnImportTemplate(self):
        return self.import_template.text
        
    def returnChannelResOption(self):
        return self.channel_res_options.currentIndex
        
    def returnChannelBitOption(self):
        return self.channel_bit_options.currentIndex
        
    def returnLayerImportOption(self):
        return self.layer_import_options.currentIndex + 1
        
    def returnResizeOption(self):
        return self.resize_options.currentIndex
        
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
class SearchingGUI(QtGui.QDialog):
    "Create SearchingGUI"
    def __init__(self, parent=None):
        super(SearchingGUI, self).__init__(parent)
        
        self.setModal(True)
        self.setWindowTitle('Search')
        main_layout = QtGui.QVBoxLayout()
        
        #Add label, progress bar and cancel button
        search_label = QtGui.QLabel('Searching for images...')
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setMaximum(0)
        self.progressBar.setTextVisible(False)
        cancel_button = QtGui.QPushButton("Cancel")
        #Connect cancel button clicked to reject the GUI
        cancel_button.connect("clicked()", self.setRejected)
        self.rejected_status = False
        
        main_layout.addWidget(search_label)
        main_layout.addWidget(self.progressBar)
        main_layout.addWidget(cancel_button)
        
        self.setLayout(main_layout)
        
    def setRejected(self):
        self.rejected_status = True
        
    def getRejected(self):
        return self.rejected_status
        
    def setProgressBar(self, value):
        self.progressBar.setValue(value)
        QtGui.QApplication.processEvents()
        
    def updateProgressBar(self):
        current_value = self.progressBar.value
        if current_value < 100:
            self.setProgressBar(current_value + 1)
        else:
            self.setProgressBar(0)        
        
# ------------------------------------------------------------------------------        
def importImages():
    "Import images using template given and rename layers to match file_ image names"
    if not isProjectSuitable():
        return

    #Create dialog and return inputs
    dialog = importImagesUI()
    if not dialog.exec_():
        return

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

    # Save user config for ImportUI settings
    settings = mari.Settings()
    settings.beginGroup('jtoolsImportImagesUI')
    settings.setValue('resolution', channel_res)
    settings.setValue('bitDepth', channel_bit)
    settings.setValue('layerOption', layer_option)
    settings.setValue('resize', resize_option)
    settings.endGroup()
    
    channel_res = channel_resolution_options[channel_res]
    channel_bit = channel_bit_depth_options[channel_bit]

    #Import images onto corresponding token info
    for file_ in file_names_short:
        ifile_ = file_names_short.index(file_)
        if '$ENTITY' in template:
            ient = template.index('$ENTITY')
            entity = image_template[ifile_][ient]
            geo_dict[entity][0].setSelected(True)
            if '$CHANNEL' in template:
                ichan = template.index('$CHANNEL')
                channel = image_template[ifile_][ichan]
                item_list = []
                for item in geo_dict[entity]:
                    item_list.append(item.name())
                if channel in item_list:
                    ilist = item_list.index(channel)
                    channel = geo_dict[entity][ilist]
                    channel.makeCurrent()
                    old_layer_list = channel.layerList()
                    channel.importImages(os.path.join(file_paths[ifile_], import_template), resize_option, layer_option)
                    layer_list = channel.layerList()
                    if len(old_layer_list) != len(layer_list):
                        if '$LAYER' in template:
                            ilay = template.index('$LAYER')
                            layer_list[0].setName(image_template[ifile_][ilay])
                        else:
                            layer_list[0].setName(file_names_short[ifile_])
                else:
                    channel = geo_dict[entity][0].createChannel(channel, channel_res, channel_res, channel_bit)
                    old_layer_list = channel.layerList()
                    channel.importImages(os.path.join(file_paths[ifile_], import_template), resize_option, layer_option)
                    layer_list = channel.layerList()
                    if len(old_layer_list) != len(layer_list):
                        if '$LAYER' in template:
                            ilay = template.index('$LAYER')
                            layer_list[0].setName(image_template[ifile_][ilay])
                        else:
                            layer_list[0].setName(file_names_short[ifile_])
            else:
                channel = geo_dict[entity][0].createChannel(file_, channel_res, channel_res, channel_bit)
                old_layer_list = channel.layerList()
                channel.importImages(os.path.join(file_paths[ifile_], import_template), resize_option, layer_option)
                layer_list = channel.layerList()
                if len(old_layer_list) != len(layer_list):
                    if '$LAYER' in template:
                        ilay = template.index('$LAYER')
                        layer_list[0].setName(image_template[ifile_][ilay])
                    else:
                        layer_list[0].setName(file_names_short[ifile_])
                    
        elif '$CHANNEL' in template:
            ichan = template.index('$CHANNEL')
            channel = image_template[ifile_][ichan]
            item_list = []
            for item in mari.geo.current().channelList():
                item_list.append(item.name())
            if channel in item_list:
                ilist = item_list.index(channel)
                channel = mari.geo.current().channelList()[ilist]
                channel.makeCurrent()
                old_layer_list = channel.layerList()
                channel.importImages(os.path.join(file_paths[ifile_], import_template), resize_option, layer_option)
                layer_list = channel.layerList()
                if len(old_layer_list) != len(layer_list):
                    if '$LAYER' in template:
                        ilay = template.index('$LAYER')
                        layer_list[0].setName(image_template[ifile_][ilay])
                    else:
                        layer_list[0].setName(file_names_short[ifile_])
            else:
                channel = mari.geo.current().createChannel(channel, channel_res, channel_res, channel_bit)
                old_layer_list = channel.layerList()
                channel.importImages(os.path.join(file_paths[ifile_], import_template), resize_option, layer_option)
                layer_list = channel.layerList()
                if len(old_layer_list) != len(layer_list):
                    if '$LAYER' in template:
                        ilay = template.index('$LAYER')
                        layer_list[0].setName(image_template[ifile_][ilay])
                    else:
                        layer_list[0].setName(file_names_short[ifile_])
                
        elif '$LAYER' in template:
            ilay = template.index('$LAYER')
            channel = mari.geo.current().currentChannel()
            old_layer_list = channel.layerList()
            channel.importImages(os.path.join(file_paths[ifile_], import_template), resize_option, layer_option)
            layer_list = channel.layerList()
            if len(old_layer_list) != len(layer_list):
                layer_list[0].setName(image_template[ifile_][ilay])
            
        else:
            channel = mari.geo.current().currentChannel()
            old_layer_list = channel.layerList()
            channel.importImages(os.path.join(file_paths[ifile_], import_template), resize_option, layer_option)
            layer_list = channel.layerList()
            if len(old_layer_list) != len(layer_list):
                layer_list[0].setName(file_)
                    
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
    importImages()