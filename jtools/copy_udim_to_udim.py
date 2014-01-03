# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Copy paint from one or more patches to other patches, for all layers and channels
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

g_u2u_window = None
g_u2u_cancelled = False

# ------------------------------------------------------------------------------

g_debug = False

def debugMsg(message):
    if g_debug:
        print message

# ------------------------------------------------------------------------------

class UserCancelledException(Exception):
    pass

# ------------------------------------------------------------------------------
# Create main UI
# ------------------------------------------------------------------------------

def showUI():
    "Copy paint from one or more patches to other patches, for all layers and channels."
    #Create UI
    
    #Check project state
    if not isProjectSuitable():
        return False
    
    #Create main dialog, add main layout and set title
    global g_u2u_window
    g_u2u_window = QtGui.QDialog()
    u2u_layout = QtGui.QVBoxLayout()
    g_u2u_window.setLayout(u2u_layout)
    g_u2u_window.setWindowTitle("Copy Udim To Udim")
    
    #Create layout for middle section
    centre_layout = QtGui.QHBoxLayout()
    
    #Create channels layout, label, and widget. Finally populate.
    channel_layout = QtGui.QVBoxLayout()
    channel_header_layout = QtGui.QHBoxLayout()
    channel_label = QtGui.QLabel("Channels")
    setBold(channel_label)
    channel_list = QtGui.QListWidget()
    channel_list.setSelectionMode(channel_list.ExtendedSelection)
    
    filter_box = QtGui.QLineEdit()
    mari.utils.connect(filter_box.textEdited, lambda: updateFilter(filter_box, channel_list))
    
    channel_header_layout.addWidget(channel_label)
    channel_header_layout.addStretch()
    channel_search_icon = QtGui.QLabel()
    search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
    channel_search_icon.setPixmap(search_pixmap)
    channel_header_layout.addWidget(channel_search_icon)
    channel_header_layout.addWidget(filter_box)
    
    geo = mari.geo.current()
    for channel in getChannelList(geo):
        channel_list.addItem(channel.name())
        channel_list.item(channel_list.count - 1).setData(USER_ROLE, channel)
    
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
    channels_to_copy_layout = QtGui.QVBoxLayout()
    channels_to_copy_label = QtGui.QLabel("Channels To Run Copy On")
    setBold(channels_to_copy_label)
    channels_to_copy_widget = ChannelsToCopyList()
    channels_to_copy_layout.addWidget(channels_to_copy_label)
    channels_to_copy_layout.addWidget(channels_to_copy_widget)
    
    #Hook up add/remove buttons
    remove_button.connect("clicked()", channels_to_copy_widget.removeChannels)
    add_button.connect("clicked()", lambda: channels_to_copy_widget.addChannels(channel_list))

    #Add widgets to centre layout
    centre_layout.addLayout(channel_layout)
    centre_layout.addLayout(middle_button_layout)
    centre_layout.addLayout(channels_to_copy_layout)

    #Add centre layout to main layout
    u2u_layout.addLayout(centre_layout)
    
    #Add bottom layout.
    bottom_layout = QtGui.QHBoxLayout()
    
    unlock_channels_box = QtGui.QCheckBox('Unlock channels')
    uncache_layers_box = QtGui.QCheckBox('Uncache layers')
    unlock_layers_box = QtGui.QCheckBox('Unlock layers')
    
    bottom_layout.addWidget(unlock_channels_box)
    bottom_layout.addStretch()
    bottom_layout.addWidget(uncache_layers_box)
    bottom_layout.addStretch()
    bottom_layout.addWidget(unlock_layers_box)
    bottom_layout.addStretch()
    
    u2u_layout.addLayout(bottom_layout)

    #Add very bottom layout.
    very_bottom_layout = QtGui.QHBoxLayout()
    
    #Create copy/paste text labels
    copy_from_text = QtGui.QLabel("Copy from UDIM")
    setBold(copy_from_text)
    paste_to_text = QtGui.QLabel("Paste to UDIM")
    setBold(paste_to_text)
    
    #Create copy layout and add widgets
    copy_line_layout = QtGui.QHBoxLayout()
    # global copy_line
    copy_line_layout.addWidget(copy_from_text)
    copy_line = QtGui.QLineEdit()
    copy_line_layout.addWidget(copy_line)
    
    #Create paste layout and add widgets
    paste_line_layout = QtGui.QHBoxLayout()
    # global paste_line
    paste_line_layout.addWidget(paste_to_text)
    paste_line = QtGui.QLineEdit()
    paste_line_layout.addWidget(paste_line)
    
    #Add OK Cancel buttons layout, buttons and add
    main_ok_button = QtGui.QPushButton("OK")
    main_cancel_button = QtGui.QPushButton("Cancel")
    main_ok_button.connect("clicked()", lambda: compareInput(g_u2u_window, channels_to_copy_widget, unlock_channels_box, uncache_layers_box, unlock_layers_box, copy_line, paste_line))
    main_cancel_button.connect("clicked()", g_u2u_window.reject)
    uncache_layers_box.connect("clicked()", lambda: uncacheBoxTicked(uncache_layers_box))
    
    very_bottom_layout.addLayout(copy_line_layout)
    very_bottom_layout.addLayout(paste_line_layout)
    very_bottom_layout.addWidget(main_ok_button)
    very_bottom_layout.addWidget(main_cancel_button)
    
    #Add browse lines to main layout
    u2u_layout.addLayout(very_bottom_layout)
    
    # Display
    g_u2u_window.show()

