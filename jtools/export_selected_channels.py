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
import PythonQt

version = "0.01"

gui = PythonQt.QtGui

USER_ROLE_01 = 34          # PythonQt.Qt.UserRole
USER_ROLE_02 = 34          # PythonQt.Qt.UserRole

current_geometry = ""

g_esc_window = None

# ------------------------------------------------------------------------------
# Create main UI
# ------------------------------------------------------------------------------

def showUI():
    "Export channels from one or more objects."
    if not isProjectSuitable():
        return False
    #Create main dialog, add main layout and set title
    global g_esc_window
    g_esc_window = gui.QDialog()
    ec_layout = gui.QVBoxLayout()
    g_esc_window.setLayout(ec_layout)
    g_esc_window.setWindowTitle("Export Channels")
    
    #Create layout for top section
    top_layout = gui.QHBoxLayout()
    
    #Create geometrys layout, label, and widget. Finally populate.
    geometry_layout = gui.QVBoxLayout()
    geometry_header_layout = gui.QHBoxLayout()
    geometry_label = gui.QLabel("Geometry")
    setBold(geometry_label)
    geometry_list = gui.QListWidget()
    
    filter_geometry_box = gui.QLineEdit()
    mari.utils.connect(filter_geometry_box.textEdited, lambda: updateGeometryFilter(filter_geometry_box, geometry_list))
    
    geometry_header_layout.addWidget(geometry_label)
    geometry_header_layout.addStretch()
    geometry_search_icon = gui.QLabel()
    search_pixmap = gui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
    geometry_search_icon.setPixmap(search_pixmap)
    geometry_header_layout.addWidget(geometry_search_icon)
    geometry_header_layout.addWidget(filter_geometry_box)
    
    geo_list = mari.geo.list()
    for geometry in geo_list:
        geometry_list.addItem(geometry.name())
        geometry_list.item(geometry_list.count - 1).setData(USER_ROLE_01, geometry)
    
    #Set the first geometry in the list to selected
    geometry_list.setCurrentRow(0)
    
    geometry_layout.addLayout(geometry_header_layout)
    geometry_layout.addWidget(geometry_list)

# -----------------------------------------------------------------------------------------------------
    
    #Create channels layout, label, and widget. Finally populate.
    channel_layout = gui.QVBoxLayout()
    channel_header_layout = gui.QHBoxLayout()
    channel_label = gui.QLabel("Channels")
    setBold(channel_label)
    channel_list = gui.QListWidget()
    channel_list.setSelectionMode(channel_list.ExtendedSelection)
       
    filter_channel_box = gui.QLineEdit()
    mari.utils.connect(filter_channel_box.textEdited, lambda: updateChannelFilter(filter_channel_box, channel_list))
        
    channel_header_layout.addWidget(channel_label)
    channel_header_layout.addStretch()
    channel_search_icon = gui.QLabel()
    search_pixmap = gui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
    channel_search_icon.setPixmap(search_pixmap)
    channel_header_layout.addWidget(channel_search_icon)
    channel_header_layout.addWidget(filter_channel_box)
    
    def channelList(channels):
        channel_list.clear()
        for channel in channels:
            channel_list.addItem(channel.name())
            channel_list.item(channel_list.count - 1).setData(USER_ROLE_02, channel)
        
    channel_layout.addLayout(channel_header_layout)
    channel_layout.addWidget(channel_list)    

# -----------------------------------------------------------------------------------------------------    
    
    #Create middle button section
    middle_right_button_layout = gui.QVBoxLayout()
    add_channel_button = gui.QPushButton("+")
    remove_channel_button = gui.QPushButton("-")
    middle_right_button_layout.addStretch()
    middle_right_button_layout.addWidget(add_channel_button)
    middle_right_button_layout.addWidget(remove_channel_button)
    middle_right_button_layout.addStretch()
    
    #Add wrapped gui.QListWidget with custom functions
    channels_to_export_layout = gui.QVBoxLayout()
    channels_to_export_label = gui.QLabel("Channels To Export")
    setBold(channels_to_export_label)
    channels_to_export_widget = ChannelsToExportList()
    channels_to_export_layout.addWidget(channels_to_export_label)
    channels_to_export_layout.addWidget(channels_to_export_widget)
    
    #Hook up add/remove buttons
    remove_channel_button.connect("clicked()", channels_to_export_widget.removeChannels)
    add_channel_button.connect("clicked()", lambda: channels_to_export_widget.addChannels(channel_list))

    #Add widgets to top layout
    top_layout.addLayout(geometry_layout)
    top_layout.addLayout(channel_layout)
    top_layout.addLayout(middle_right_button_layout)
    top_layout.addLayout(channels_to_export_layout)

    #Add top layout to main layout
    ec_layout.addLayout(top_layout)    
    
