# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Export selected channels from one or more objects
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

version = "0.02"

USER_ROLE = 34          # PythonQt.Qt.UserRole

# ------------------------------------------------------------------------------
class ExportSelectedChannelsGUI(QDialog):
    "Export channels from one or more objects."
    def __init__(self, parent=None):
        super(ExportSelectedChannelsGUI, self).__init__(parent)

        #Set window title and create a main layout
        self.setWindowTitle("Export Selected Channels")
        main_layout = QVBoxLayout()
        
        #Create layout for middle section
        top_layout = QHBoxLayout()
        
        #Create channel layout, label, and widget. Finally populate.
        channel_layout = QVBoxLayout()
        channel_header_layout = QHBoxLayout()
        self.channel_label = QLabel("Channels")
        setBold(self.channel_label)
        self.channel_list = QListWidget()
        self.channel_list.setSelectionMode(self.channel_list.ExtendedSelection)
        
        #Create filter box for channel list
        self.channel_filter_box = QLineEdit()
        mari.utils.connect(self.channel_filter_box.textEdited, lambda: updateChannelFilter(self.channel_filter_box, self.channel_list))
        
        #Create layout and icon/label for channel filter
        channel_header_layout.addWidget(self.channel_label)
        channel_header_layout.addStretch()
        self.channel_search_icon = QLabel()
        search_pixmap = QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
        self.channel_search_icon.setPixmap(search_pixmap)
        channel_header_layout.addWidget(self.channel_search_icon)
        channel_header_layout.addWidget(self.channel_filter_box)
        
        #Populate geo : channel list widget
        geo_list = mari.geo.list()
        chan_list = []
        for geo in geo_list:
            chan_list.append((geo.name(), geo.channelList()))
        for item in chan_list:
            for channel in item[1]:
                self.channel_list.addItem(item[0] + ' : ' + channel.name())
                self.channel_list.item(self.channel_list.count - 1).setData(USER_ROLE, channel)
        
        #Add filter layout and channel list to channel layout
        channel_layout.addLayout(channel_header_layout)
        channel_layout.addWidget(self.channel_list)
        
        #Create middle button section
        middle_button_layout = QVBoxLayout()
        self.add_button = QPushButton("+")
        self.remove_button = QPushButton("-")
        middle_button_layout.addStretch()
        middle_button_layout.addWidget(self.add_button)
        middle_button_layout.addWidget(self.remove_button)
        middle_button_layout.addStretch()
        
        #Add wrapped QListWidget with custom functions
        export_layout = QVBoxLayout()
        export_header_layout = QHBoxLayout()
        self.export_label = QLabel("Channels To Export")
        setBold(self.export_label)
        self.export_list = ChannelsToExportList()
        self.export_list.setSelectionMode(self.export_list.ExtendedSelection)
        
        #Create filter box for export list
        self.export_filter_box = QLineEdit()
        mari.utils.connect(self.export_filter_box.textEdited, lambda: updateExportFilter(self.export_filter_box, self.export_list))
        
        #Create layout and icon/label for export filter
        export_header_layout.addWidget(self.export_label)
        export_header_layout.addStretch()
        self.export_search_icon = QLabel()
        self.export_search_icon.setPixmap(search_pixmap)
        export_header_layout.addWidget(self.export_search_icon)
        export_header_layout.addWidget(self.export_filter_box)
        
        #Add filter layout and export list to export layout
        export_layout.addLayout(export_header_layout)
        export_layout.addWidget(self.export_list)
        
        #Hook up add/remove buttons
        self.remove_button.connect("clicked()", self.export_list.removeChannels)
        self.add_button.connect("clicked()", lambda: self.export_list.addChannels(self.channel_list))

        #Add widgets to top layout
        top_layout.addLayout(channel_layout)
        top_layout.addLayout(middle_button_layout)
        top_layout.addLayout(export_layout)
        
        #Add layouts to main layout and dialog
        main_layout.addLayout(top_layout)
    