# ------------------------------------------------------------------------------   
def uncacheBoxTicked(uncache_layers_box):
    "Warning message for uncache tick box."
    if uncache_layers_box.isChecked():
        mari.utils.message("Please be aware that uncaching and re-caching the layers could take some time")
    
# ------------------------------------------------------------------------------   
class ChannelsToCopyList(QtGui.QListWidget):
    "Stores a list of operations to perform."
    
    def __init__(self, title="For Export"):
        super(ChannelsToCopyList, self).__init__()
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
                self.addItem(channel.name())
                self.item(self.count - 1).setData(USER_ROLE, channel)
        
    def removeChannels(self):
        "Removes any currently selected operations."
        for item in reversed(self.selectedItems()):     # reverse so indices aren't modified
            index = self.row(item)
            self.takeItem(index)    

# ------------------------------------------------------------------------------     
def checkBox(ui, channels_to_copy, unlock_channels_box, uncache_layers_box, unlock_layers_box, copy_udim_list, paste_udim_list):
    "This is where the check boxes are queried and where lists are generated for functions."
    unlock_channels = unlock_channels_box.isChecked()
    uncache_layers = uncache_layers_box.isChecked()
    unlock_layers = unlock_layers_box.isChecked()
    
    channels_to_copy_list = channels_to_copy.currentChannels()

    channels_locked = []
    layers_locked = []
    layers_cached = []
    
    if unlock_channels:
        for channel in channels_to_copy_list:
            channels_locked.extend(getLockedChannels(channels_to_copy_list))
        unlockOrLockList(channels_locked, False)
    
    if uncache_layers:
        for channel in channels_to_copy_list:
            layers_cached.extend(getCachedLayers(channel.layerList()))
        uncacheOrCacheList(layers_cached, False)
    
    if (unlock_layers == True) and (uncache_layers == False):
        for channel in channels_to_copy_list:
            layers_locked.extend(getLockedLayers(channel.layerList()))
            layers_cached.extend(getCachedLayers(channel.layerList()))
        for layer in layers_locked:
            if layer in layers_cached:
                layers_locked.remove(layer)
        unlockOrLockList(layers_locked, False)
        
    elif unlock_layers:
        for channel in channels_to_copy_list:
            layers_locked.extend(getLockedLayers(channel.layerList()))
        unlockOrLockList(layers_locked, False)
        
    copy_udim_list = udimToIndex(copy_udim_list)
    paste_udim_list = udimToIndex(paste_udim_list)

    whatToCopy(channels_to_copy_list, copy_udim_list, paste_udim_list, unlock_channels, uncache_layers, unlock_layers)

    if len(layers_cached) == 0:
        pass
    else:
        uncacheOrCacheList(layers_cached, True)
    
    if len(layers_locked) == 0:
        pass
    else:
        unlockOrLockList(layers_locked, True)
            
    if len(channels_locked) == 0:
        pass
    else:
        unlockOrLockList(channels_locked, True)
            
    #Close Qt dialog
    ui.accept()