# -----------------------------------------------------------------------------------------------------    
    
    #Connect the geomtry_list item changed signal to currentGeometry function, this is to refresh the channel list
    geo_object = geometry_list.item(geometry_list.count - 1)
    geometry_list.connect("itemSelectionChanged()", lambda: getCurrentGeometry(geometry_list))
    
    #Get the current selected geometry from the list
    def getCurrentGeometry(geometry_list):
        global current_geometry
        index = geometry_list.currentIndex().row()
        object = geometry_list.item(index)
        geometry = object.data(USER_ROLE_01)
        current_geometry = geometry.name()
        channels = geometry.channelList()
        channelList(channels)
        
    #Start the geometry selection channel return
    getCurrentGeometry(geometry_list)
    
# -----------------------------------------------------------------------------------------------------    
    
    #Add middle layout.
    middle_layout = gui.QHBoxLayout()
    export_everything_box = gui.QCheckBox('Export Everything')
    export_everything_box.connect("clicked()", lambda: exportEverything())

    #Hide parts of interface if export everything is ticked
    def exportEverything():
        _bool = export_everything_box.isChecked()
        geometry_label.setHidden(_bool)
        geometry_search_icon.setHidden(_bool)
        filter_geometry_box.setHidden(_bool)
        geometry_list.setHidden(_bool)
        channel_label.setHidden(_bool)
        channel_search_icon.setHidden(_bool)
        filter_channel_box.setHidden(_bool)
        channel_list.setHidden(_bool)
        add_channel_button.setHidden(_bool)
        remove_channel_button.setHidden(_bool)
        channels_to_export_label.setHidden(_bool)
        channels_to_export_widget.setHidden(_bool)
            
    #Add to middle layout    
    middle_layout.addWidget(export_everything_box)
    #Add to main layout
    ec_layout.addLayout(middle_layout)
    
    #Add bottom layout.
    bottom_layout = gui.QHBoxLayout()
    
    #Add path line input and button
    path_label = gui.QLabel('Path:')
    path_line_edit = gui.QLineEdit()
    path_pixmap = gui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
    icon = gui.QIcon(path_pixmap)
    path_button = gui.QPushButton(icon, "")
    path_button.connect("clicked()", lambda: getPath())
    
    #Get the path from existing directory
    def getPath():
        path = mari.utils.misc.getExistingDirectory(parent=None, caption='Export Path', dir='')
        if path == "":
            return False
        
        path = os.path.abspath(path)
        path_line_edit.setText(path)
        
    #Add export option check boxes
    export_flattened_box = gui.QCheckBox('Export Flattened')
    export_small_textures_box = gui.QCheckBox('Small Textures')
    
    #Add OK Cancel buttons layout, buttons and add
    main_ok_button = gui.QPushButton("OK")
    main_cancel_button = gui.QPushButton("Cancel")
    main_ok_button.connect("clicked()", lambda: compareInput(g_esc_window, path_line_edit, export_everything_box, export_flattened_box, export_small_textures_box, channels_to_export_widget))
    main_cancel_button.connect("clicked()", g_esc_window.reject)
    
    bottom_layout.addWidget(path_label)
    bottom_layout.addWidget(path_line_edit)
    bottom_layout.addWidget(path_button)
    bottom_layout.addWidget(export_flattened_box)
    bottom_layout.addWidget(export_small_textures_box)
    bottom_layout.addWidget(main_ok_button)
    bottom_layout.addWidget(main_cancel_button)
    
    #Add browse lines to main layout
    ec_layout.addLayout(bottom_layout)
    
    # Display
    g_esc_window.show()
    
