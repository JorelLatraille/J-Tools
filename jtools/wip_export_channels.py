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

USER_ROLE_01 = 34          # PythonQt.Qt.UserRolea
USER_ROLE_02 = 32          # PythonQt.Qt.UserRole

g_ec_window = None
g_ec_cancelled = False

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
    "Export channels from one or more objects."
    
    if not isProjectSuitable():
        return False
    
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
    geometry_list.setSelectionMode(geometry_list.ExtendedSelection)
    
    filter_box = gui.QLineEdit()
    mari.utils.connect(filter_box.textEdited, lambda: updateFilter(filter_box, geometry_list))
    
    geometry_header_layout.addWidget(geometry_label)
    geometry_header_layout.addStretch()
    geometry_search_icon = gui.QLabel()
    search_pixmap = gui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
    geometry_search_icon.setPixmap(search_pixmap)
    geometry_header_layout.addWidget(geometry_search_icon)
    geometry_header_layout.addWidget(filter_box)
    
    geo_list = mari.geo.list()
    for geometry in geo_list:
        geometry_list.addItem(geometry.name())
        geometry_list.item(geometry_list.count - 1).setData(USER_ROLE_01, geometry)
    
    geometry_layout.addLayout(geometry_header_layout)
    geometry_layout.addWidget(geometry_list)
    
    #Create middle button section
    middle_left_button_layout = gui.QVBoxLayout()
    add_geo_button = gui.QPushButton("+")
    remove_geo_button = gui.QPushButton("-")
    middle_left_button_layout.addStretch()
    middle_left_button_layout.addWidget(add_geo_button)
    middle_left_button_layout.addWidget(remove_geo_button)
    middle_left_button_layout.addStretch()
    
    #Add wrapped gui.QListWidget with custom functions
    geometry_to_export_layout = gui.QVBoxLayout()
    geometry_to_export_label = gui.QLabel("Channels To Export")
    setBold(geometry_to_export_label)
    geometry_to_export_widget = GeometryToExportList()
    geometry_to_export_layout.addWidget(geometry_to_export_label)
    geometry_to_export_layout.addWidget(geometry_to_export_widget)
    
    #Hook up add/remove buttons
    remove_geo_button.connect("clicked()", geometry_to_export_widget.removeGeometry)
    add_geo_button.connect("clicked()", lambda: geometry_to_export_widget.addGeometry(geometry_list))

    #Add widgets to centre layout
    centre_layout.addLayout(geometry_layout)
    centre_layout.addLayout(middle_left_button_layout)
    centre_layout.addLayout(geometry_to_export_layout)
    
# -----------------------------------------------------------------------------------------------------
    
    #Create channels layout, label, and widget. Finally populate.
    channel_layout = gui.QVBoxLayout()
    channel_header_layout = gui.QHBoxLayout()
    channel_label = gui.QLabel("Channels")
    setBold(channel_label)
    channel_list = gui.QListWidget()
    channel_list.setSelectionMode(channel_list.ExtendedSelection)
    
    filter_box = gui.QLineEdit()
    mari.utils.connect(filter_box.textEdited, lambda: updateFilter(filter_box, channel_list))
    
    channel_header_layout.addWidget(channel_label)
    channel_header_layout.addStretch()
    channel_search_icon = gui.QLabel()
    search_pixmap = gui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
    channel_search_icon.setPixmap(search_pixmap)
    channel_header_layout.addWidget(channel_search_icon)
    channel_header_layout.addWidget(filter_box)
    
    geo = mari.geo.current()
    channels = geo.channelList()
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
    centre_layout.addLayout(channel_layout)
    centre_layout.addLayout(middle_right_button_layout)
    centre_layout.addLayout(channels_to_export_layout)

    #Add centre layout to main layout
    ec_layout.addLayout(centre_layout)
    
    #Add bottom layout.
    bottom_layout = gui.QHBoxLayout()
    
    unlock_channels_box = gui.QCheckBox('Unlock channels')
    uncache_layers_box = gui.QCheckBox('Uncache layers')
    unlock_layers_box = gui.QCheckBox('Unlock layers')
    
    bottom_layout.addWidget(unlock_channels_box)
    bottom_layout.addStretch()
    bottom_layout.addWidget(uncache_layers_box)
    bottom_layout.addStretch()
    bottom_layout.addWidget(unlock_layers_box)
    bottom_layout.addStretch()
    
    ec_layout.addLayout(bottom_layout)

    #Add very bottom layout.
    very_bottom_layout = gui.QHBoxLayout()
    
    #Create export/paste text labels
    export_from_text = gui.QLabel("Copy from UDIM")
    setBold(export_from_text)
    paste_to_text = gui.QLabel("Paste to UDIM")
    setBold(paste_to_text)
    
    #Create export layout and add widgets
    export_line_layout = gui.QHBoxLayout()
    # global export_line
    export_line_layout.addWidget(export_from_text)
    export_line = gui.QLineEdit()
    export_line_layout.addWidget(export_line)
    
    #Create paste layout and add widgets
    paste_line_layout = gui.QHBoxLayout()
    # global paste_line
    paste_line_layout.addWidget(paste_to_text)
    paste_line = gui.QLineEdit()
    paste_line_layout.addWidget(paste_line)
    
    #Add OK Cancel buttons layout, buttons and add
    main_ok_button = gui.QPushButton("OK")
    main_cancel_button = gui.QPushButton("Cancel")
    main_ok_button.connect("clicked()", lambda: compareInput(g_ec_window, channels_to_export_widget, unlock_channels_box, uncache_layers_box, unlock_layers_box, export_line, paste_line))
    main_cancel_button.connect("clicked()", g_ec_window.reject)
    uncache_layers_box.connect("clicked()", lambda: uncacheBoxTicked(uncache_layers_box))
    
    very_bottom_layout.addLayout(export_line_layout)
    very_bottom_layout.addLayout(paste_line_layout)
    very_bottom_layout.addWidget(main_ok_button)
    very_bottom_layout.addWidget(main_cancel_button)
    
    #Add browse lines to main layout
    ec_layout.addLayout(very_bottom_layout)
    
    # Display
    g_ec_window.show()

