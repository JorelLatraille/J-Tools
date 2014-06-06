# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Export selected channels from one or more objects
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

import mari, os, hashlib
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

version = "0.05"

USER_ROLE = 34          # PySide.Qt.UserRole

# ------------------------------------------------------------------------------
class ExportSelectedChannelsUI(QtGui.QDialog):
    """Export channels from one or more objects."""
    def __init__(self, bool_, parent=None):
        super(ExportSelectedChannelsUI, self).__init__(parent)

        #Set window title and create a main layout
        self.bool_ = bool_
        self.setWindowTitle("Export Selected Channels")
        main_layout = QtGui.QVBoxLayout()
        top_group = QtGui.QGroupBox()
        middle_group = QtGui.QGroupBox()
        bottom_group = QtGui.QGroupBox()
        
        #Create layout for middle section
        top_layout = QtGui.QHBoxLayout()
        
        #Create channel layout, label, and widget. Finally populate.
        channel_layout = QtGui.QVBoxLayout()
        channel_header_layout = QtGui.QHBoxLayout()
        self.channel_label = QtGui.QLabel("<strong>Channels</strong>")
        self.channel_list = QtGui.QListWidget()
        self.channel_list.setSelectionMode(self.channel_list.ExtendedSelection)
        
        #Create filter box for channel list
        self.channel_filter_box = QtGui.QLineEdit()
        mari.utils.connect(self.channel_filter_box.textEdited, lambda: _updateChannelFilter(self.channel_filter_box, self.channel_list))
        
        #Create layout and icon/label for channel filter
        channel_header_layout.addWidget(self.channel_label)
        channel_header_layout.addStretch()
        self.channel_search_icon = QtGui.QLabel()
        search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
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
                self.channel_list.item(self.channel_list.count() - 1).setData(USER_ROLE, channel)
        
        #Add filter layout and channel list to channel layout
        channel_layout.addLayout(channel_header_layout)
        channel_layout.addWidget(self.channel_list)
        
        #Create middle button section
        middle_button_layout = QtGui.QVBoxLayout()
        self.add_button = QtGui.QPushButton("+")
        self.remove_button = QtGui.QPushButton("-")
        middle_button_layout.addStretch()
        middle_button_layout.addWidget(self.add_button)
        middle_button_layout.addWidget(self.remove_button)
        middle_button_layout.addStretch()
        
        #Add wrapped QtGui.QListWidget with custom functions
        export_layout = QtGui.QVBoxLayout()
        export_header_layout = QtGui.QHBoxLayout()
        self.export_label = QtGui.QLabel("<strong>Channels To Export</strong>")
        self.export_list = ChannelsToExportList()
        self.export_list.setSelectionMode(self.export_list.ExtendedSelection)
        
        #Create filter box for export list
        self.export_filter_box = QtGui.QLineEdit()
        mari.utils.connect(self.export_filter_box.textEdited, lambda: _updateExportFilter(self.export_filter_box, self.export_list))
        
        #Create layout and icon/label for export filter
        export_header_layout.addWidget(self.export_label)
        export_header_layout.addStretch()
        self.export_search_icon = QtGui.QLabel()
        self.export_search_icon.setPixmap(search_pixmap)
        export_header_layout.addWidget(self.export_search_icon)
        export_header_layout.addWidget(self.export_filter_box)
        
        #Add filter layout and export list to export layout
        export_layout.addLayout(export_header_layout)
        export_layout.addWidget(self.export_list)
        
        #Hook up add/remove buttons
        self.remove_button.clicked.connect(self.export_list._removeChannels)
        self.add_button.clicked.connect(lambda: self.export_list._addChannels(self.channel_list))

        #Add widgets to top layout
        top_layout.addLayout(channel_layout)
        top_layout.addLayout(middle_button_layout)
        top_layout.addLayout(export_layout)
    