# ------------------------------------------------------------------------------
def whatToCopy(channels_to_copy_list, copy_udim_list, paste_udim_list, unlock_channels, uncache_layers, unlock_layers):
    "Checks channel list against tick boxes and runs copy accordingly"
    channels_to_copy = channels_to_copy_list
    
    if unlock_channels and uncache_layers and unlock_layers:
        for channel in channels_to_copy:
            layer_list = getMatchingLayers(channel.layerList(), returnTrue)
            maskToMaskStack(layer_list)
            layer_list = getMatchingLayers(channel.layerList(), returnTrue)
            layer_list = getPaintableLayers(layer_list)
            copyUdimToUdim(copy_udim_list, paste_udim_list, layer_list)
            
    if unlock_channels and uncache_layers or not uncache_layers and unlock_layers or not unlock_layers:
        for channel in channels_to_copy:
            layer_list = getMatchingLayers(channel.layerList(), returnTrue)
            layer_list = getModifiableLayers(layer_list)
            layer_list = maskToMaskStack(layer_list)
            layer_list = getPaintableLayers(layer_list)
            copyUdimToUdim(copy_udim_list, paste_udim_list, layer_list)
            
    if not unlock_channels and uncache_layers or not uncache_layers and unlock_layers or not unlock_layers:
        channels_locked = getLockedChannels(channels_to_copy)
        for channel in channels_to_copy:
            if channel in channels_locked:
                channels_to_copy.remove(channel)
        for channel in channels_to_copy:
            layer_list = getMatchingLayers(channel.layerList(), returnTrue)
            layer_list = getModifiableLayers(layer_list)
            layer_list = maskToMaskStack(layer_list)
            layer_list = getPaintableLayers(layer_list)
            copyUdimToUdim(copy_udim_list, paste_udim_list, layer_list)
            
# ------------------------------------------------------------------------------  
def copyUdimRange(layer_list, copy_udim_list, paste_udim_list):
            "Pass each udim and layer list to the copyUdimToUdim function"
            for index in range(len(copy_udim_list)):
                copyUdimToUdim(copy_udim_list[index], paste_udim_list[index], layer_list)
       
# ------------------------------------------------------------------------------  
def compareInput(g_u2u_window, channels_to_copy, unlock_channels_box, uncache_layers_box, unlock_layers_box, copy_line, paste_line):
    "Check copy and paste input from the dialog are udim numbers i.e. 1001 - 9999, and not alphabetical, they can contain multiple ranges and individual udims i.e. 1001-1005,1006,1009,1021-1030"

    copy_line = copy_line.text
    paste_line = paste_line.text
    copy_list = copy_line.split(',')
    paste_list = paste_line.split(',')           
    copy_udim_check = []
    paste_udim_check = []
    copy_udim_list = []
    paste_udim_list = []
    check_list = []
    check = False
    
    for item in copy_list:
        if '-' in item:
            item_list = item.split('-')
            ranges = []
            for item in item_list:
                if item.isdigit() and int(item) >= 1001 and len(item) == 4:
                    ranges.append(int(item))
                else:
                    check_list.append(False)
            ranges.sort()
            range_list = range(ranges[0], ranges[1] + 1)
            copy_udim_check.append(len(range_list))
            copy_udim_list.extend(range_list)
        elif item.isdigit() and len(item) == 4 and int(item) >= 1001:
            copy_udim_check.append(1)
            copy_udim_list.append(int(item))
        else:
            check_list.append(False)
       
    for item in paste_list:
        if '-' in item:
            item_list = item.split('-')
            ranges = []
            for item in item_list:
                if item.isdigit() and int(item) >= 1001 and len(item) == 4:
                    ranges.append(int(item))
                else:
                    check_list.append(False)
            ranges.sort()
            range_list = range(ranges[0], ranges[1] + 1)
            paste_udim_check.append(len(range_list))
            paste_udim_list.extend(range_list)
        elif item.isdigit() and len(item) == 4 and int(item) >= 1001:
            paste_udim_check.append(1)
            paste_udim_list.append(int(item))
        else:
            check_list.append(False)

    if len(copy_udim_check) == len(paste_udim_check):
        for i in range(len(copy_udim_check)):
            if copy_udim_check[i] == paste_udim_check[i]:
                check_list.append(True)
            else:
                check_list.append(False)
    
    if len(check_list) == 0:
        check = False
    elif False in check_list:
        check = False
    else:
        check = True
        
    if check == False:
        mari.utils.message("Please enter matching UDIM ranges for copying, i.e. Copy UDIM: 1001-1005,1009 Paste UDIM: 1016-1020,1032")
    else:
        checkBox(g_u2u_window, channels_to_copy, unlock_channels_box, unlock_layers_box, uncache_layers_box, copy_udim_list, paste_udim_list)
        
# ------------------------------------------------------------------------------  
def udimToIndex(udim_list):
    "Converts udim number to index number"
    index_list = []
    
    for udim in udim_list:
        index_list.append(udim - 1001)
    
    return index_list

# ------------------------------------------------------------------------------  
def unlockOrLockList(List, bool):
    "Unlocks or locks list of channels/layers depending on what is passed to it."
    for obj in List:
        obj.setLocked(bool)
        