# -----------------------------------------------------------------------------------------------------    
    
        #Add middle layout.
        middle_layout = QHBoxLayout()

        #Get mari default path and template
        path = os.path.abspath(mari.resources.path(mari.resources.DEFAULT_EXPORT))
        template = mari.resources.sequenceTemplate()
        export_path_template = os.path.join(path, template)

        #Add path line input and button, also set text to Mari default path and template
        path_label = QLabel('Path:')
        self.path_line_edit = QLineEdit()
        path_pixmap = QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QIcon(path_pixmap)
        path_button = QPushButton(icon, "")
        path_button.connect("clicked()", lambda: self.getPath())
        self.path_line_edit.setText(export_path_template)
            
        #Add path line input and button to middle layout    
        middle_layout.addWidget(path_label)
        middle_layout.addWidget(self.path_line_edit)
        middle_layout.addWidget(path_button)
        #Add to main layout
        main_layout.addLayout(middle_layout)
    
        #Add bottom layout.
        bottom_layout = QHBoxLayout()
        
        #Add export option check boxes
        self.export_everything_box = QCheckBox('Export Everything')
        self.export_everything_box.connect("clicked()", lambda: self.exportEverything())
        self.export_flattened_box = QCheckBox('Export Flattened')
        self.export_small_textures_box = QCheckBox('Small Textures')
    
        #Add OK Cancel buttons layout, buttons and add
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        ok_button.connect("clicked()", self.checkInput)
        cancel_button.connect("clicked()", self.reject)
        
        #Add tick boxes and buttons to bottom layout
        bottom_layout.addWidget(self.export_everything_box)
        bottom_layout.addWidget(self.export_flattened_box)
        bottom_layout.addWidget(self.export_small_textures_box)
        bottom_layout.addWidget(ok_button)
        bottom_layout.addWidget(cancel_button)

        #Add bottom layout to main layout and set main layout to dialog's layout
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

    #Hide parts of interface if export everything is ticked
    def exportEverything(self):
        _bool = self.export_everything_box.isChecked()
        self.channel_label.setHidden(_bool)
        self.channel_search_icon.setHidden(_bool)
        self.channel_filter_box.setHidden(_bool)
        self.channel_list.setHidden(_bool)
        self.export_label.setHidden(_bool)
        self.export_search_icon.setHidden(_bool)
        self.export_filter_box.setHidden(_bool)
        self.export_list.setHidden(_bool)
        self.add_button.setHidden(_bool)
        self.remove_button.setHidden(_bool)
    
    #Get the path from existing directory
    def getPath(self):
        path = mari.utils.misc.getSaveFileName(parent=self, caption='Export Path', dir='', filter='', selected_filter=None, options=0, save_filename='')
        if path == "":
            return
        else:
            self.setPath(os.path.abspath(path))

    #Set the path line edit box text to be the path provided
    def setPath(self, path):
        self.path_line_edit.setText(path)

    #Check path and template will work, check if export everything box is ticked if not make sure there are some channels to export
    def checkInput(self):
        image_file_types = ('.bmp', '.jpg', '.jpeg', '.png', '.ppm', '.psd', '.tga', '.tif', '.tiff', '.xbm', '.xpm', '.exr')
        path_template = self.path_line_edit.text
        if not os.path.exists(os.path.split(path_template)[0]):
            mari.utils.message("Path does not exist: '%s'" %(os.path.split(path_template)[0]))
            return
        if not path_template.endswith(image_file_types):
            mari.utils.message("File type is not supported: '%s'" %(os.path.split(path_template)[1]))
            return
        if self.export_everything_box.isChecked():
            pass
        elif len(self.export_list.currentChannels()) == 0:
            mari.utils.message("Please add a channel to export")
            return
        self.accept()

    #Get list of channels to export from the export list
    def getChannelsToExport(self):
        return self.export_list.currentChannels()

    #Get export path and template
    def getExportPathTemplate(self):
        return self.path_line_edit.text

    #Get export everything box is ticked (bool)
    def getExportEverything(self):
        return self.export_everything_box.isChecked()

    #Get export flattened box is ticked (bool)
    def getExportFlattened(self):
        return self.export_flattened_box.isChecked()

    #Get export small textures box is ticked (bool)
    def getExportSmallTextures(self):
        return self.export_small_textures_box.isChecked()