# -----------------------------------------------------------------------------------------------------    
    
        #Add path layout.
        path_layout = QtGui.QHBoxLayout()

        #Get mari default path and template
        path = os.path.abspath(mari.resources.path(mari.resources.DEFAULT_EXPORT))
        template = mari.resources.sequenceTemplate()
        export_path_template = os.path.join(path, template)

        #Add path line input and button, also set text to Mari default path and template
        path_label = QtGui.QLabel('Path:')
        self.path_line_edit = QtGui.QLineEdit()
        path_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QtGui.QIcon(path_pixmap)
        path_button = QtGui.QPushButton(icon, "")
        path_button.clicked.connect(self._getPath)
        self.path_line_edit.setText(export_path_template)
            
        #Add path line input and button to middle layout    
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_line_edit)
        path_layout.addWidget(path_button)

        #Add to top group
        top_group_layout = QtGui.QVBoxLayout()

        #Add export everything check box
        self.export_everything_box = QtGui.QCheckBox('Export Everything')
        self.export_everything_box.clicked.connect(self._exportEverything)

        top_group_layout.addLayout(top_layout)
        top_group_layout.addLayout(path_layout)
        top_group_layout.addWidget(self.export_everything_box)
        top_group.setLayout(top_group_layout)
    
        #Add middle group layout and check boxes
        middle_group_layout = QtGui.QHBoxLayout()
        self.export_only_modified_textures_box = QtGui.QCheckBox('Only Modified Textures')
        self.export_only_modified_textures_box.setChecked(True)
        middle_group_layout.addWidget(self.export_only_modified_textures_box)
        middle_group.setLayout(middle_group_layout)

        #Add check box layout.
        check_box_layout = QtGui.QGridLayout()
        
        #Add export option check boxes
        self.export_flattened_box = QtGui.QCheckBox('Export Flattened')
        self.export_full_patch_bleed_box = QtGui.QCheckBox('Full Patch Bleed')
        self.export_small_textures_box = QtGui.QCheckBox('Disable Small Textures')
        if self.bool_:
            self.export_remove_alpha_box = QtGui.QCheckBox('Remove Alpha')
    
        #Add tick boxes and buttons to bottom layout
        check_box_layout.addWidget(self.export_flattened_box, 0, 0)
        check_box_layout.addWidget(self.export_full_patch_bleed_box, 1, 0)
        check_box_layout.addWidget(self.export_small_textures_box, 1, 1)
        if self.bool_:
            check_box_layout.addWidget(self.export_remove_alpha_box, 1, 2)

        bottom_group.setLayout(check_box_layout)

        #Add widget groups to main layout
        main_layout.addWidget(top_group)
        main_layout.addWidget(middle_group)
        main_layout.addWidget(bottom_group)

        # Add OK Cancel buttons
        self.button_box = QtGui.QDialogButtonBox()
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.button_box.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self._checkInput)
        self.button_box.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.reject)

        #Add bottom layout to main layout and set main layout to dialog's layout
        main_layout.addWidget(self.button_box)
        self.setLayout(main_layout)

    #Hide parts of interface if export everything is ticked
    def _exportEverything(self):
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
    def _getPath(self):
        path = mari.utils.misc.getSaveFileName(parent=None, caption='Export Path', dir='', filter='', selected_filter=None, options=0, save_filename='')
        if path == "":
            return
        else:
            self._setPath(os.path.abspath(path))

    #Set the path line edit box text to be the path provided
    def _setPath(self, path):
        self.path_line_edit.setText(path)

    #Check path and template will work, check if export everything box is ticked if not make sure there are some channels to export
    def _checkInput(self):
        file_types = ['.' + format for format in mari.images.supportedWriteFormats()]
        path_template = self.path_line_edit.text()
        if not os.path.exists(os.path.split(path_template)[0]):
            title = 'Create Directories'
            text = 'Path does not exist "%s".' %os.path.split(path_template)[0]
            info = 'Create the path?'
            dialog = InfoUI(title, text, info)
            if not dialog.exec_():
                return
            os.makedirs(os.path.split(path_template)[0])
        if not path_template.endswith(tuple(file_types)):
            mari.utils.message("File type is not supported: '%s'" %(os.path.split(path_template)[1]))
            return
        if self.export_everything_box.isChecked():
            pass
        elif len(self.export_list._currentChannels()) == 0:
            mari.utils.message("Please add a channel to export.")
            return
        self.accept()

    #Get list of channels to export from the export list
    def _getChannelsToExport(self):
        return self.export_list._currentChannels()

    #Get export path and template
    def _getExportPathTemplate(self):
        return self.path_line_edit.text()

    #Get export everything box is ticked (bool)
    def _getExportEverything(self):
        return self.export_everything_box.isChecked()

    #Get export only modified textures box is ticked (bool)
    def _getExportOnlyModifiedTextures(self):
        return self.export_only_modified_textures_box.isChecked()

    #Get export flattened box is ticked (bool)
    def _getExportFlattened(self):
        return self.export_flattened_box.isChecked()

    #Get export small textures box is ticked (bool)
    def _getExportFullPatchBleed(self):
        return self.export_full_patch_bleed_box.isChecked()

    #Get export small textures box is ticked (bool)
    def _getExportSmallTextures(self):
        return self.export_small_textures_box.isChecked()

    #Get export remove alpha box is ticked (bool)
    def _getExportRemoveAlpha(self):
        if self.bool_:
            return self.export_remove_alpha_box.isChecked()
        else:
            return False