# ------------------------------------------------------------------------------   
def uncacheBoxTicked(uncache_layers_box):
    "Warning message for uncache tick box."
    if uncache_layers_box.isChecked():
        mari.utils.message("Please be aware that uncaching and re-caching the layers could take some time")
        
# ------------------------------------------------------------------------------   
class GeometryToExportList(gui.QListWidget):
    "Stores a list of operations to perform."
    
    def __init__(self, title="For Export"):
        super(GeometryToExportList, self).__init__()
        self._title = title
        self.setSelectionMode(self.ExtendedSelection)
        
    def currentGeometry(self):
        return [self.item(index).data(USER_ROLE_01) for index in range(self.count)]
        
    def addGeometry(self, geometry_list):
        "Adds an operation from the current selections of geometry and directories."
        selected_items = geometry_list.selectedItems()
        if selected_items == []:
            mari.utils.message("Please select at least one object.")
            return
        
        # Add geometry that aren't already added
        current_geometry = set(self.currentGeometry())
        for item in selected_items:
            geometry = item.data(USER_ROLE_01)
            if geometry not in current_geometry:
                current_geometry.add(geometry)
                self.addItem(geometry.name())
                self.item(self.count - 1).setData(USER_ROLE_01, geometry)
        
    def removeGeometry(self):
        "Removes any currently selected operations."
        for item in reversed(self.selectedItems()):     # reverse so indices aren't modified
            index = self.row(item)
            self.takeItem(index)    
    
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
def checkBox(ui, channels_to_export, unlock_channels_box, uncache_layers_box, unlock_layers_box, export_udim_list, paste_udim_list):
    "This is where the check boxes are queried and where lists are generated for functions."
    unlock_channels = unlock_channels_box.isChecked()
    uncache_layers = uncache_layers_box.isChecked()
    unlock_layers = unlock_layers_box.isChecked()
    
    channels_to_export_list = channels_to_export.currentChannels()

    channels_locked = []
    layers_locked = []
    layers_cached = []
    
    if unlock_channels:
        for channel in channels_to_export_list:
            channels_locked.extend(getLockedChannels(channels_to_export_list))
        unlockOrLockList(channels_locked, False)
    
    if uncache_layers:
        for channel in channels_to_export_list:
            layers_cached.extend(getCachedLayers(channel.layerList()))
        uncacheOrCacheList(layers_cached, False)
    
    if (unlock_layers == True) and (uncache_layers == False):
        for channel in channels_to_export_list:
            layers_locked.extend(getLockedLayers(channel.layerList()))
            layers_cached.extend(getCachedLayers(channel.layerList()))
        for layer in layers_locked:
            if layer in layers_cached:
                layers_locked.remove(layer)
        unlockOrLockList(layers_locked, False)
        
    elif unlock_layers:
        for channel in channels_to_export_list:
            layers_locked.extend(getLockedLayers(channel.layerList()))
        unlockOrLockList(layers_locked, False)
        
    export_udim_list = udimToIndex(export_udim_list)
    paste_udim_list = udimToIndex(paste_udim_list)

    whatToCopy(channels_to_export_list, export_udim_list, paste_udim_list, unlock_channels, uncache_layers, unlock_layers)

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
def whatToCopy(channels_to_export_list, export_udim_list, paste_udim_list, unlock_channels, uncache_layers, unlock_layers):
    "Checks channel list against tick boxes and runs export accordingly"
    channels_to_export = channels_to_export_list
    
    if unlock_channels and uncache_layers and unlock_layers:
        for channel in channels_to_export:
            layer_list = getMatchingLayers(channel.layerList(), returnTrue)
            maskToMaskStack(layer_list)
            layer_list = getMatchingLayers(channel.layerList(), returnTrue)
            layer_list = getPaintableLayers(layer_list)
            exportUdimToUdim(export_udim_list, paste_udim_list, layer_list)
            
    if unlock_channels and uncache_layers or not uncache_layers and unlock_layers or not unlock_layers:
        for channel in channels_to_export:
            layer_list = getMatchingLayers(channel.layerList(), returnTrue)
            layer_list = getModifiableLayers(layer_list)
            layer_list = maskToMaskStack(layer_list)
            layer_list = getPaintableLayers(layer_list)
            exportUdimToUdim(export_udim_list, paste_udim_list, layer_list)
            
    if not unlock_channels and uncache_layers or not uncache_layers and unlock_layers or not unlock_layers:
        channels_locked = getLockedChannels(channels_to_export)
        for channel in channels_to_export:
            if channel in channels_locked:
                channels_to_export.remove(channel)
        for channel in channels_to_export:
            layer_list = getMatchingLayers(channel.layerList(), returnTrue)
            layer_list = getModifiableLayers(layer_list)
            layer_list = maskToMaskStack(layer_list)
            layer_list = getPaintableLayers(layer_list)
            exportUdimToUdim(export_udim_list, paste_udim_list, layer_list)
            