# ------------------------------------------------------------------------------ 
def exportChannels(g_esc_window, path_line_edit, export_flattened_box, export_small_textures_box, channels_to_export_widget):
    channels = channels_to_export_widget.currentChannels()
    save_options = 1
    if export_small_textures_box.isChecked():
        save_options = 0
    success = False
    #Check if export flattened is ticked, if not export unflattened
    if export_flattened_box.isChecked():
        for channel in channels:
            try:
                channel.exportImagesFlattened(path_line_edit.text, save_options)
            except:
                mari.utils.message("IOError: Export failed: Exporting to '%s' files is not supported" %(path_line_edit.text))
                break
            success = True
    else:
        for channel in channels:
            try:
                channel.exportImages(path_line_edit.text, save_options)
            except:
                mari.utils.message("IOError: Export failed: Exporting to '%s' files is not supported" %(path_line_edit.text))
                break
            success = True
    #If successful let the user know and close window
    if success:
        mari.utils.message("Export Successful")
        g_esc_window.accept()
    
# ------------------------------------------------------------------------------ 
def exportEverything(g_esc_window, path_line_edit, export_flattened_box, export_small_textures_box):
    "Export everything, all geo and all channels"
    geo_list = mari.geo.list()
    channels = []
    for geo in geo_list:
        channels.extend(geo.channelList())
    save_options = 1
    if export_small_textures_box.isChecked():
        save_options = 0
    success = False
    #Check if export flattened is ticked, if not export unflattened
    if export_flattened_box.isChecked():
        for channel in channels:
            try:
                channel.exportImagesFlattened(path_line_edit.text, save_options)
            except:
                mari.utils.message("Export failed: Exporting to '%s' files is not supported" %(path_line_edit.text))
                break
            success = True
    else:
        for channel in channels:
            try:
                channel.exportImages(path_line_edit.text, save_options)
            except:
                mari.utils.message("Export failed: Exporting to '%s' files is not supported" %(path_line_edit.text))
                break
            success = True
    #If successful let the user know and close window
    if success:
        mari.utils.message("Export Successful")
        g_esc_window.accept()
                
# ------------------------------------------------------------------------------ 
def compareInput(g_esc_window, path_line_edit, export_everything_box, export_flattened_box, export_small_textures_box, channels_to_export_widget):
    "Compare the input from the gui"
    if export_everything_box.isChecked():
        exportEverything(g_esc_window, path_line_edit, export_flattened_box, export_small_textures_box)
    else:
        #If no channels in export list tell user and stop
        if len(channels_to_export_widget.currentChannels()) == 0:
            mari.utils.message("Please add a channel to export")
            return False
        exportChannels(g_esc_window, path_line_edit, export_flattened_box, export_small_textures_box, channels_to_export_widget)

# ------------------------------------------------------------------------------   
class ChannelsToExportList(gui.QListWidget):
    "Stores a list of operations to perform."
    
    def __init__(self, title="For Export"):
        super(ChannelsToExportList, self).__init__()
        self._title = title
        self.setSelectionMode(self.ExtendedSelection)
        
    def currentChannels(self):
        return [self.item(index).data(USER_ROLE_02) for index in range(self.count)]
        
    def addChannels(self, channel_list):
        "Adds an operation from the current selections of channels and directories."
        selected_items = channel_list.selectedItems()
        if selected_items == []:
            mari.utils.message("Please select at least one channel.")
            return
        
        # Add channels that aren't already added
        current_channels = set(self.currentChannels())
        for item in selected_items:
            channel = item.data(USER_ROLE_02)
            if channel not in current_channels:
                current_channels.add(channel)
                self.addItem(current_geometry + ":" + channel.name())
                self.item(self.count - 1).setData(USER_ROLE_02, channel)
        
    def removeChannels(self):
        "Removes any currently selected operations."
        for item in reversed(self.selectedItems()):     # reverse so indices aren't modified
            index = self.row(item)
            self.takeItem(index)    
    
# ------------------------------------------------------------------------------
def updateGeometryFilter(filter_geometry_box, geometry_list):
    "For each item in the channel list display, set it to hidden if it doesn't match the filter text."
    match_words = filter_geometry_box.text.lower().split()
    for item_index in range(geometry_list.count):
        item = geometry_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)

# ------------------------------------------------------------------------------
def updateChannelFilter(filter_channel_box, channel_list):
    "For each item in the channel list display, set it to hidden if it doesn't match the filter text."
    match_words = filter_channel_box.text.lower().split()
    for item_index in range(channel_list.count):
        item = channel_list.item(item_index)
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
    showUI()