# ------------------------------------------------------------------------------   
class ChannelsToExportList(QtGui.QListWidget):
    """Stores a list of operations to perform."""
    
    def __init__(self, title="For Export"):
        super(ChannelsToExportList, self).__init__()
        self._title = title
        self.setSelectionMode(self.ExtendedSelection)
        
    def _currentChannels(self):
        return [self.item(index).data(USER_ROLE) for index in range(self.count())]
        
    def _addChannels(self, channel_list):
        "Adds an operation from the current selections of channels and directories."
        selected_items = channel_list.selectedItems()
        if selected_items == []:
            mari.utils.message("Please select at least one channel.")
            return
        
        # Add channels that aren't already added
        current_channels = set(self._currentChannels())
        for item in selected_items:
            channel = item.data(USER_ROLE)
            if channel not in current_channels:
                current_channels.add(channel)
                self.addItem(item.text())
                self.item(self.count() - 1).setData(USER_ROLE, channel)
        
    def _removeChannels(self):
        "Removes any currently selected operations."
        for item in reversed(self.selectedItems()):     # reverse so indices aren't modified
            index = self.row(item)
            self.takeItem(index)    

# ------------------------------------------------------------------------------
def _updateChannelFilter(channel_filter_box, channel_list):
    """For each item in the channel list display, set it to hidden if it doesn't match the filter text."""
    match_words = channel_filter_box.text().lower().split()
    for item_index in range(channel_list.count()):
        item = channel_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)
        
# ------------------------------------------------------------------------------
def _updateExportFilter(export_filter_box, export_list):
    """For each item in the export list display, set it to hidden if it doesn't match the filter text."""
    match_words = export_filter_box.text().lower().split()
    for item_index in range(export_list.count()):
        item = export_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)

# ------------------------------------------------------------------------------
class InfoUI(QtGui.QMessageBox):
    """Show the user information for them to make a decision on whether to procede."""
    def __init__(self, title, text, info=None, details=None, bool_=False, parent=None):
        super(InfoUI, self).__init__(parent)

        # Create info gui
        self.setIcon(4)
        self.setWindowTitle(title)
        self.setText(text)
        if not info == None:
            self.setInformativeText(info)
        if not details == None:
            self.setDetailedText(details)
        if not bool_:
            self.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            self.setDefaultButton(QtGui.QMessageBox.Ok)

# ------------------------------------------------------------------------------ 
def _exportChannels(args_dict):
    save_options = 0
    if args_dict['full_patch_bleed']:
        save_options = save_options|2
    elif args_dict['small_textures']:
        save_options = save_options|1
    elif args_dict['remove_alpha']:
        save_options = save_options|4
    #Check if export flattened is ticked, if not export unflattened
    path = args_dict['path']
    if args_dict['flattened']:
        for channel in args_dict['channels']:
            uv_index_list = []
            metadata = []
            if args_dict['only_modified_textures']:
                uv_index_list, metadata = _onlyModifiedTextures(channel)
                if len(uv_index_list) == 0:
                    continue
            try:
                channel.exportImagesFlattened(path, save_options, uv_index_list)
            except Exception, e:
                mari.utils.message('Failed to export "%s"' %e)
                return
            for data in metadata:            
                channel.setMetadata(*data)
                channel.setMetadataEnabled(data[0], False)
            channel.setMetadata('jtoolsOnlyModifiedTextures', True)
            channel.setMetadataEnabled('jtoolsOnlyModifiedTextures', False)  
    else:
        for channel in args_dict['channels']:
            uv_index_list = []
            metadata = []
            if args_dict['only_modified_textures']:
                uv_index_list, metadata = _onlyModifiedTextures(channel)
                if len(uv_index_list) == 0:
                    continue
            try:
                channel.exportImages(path, save_options, uv_index_list)
            except Exception, e:
                mari.utils.message('Failed to export "%s"' %e)
                return
            for data in metadata:            
                channel.setMetadata(*data)
                channel.setMetadataEnabled(data[0], False)
            channel.setMetadata('jtoolsOnlyModifiedTextures', True)
            channel.setMetadataEnabled('jtoolsOnlyModifiedTextures', False)        
    #If successful let the user know
    mari.utils.message("Export Successful")
    