# ------------------------------------------------------------------------------  
def exportUdimRange(layer_list, export_udim_list, paste_udim_list):
            "Pass each udim and layer list to the exportUdimToUdim function"
            for index in range(len(export_udim_list)):
                exportUdimToUdim(export_udim_list[index], paste_udim_list[index], layer_list)
       
# ------------------------------------------------------------------------------  
def compareInput(g_ec_window, channels_to_export, unlock_channels_box, uncache_layers_box, unlock_layers_box, export_line, paste_line):
    "Check export and paste input from the dialog are udim numbers i.e. 1001 - 9999, and not alphabetical, they can contain multiple ranges and individual udims i.e. 1001-1005,1006,1009,1021-1030"

    export_line = export_line.text
    paste_line = paste_line.text
    export_list = export_line.split(',')
    paste_list = paste_line.split(',')           
    export_udim_check = []
    paste_udim_check = []
    export_udim_list = []
    paste_udim_list = []
    check_list = []
    check = False
    
    for item in export_list:
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
            export_udim_check.append(len(range_list))
            export_udim_list.extend(range_list)
        elif item.isdigit() and len(item) == 4 and int(item) >= 1001:
            export_udim_check.append(1)
            export_udim_list.append(int(item))
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

    if len(export_udim_check) == len(paste_udim_check):
        for i in range(len(export_udim_check)):
            if export_udim_check[i] == paste_udim_check[i]:
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
        mari.utils.message("Please enter matching UDIM ranges for exporting, i.e. Copy UDIM: 1001-1005,1009 Paste UDIM: 1016-1020,1032")
    else:
        checkBox(g_ec_window, channels_to_export, unlock_channels_box, unlock_layers_box, uncache_layers_box, export_udim_list, paste_udim_list)
        
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
            mari.utils.message("Currently in development this is just a place holder.")
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
        
        mari.utils.message("Currently in development this is just a place holder.")
        return False
    
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False

# ------------------------------------------------------------------------------   
def exportUdimToUdim(export_index, paste_index, layer_list):
    "Copies udim to udim."
    # un-select patches
    patches = mari.geo.current().selectedPatches()
    if patches == None:
        pass
    else:
        for patch in patches:
            patch.setSelected(False)
   
    export = mari.actions.get('/Mari/Project/Project Explorer/Quick Copy')
    paste = mari.actions.get('/Mari/Project/Project Explorer/Quick Paste')
    
    for i in range(len(export_index)):
        for layer in layer_list:
            # un-select layers
            layer.makeCurrent()
            layer.setSelected(False)
            
            layer.makeCurrent()
            mari.geo.current().patch(export_index[i]).setSelected(True)
            export.trigger()
            mari.geo.current().patch(export_index[i]).setSelected(False)
            mari.geo.current().patch(paste_index[i]).setSelected(True)
            paste.trigger()
            mari.geo.current().patch(paste_index[i]).setSelected(False)
            layer.setSelected(False)