# ------------------------------------------------------------------------------   
class ChannelsToExportList(QListWidget):
    "Stores a list of operations to perform."
    
    def __init__(self, title="For Export"):
        super(ChannelsToExportList, self).__init__()
        self._title = title
        self.setSelectionMode(self.ExtendedSelection)
        
    def currentChannels(self):
        return [self.item(index).data(USER_ROLE) for index in range(self.count)]
        
    def addChannels(self, channel_list):
        "Adds an operation from the current selections of channels and directories."
        selected_items = channel_list.selectedItems()
        if selected_items == []:
            mari.utils.message("Please select at least one channel.")
            return
        
        # Add channels that aren't already added
        current_channels = set(self.currentChannels())
        for item in selected_items:
            channel = item.data(USER_ROLE)
            if channel not in current_channels:
                current_channels.add(channel)
                self.addItem(item.text())
                self.item(self.count - 1).setData(USER_ROLE, channel)
        
    def removeChannels(self):
        "Removes any currently selected operations."
        for item in reversed(self.selectedItems()):     # reverse so indices aren't modified
            index = self.row(item)
            self.takeItem(index)    

# ------------------------------------------------------------------------------
def updateChannelFilter(channel_filter_box, channel_list):
    "For each item in the channel list display, set it to hidden if it doesn't match the filter text."
    match_words = channel_filter_box.text.lower().split()
    for item_index in range(channel_list.count):
        item = channel_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)
        
# ------------------------------------------------------------------------------
def updateExportFilter(export_filter_box, export_list):
    "For each item in the export list display, set it to hidden if it doesn't match the filter text."
    match_words = export_filter_box.text.lower().split()
    for item_index in range(export_list.count):
        item = export_list.item(item_index)
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
def exportChannels(channels, path, flattened, small_textures):
    save_options = 1
    if small_textures:
        save_options = 0
    #Check if export flattened is ticked, if not export unflattened
    if flattened:
        for channel in channels:
            try:
                channel.exportImagesFlattened(path, save_options)
            except:
                mari.utils.message("IOError: Failed to export to '%s'" %(path))
                return
    else:
        for channel in channels:
            try:
                channel.exportImages(path, save_options)
            except:
                mari.utils.message("IOError: Failed to export to '%s'" %(path))
                return
    #If successful let the user know
    mari.utils.message("Export Successful")
    
# ------------------------------------------------------------------------------ 
def exportEverything(path, flattened, small_textures):
    "Export everything, all geo and all channels"
    geo_list = mari.geo.list()
    channels = []
    for geo in geo_list:
        channels.extend(geo.channelList())
    save_options = 1
    if small_textures:
        save_options = 0
    #Check if export flattened is ticked, if not export unflattened
    if flattened:
        for channel in channels:
            try:
                channel.exportImagesFlattened(path, save_options)
            except:
                mari.utils.message("IOError: Failed to export to '%s'" %(path))
                return
    else:
        for channel in channels:
            try:
                channel.exportImages(path, save_options)
            except:
                mari.utils.message("IOError: Failed to export to '%s'" %(path))
                return
    #If successful let the user know
    mari.utils.message("Export Successful")

# ------------------------------------------------------------------------------
def exportSelectedChannels():
    "Export selected channels."
    if not isProjectSuitable():
        return
    
    #Create dialog and execute accordingly
    dialog = ExportSelectedChannelsGUI()
    if dialog.exec_():
        channels = dialog.getChannelsToExport()
        path = dialog.getExportPathTemplate()
        flattened = dialog.getExportFlattened()
        small_textures = dialog.getExportSmallTextures()
        if dialog.getExportEverything():
            exportEverything(path, flattened, small_textures)
        else:
            exportChannels(channels, path, flattened, small_textures)
    
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
    exportSelectedChannels()