# ------------------------------------------------------------------------------ 
def _exportEverything(args_dict):
    """Export everything, all geo and all channels"""
    geo_list = mari.geo.list()
    channels = []
    for geo in geo_list:
        channels.extend(geo.channelList())
    save_options = 0
    if args_dict['full_patch_bleed']:
        save_options = save_options|2
    elif args_dict['small_textures']:
        save_options = save_options|1
    elif args_dict['remove_alpha']:
        save_options = save_options|4
    #Check if export flattened is ticked, if not export unflattened
    path = args_dict['path']
    if args_dict['flattened']:
        for channel in channels:
            uv_index_list = []
            metadata = []
            if args_dict['only_modified_textures']:
                uv_index_list, metadata = _onlyModifiedTextures(channel)
                if len(uv_index_list) == 0:
                    continue
            try:
                channel.exportImagesFlattened(path, save_options, uv_index_list)
            except Exception, e:
                mari.utils.message('Failed to export "%s"' %e)
                return
            for data in metadata:            
                channel.setMetadata(*data)
                channel.setMetadataEnabled(data[0], False)
            channel.setMetadata('jtoolsOnlyModifiedTextures', True)
            channel.setMetadataEnabled('jtoolsOnlyModifiedTextures', False)
    else:
        for channel in channels:
            uv_index_list = []
            metadata = []
            if agrs_dict['only_modified_textures']:
                uv_index_list, metadata = _onlyModifiedTextures(channel)
                if len(uv_index_list) == 0:
                    continue
            try:
                channel.exportImages(path, save_options, uv_index_list)
            except Exception, e:
                mari.utils.message('Failed to export "%s"' %e)
                return
            for data in metadata:            
                channel.setMetadata(*data)
                channel.setMetadataEnabled(data[0], False)
            channel.setMetadata('jtoolsOnlyModifiedTextures', True)
            channel.setMetadataEnabled('jtoolsOnlyModifiedTextures', False)
    #If successful let the user know
    mari.utils.message("Export Successful")

# ------------------------------------------------------------------------------
def exportSelectedChannels():
    """Export selected channels."""
    suitable = _isProjectSuitable()
    if not suitable[0]:
        return
    
    #Create dialog and execute accordingly
    dialog = ExportSelectedChannelsUI(suitable[1])
    if dialog.exec_():
        args_dict = {
        'channels' : dialog._getChannelsToExport(),
        'path' : dialog._getExportPathTemplate(),
        'flattened' : dialog._getExportFlattened(),
        'full_patch_bleed' : dialog._getExportFullPatchBleed(),
        'small_textures' : dialog._getExportSmallTextures(),
        'remove_alpha' : dialog._getExportRemoveAlpha(),
        'only_modified_textures' : dialog._getExportOnlyModifiedTextures()
        }
        if dialog._getExportEverything():
            _exportEverything(args_dict)
        else:
            _exportChannels(args_dict)

# ------------------------------------------------------------------------------
def _onlyModifiedTextures(channel):
    """Manage channels so only modified patch images get exported"""
    if channel.hasMetadata('jtoolsOnlyModifiedTextures'):
        uv_index_list, metadata = _getChangedUvIndexes(channel)   
    else:
        uv_index_list, metadata = _setChannelUvIndexes(channel)
    return uv_index_list, metadata

# ------------------------------------------------------------------------------
def _getChangedUvIndexes(channel):
    """Get uv indexes with new hashes"""
    geo = channel.geoEntity()
    all_layers = _getAllLayers(channel.layerList())
    patch_list = geo.patchList()
    uv_index_list = []
    metadata = []
    for patch in patch_list:
        hash_ = _createHash(patch, all_layers)
        if not hash_ == channel.metadata(str(patch.uvIndex())):
            uv_index_list.append(patch.uvIndex())
            metadata.append((str(patch.uvIndex()), hash_))
    return uv_index_list, metadata

