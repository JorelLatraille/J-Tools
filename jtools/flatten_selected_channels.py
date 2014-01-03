# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Duplicate and flatten selected channels
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

import mari
import PythonQt.QtGui as QtGui

version = "0.03"

USER_ROLE = 32          # PythonQt.Qt.UserRole

# ------------------------------------------------------------------------------       
class FlattenSelectedChannelsGUI(QtGui.QDialog):
    "Create main UI."
    def __init__(self, parent=None):
        super(FlattenSelectedChannelsGUI, self).__init__(parent)

        #Set window title and create a main layout
        self.setWindowTitle("Flatten Selected Channels")
        main_layout = QtGui.QVBoxLayout()
        
        #Create layout for middle section
        centre_layout = QtGui.QHBoxLayout()
        
        #Create channel layout, label, and widget. Finally populate.
        channel_layout = QtGui.QVBoxLayout()
        channel_header_layout = QtGui.QHBoxLayout()
        channel_label = QtGui.QLabel("Channels")
        setBold(channel_label)
        channel_list = QtGui.QListWidget()
        channel_list.setSelectionMode(channel_list.ExtendedSelection)
        
        #Create filter box for channel list
        channel_filter_box = QtGui.QLineEdit()
        mari.utils.connect(channel_filter_box.textEdited, lambda: updateChannelFilter(channel_filter_box, channel_list))
        
        #Create layout and icon/label for channel filter
        channel_header_layout.addWidget(channel_label)
        channel_header_layout.addStretch()
        channel_search_icon = QtGui.QLabel()
        search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
        channel_search_icon.setPixmap(search_pixmap)
        channel_header_layout.addWidget(channel_search_icon)
        channel_header_layout.addWidget(channel_filter_box)
        
        #Populate geo : channel list widget
        geo_list = mari.geo.list()
        chan_list = []
        for geo in geo_list:
            chan_list.append((geo.name(), geo.channelList()))
        for item in chan_list:
            for channel in item[1]:
                channel_list.addItem(item[0] + ' : ' + channel.name())
                channel_list.item(channel_list.count - 1).setData(USER_ROLE, channel)
        
        #Add filter layout and channel list to channel layout
        channel_layout.addLayout(channel_header_layout)
        channel_layout.addWidget(channel_list)
        
        #Create middle button section
        middle_button_layout = QtGui.QVBoxLayout()
        add_button = QtGui.QPushButton("+")
        remove_button = QtGui.QPushButton("-")
        middle_button_layout.addStretch()
        middle_button_layout.addWidget(add_button)
        middle_button_layout.addWidget(remove_button)
        middle_button_layout.addStretch()
        
        #Add wrapped QtGui.QListWidget with custom functions
        flatten_layout = QtGui.QVBoxLayout()
        flatten_header_layout = QtGui.QHBoxLayout()
        flatten_label = QtGui.QLabel("Channels To Flatten")
        setBold(flatten_label)
        self.flatten_list = ChannelsToFlattenList()
        self.flatten_list.setSelectionMode(self.flatten_list.ExtendedSelection)
        
        #Create filter box for flatten list
        flatten_filter_box = QtGui.QLineEdit()
        mari.utils.connect(flatten_filter_box.textEdited, lambda: updateFlattenFilter(flatten_filter_box, self.flatten_list))
        
        #Create layout and icon/label for flatten filter
        flatten_header_layout.addWidget(flatten_label)
        flatten_header_layout.addStretch()
        flatten_search_icon = QtGui.QLabel()
        flatten_search_icon.setPixmap(search_pixmap)
        flatten_header_layout.addWidget(flatten_search_icon)
        flatten_header_layout.addWidget(flatten_filter_box)
        
        #Add filter layout and flatten list to flatten layout
        flatten_layout.addLayout(flatten_header_layout)
        flatten_layout.addWidget(self.flatten_list)
        
        #Hook up add/remove buttons
        remove_button.connect("clicked()", self.flatten_list.removeChannels)
        add_button.connect("clicked()", lambda: self.flatten_list.addChannels(channel_list))

        #Add widgets to centre layout
        centre_layout.addLayout(channel_layout)
        centre_layout.addLayout(middle_button_layout)
        centre_layout.addLayout(flatten_layout)
        
        #Create button layout and hook them up
        button_layout = QtGui.QHBoxLayout()
        ok_button = QtGui.QPushButton("&OK")
        cancel_button = QtGui.QPushButton("&Cancel")
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        #Hook up OK/Cancel button clicked signal to accept/reject slot
        ok_button.connect("clicked()", self.accept)
        cancel_button.connect("clicked()", self.reject)
        
        #Add layouts to main layout and dialog
        main_layout.addLayout(centre_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        
    def getChannelsToFlatten(self):
        return self.flatten_list.currentChannels()
    
# ------------------------------------------------------------------------------   
class ChannelsToFlattenList(QtGui.QListWidget):
    "Stores a list of operations to perform."
    
    def __init__(self, title="For Export"):
        super(ChannelsToFlattenList, self).__init__()
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
def updateFlattenFilter(flatten_filter_box, flatten_list):
    "For each item in the flatten list display, set it to hidden if it doesn't match the filter text."
    match_words = flatten_filter_box.text.lower().split()
    for item_index in range(flatten_list.count):
        item = flatten_list.item(item_index)
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
        
        geo_list = mari.geo.list()
        for geo in geo_list:
            channel_list = geo.channelList()
            if channel_list == 0:
                mari.utils.message("Please ensure all objects have at least one channel.")
                return False

        return True
    
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False

# ------------------------------------------------------------------------------                  
def flattenSelectedChannels():
    "Duplicate and flatten selected channels."
    if not isProjectSuitable():
        return
    
    #Create dialog and execute accordingly
    dialog = FlattenSelectedChannelsGUI()
    if dialog.exec_():
        channels_to_flatten = dialog.getChannelsToFlatten()
        
        for channel in channels_to_flatten:
            orig_name = channel.name()
            geo = channel.geoEntity()
            flatten_channel = geo.createDuplicateChannel(channel, channel.name() + '_flatten')
            flatten_channel.flatten()
            channel.setName(channel.name() + '_original')
            flatten_channel.setName(orig_name)
    
# ------------------------------------------------------------------------------            
if __name__ == "__main__":
    flattenSelectedChannels()