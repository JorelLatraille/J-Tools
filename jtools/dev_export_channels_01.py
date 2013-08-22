# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Export channels from one or more objects
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

import mari
import PythonQt

version = "0.01"

gui = PythonQt.QtGui

USER_ROLE_01 = 34          # PythonQt.Qt.UserRole
USER_ROLE_02 = 34          # PythonQt.Qt.UserRole

g_ec_window = None
g_ec_cancelled = False

# ------------------------------------------------------------------------------

class UserCancelledException(Exception):
    pass

# ------------------------------------------------------------------------------
# Create main UI
# ------------------------------------------------------------------------------

def showUI():
    "Export channels from one or more objects."
    
    #Create main dialog, add main layout and set title
    global g_ec_window
    g_ec_window = gui.QDialog()
    ec_layout = gui.QVBoxLayout()
    g_ec_window.setLayout(ec_layout)
    g_ec_window.setWindowTitle("Export Channels")
    
    #Create layout for middle section
    centre_layout = gui.QHBoxLayout()
    
    #Create channels layout, label, and widget. Finally populate.
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

    #Add widgets to centre layout
    centre_layout.addLayout(geometry_layout)
    centre_layout.addLayout(channel_layout)
    centre_layout.addLayout(middle_right_button_layout)
    centre_layout.addLayout(channels_to_export_layout)

    #Add centre layout to main layout
    ec_layout.addLayout(centre_layout)    
        
    geo_object = geometry_list.item(geometry_list.count - 1)
    geometry_list.connect("itemSelectionChanged()", lambda: getCurrentGeometry(geometry_list))
    
    def getCurrentGeometry(geometry_list):
        index = geometry_list.currentIndex().row()
        object = geometry_list.item(index)
        geometry = object.data(USER_ROLE_01)
        channels = geometry.channelList()
        channelList(channels)
        
    getCurrentGeometry(geometry_list)
    
    # Display
    g_ec_window.show()

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
                self.addItem(channel.name())
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
if __name__ == "__main__":
    showUI()