# ------------------------------------------------------------------------------
def _setChannelUvIndexes(channel):
    """Set the channel metadata uv index hash"""
    geo = channel.geoEntity()
    all_layers = _getAllLayers(channel.layerList())
    patch_list = geo.patchList()
    uv_index_list = []
    metadata = []
    for patch in patch_list:
        hash_ = _createHash(patch, all_layers)
        uv_index_list.append(patch.uvIndex())
        metadata.append((str(patch.uvIndex()), hash_))
    return uv_index_list, metadata

# ------------------------------------------------------------------------------
def _createHash(patch, all_layers):
    """Create hashes on channel for all layers"""
    hash_ = ''
    index = patch.uvIndex()

    for layer in all_layers:
        hash_ += _basicLayerData(layer)

        if layer.isAdjustmentLayer():
            for adjustmentParameter in layer.primaryAdjustmentParameters():
                hash_ += str(layer.getPrimaryAdjustmentParameter(adjustmentParameter))
            # If this layer has a secondary adjustment then capture that data as well.
            if layer.hasSecondaryAdjustment():
                for adjustmentParameter in layer.secondaryAdjustmentParameters():
                    hash_ += str(layer.getPrimaryAdjustmentParameter(adjustmentParameter))

        elif layer.isProceduralLayer():
                for proceduralParameter in layer.proceduralParameters():
                    if 'Cache' in proceduralParameter:
                        continue
                    parameterValue = layer.getProceduralParameter(proceduralParameter)
                    if isinstance(parameterValue, mari.Color):
                        hash_ += str(parameterValue.rgba())
                    elif isinstance(parameterValue, mari.LookUpTable):
                        hash_ += parameterValue.controlPointsAsString()
                    else:
                        hash_ += str(parameterValue)

        elif layer.isPaintableLayer():
            hash_ += layer.imageSet().image(index).hash()
            
        elif layer.hasMask():
            hash_ += layer.maskImageSet().image(index).hash()

    return _sha256(hash_)

# ------------------------------------------------------------------------------
def _getAllLayers(layer_list):
    """Returns a list of all of the layers in the layer stack, including substacks."""
    return _getMatchingLayers(layer_list, _returnTrue)

# ------------------------------------------------------------------------------
def _returnTrue(*object):
    """Return True for anything passed to this function."""
    return True

# ------------------------------------------------------------------------------
def _getMatchingLayers(layer_list, criterionFn):
    """Returns a list of all of the layers in the stack that match the given criterion function, including substacks."""
    matching = []
    for layer in layer_list:
        if criterionFn(layer):
            matching.append(layer)
        if hasattr(layer, 'layerStack'):
            matching.extend(_getMatchingLayers(layer.layerStack().layerList(), criterionFn))
        if layer.hasMaskStack():
            matching.extend(_getMatchingLayers(layer.maskStack().layerList(), criterionFn))
        if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
            matching.extend(_getMatchingLayers(layer.adjustmentStack().layerList(), criterionFn))
        
    return matching

# ------------------------------------------------------------------------------
def _basicLayerData(layer):
    """Collect basic layer data common to all types of layers."""
    return str(layer.blendAmount()) + \
    str(layer.blendMode()) + \
    str(layer.blendModeStr()) + \
    str(layer.isVisible())

# ------------------------------------------------------------------------------
def _sha256(string):
    """Returns a hash for the given string."""
    sha256 = hashlib.sha256()
    sha256.update(string)
    return sha256.hexdigest()

# ------------------------------------------------------------------------------
def _isProjectSuitable():
    """Checks project state."""
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
    
        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False, False

        if mari.app.version().number() >= 20502300:
            return True, True

        return True, False
    
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False, False
    
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    exportSelectedChannels()

# ------------------------------------------------------------------------------
# Add action to Mari menu.
action = mari.actions.create(
    "Export Selected Channels", "mari.jtools.exportSelectedChannels()"
    )
mari.menus.addAction(action, "MainWindow/&Channels", "Export")
icon_filename = "ExportImages.png"
icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
action.setIconPath(icon_path)