# ------------------------------------------------------------------------------
def uncacheOrCacheList(List, bool):
    "Uncaches or caches a list of layers."
    uncache = mari.actions.get('/Mari/Layers/Uncache Layer')
    cache = mari.actions.get('/Mari/Layers/Cache Layer')
    if bool:
        for layer in List:
            layer.makeCurrent()
            cache.trigger()
    else:
        for layer in List:
            layer.makeCurrent()
            uncache.trigger()

# ------------------------------------------------------------------------------  
def getLockedChannels(channel_list):
    "Returns a list of all the locked channels."
    matching = []
    for channel in channel_list:
        if channel.isLocked():
            matching.append(channel)
            
    return matching
    
# ------------------------------------------------------------------------------
def getCachedLayers(layer_list):
    "Returns a list of all of the cached layers in the layer stack, including in substacks."
    return getMatchingLayers(layer_list, mari.Layer.isLayerCached)

# ------------------------------------------------------------------------------
def getLockedLayers(layer_list):
    "Returns a list of all of the locked layers in the layer stack, including in substacks."
    return getMatchingLayers(layer_list, mari.Layer.isLocked)

# ------------------------------------------------------------------------------
def getPaintableLayers(layer_list):
    "Returns a list of all of the paintable layers in the layer stack, including in substacks."
    return getMatchingLayers(layer_list, mari.Layer.isPaintableLayer)
    
# ------------------------------------------------------------------------------
def getModifiableLayers(layer_list):
    "Returns a list of all of the modifiable layers in the layer stack, including in substacks."
    return getMatchingLayers(layer_list, mari.Layer.isModifiable)

# ------------------------------------------------------------------------------    
def returnTrue(layer):
    "Returns True for any object passed to it."
    return True

# ------------------------------------------------------------------------------
def getMatchingLayers(layer_list, criterionFn):
    "Returns a list of all of the layers in the stack that match the given criterion function, including substacks."
    matching = []
    for layer in layer_list:
        if criterionFn(layer):
            matching.append(layer)
        if hasattr(layer, 'layerStack'):
            matching.extend(getMatchingLayers(layer.layerStack().layerList(), criterionFn))
        if layer.hasMaskStack():
            matching.extend(getMatchingLayers(layer.maskStack().layerList(), criterionFn))
        if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
            matching.extend(getMatchingLayers(layer.adjustmentStack().layerList(), criterionFn))
        
    return matching

# ------------------------------------------------------------------------------
def maskToMaskStack(layer_list):
    "Returns a list of all of the layers in the stack that match the given criterion function, including substacks."
    matching = []
    for layer in layer_list:
        matching.append(layer)
        if layer.hasMask() and (layer.hasMaskStack() == False):
            layer.makeMaskStack()
            matching.extend(maskToMaskStack(layer.maskStack().layerList()))
            
    return matching

# ------------------------------------------------------------------------------
def updateFilter(filter_box, channel_list):
    "For each item in the channel list display, set it to hidden if it doesn't match the filter text."
    match_words = filter_box.text.lower().split()
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
            
        geo = mari.geo.current()
        if geo is None:
            mari.utils.message("Please select an object to copy from.")
            return False
        
        chan = geo.currentChannel()
        if chan is None:
            mari.utils.message("Please select a channel to copy from.")
            return False
            
        if len(chan.layerList()) == 0:
            mari.utils.message("No layers to copy from!")
            return False

        return True
    
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False
    
# ------------------------------------------------------------------------------   
def copyUdimToUdim(copy_index, paste_index, layer_list):
    "Copies udim to udim."
    # un-select patches
    patches = mari.geo.current().selectedPatches()
    if patches == None:
        pass
    else:
        for patch in patches:
            patch.setSelected(False)
   
    copy = mari.actions.get('/Mari/Project/Project Explorer/Quick Copy')
    paste = mari.actions.get('/Mari/Project/Project Explorer/Quick Paste')
    
    for i in range(len(copy_index)):
        for layer in layer_list:
            # un-select layers
            layer.makeCurrent()
            layer.setSelected(False)
            
            layer.makeCurrent()
            mari.geo.current().patch(copy_index[i]).setSelected(True)
            copy.trigger()
            mari.geo.current().patch(copy_index[i]).setSelected(False)
            mari.geo.current().patch(paste_index[i]).setSelected(True)
            paste.trigger()
            mari.geo.current().patch(paste_index[i]).setSelected(False)
            layer.setSelected(False)
    
# ------------------------------------------------------------------------------
def getChannelList(geo):
    "Return a list of channels"
    channels = geo.channelList()
    return channels
    
# ------------------------------------------------------------------------------            
if __name__ == "__main__":
    showUI()