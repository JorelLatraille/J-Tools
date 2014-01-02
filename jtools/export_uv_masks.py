# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Export UV Masks for selected geo
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
import PythonQt.QtGui as QtGui

version = "0.03"

USER_ROLE = 32          # PythonQt.Qt.UserRole

g_eum_window = None
g_eum_cancelled = False
directory = ''
g_file_types = ['.' + format for format in mari.images.supportedWriteFormats()]
list.sort(g_file_types)

# ------------------------------------------------------------------------------
def exportUVMasks():
    "Export UV masks initialise"
    global directory
    
    #Check project is suitable
    if not isProjectSuitable():
        return False        
        
    #Get directory to export to
    directory = mari.utils.misc.getExistingDirectory(parent=None, caption='Export UV Masks', dir='')
    if directory == "":
        return False
        
    showUI()    

# ------------------------------------------------------------------------------    
def exportMasks(g_eum_window, q_geo_list, file_type_combo):
    "Export the masks"
    geo_list = q_geo_list.currentGeometry()
    file_type = file_type_combo.currentText

    if len(geo_list) == 0:
        return False
        
    g_eum_window.reject()
     
    #Export selected geo UV masks 
    for geo in geo_list:
        mari.geo.setCurrent(geo)
        geo_name = geo.name()
        patch_list = geo.patchList()
        patch_udims = []
        for patch in patch_list:
            patch_udims.append(int(patch.name()))
            patch.setSelected(False)
        for patch in patch_udims:
            uv_mask = mari.actions.get('/Mari/Geometry/Patches/UV Mask to Image Manager')
            index = patch - 1001
            geo.patch(index).setSelected(True)
            uv_mask.trigger()
            geo.patch(index).setSelected(False)        
            image_list = mari.images.list()
            mari.images.saveImages(image_list[-1:], os.path.join(directory, "%s.mask.%d.%s" %(geo_name, patch, file_type)))
            index = len(image_list) - 1
            image_list[index].close()
    mari.utils.message("Export UV Masks Complete.")

# ------------------------------------------------------------------------------
def showUI():
    "Copy paint from one or more patches to other patches, for all layers and geometry."
    #Create UI
    
    #Check project state
    if not isProjectSuitable():
        return False
    
    #Create main dialog, add main layout and set title
    global g_eum_window
    g_eum_window = QtGui.QDialog()
    eum_layout = QtGui.QVBoxLayout()
    g_eum_window.setLayout(eum_layout)
    g_eum_window.setWindowTitle("Export UV Masks")
    
    #Create layout for middle section
    centre_layout = QtGui.QHBoxLayout()
    
    #Create geometry layout, label, and widget. Finally populate.
    geo_layout = QtGui.QVBoxLayout()
    geo_header_layout = QtGui.QHBoxLayout()
    geo_label = QtGui.QLabel("Geometry")
    setBold(geo_label)
    geo_list = QtGui.QListWidget()
    geo_list.setSelectionMode(geo_list.ExtendedSelection)
    
    filter_box = QtGui.QLineEdit()
    mari.utils.connect(filter_box.textEdited, lambda: updateFilter(filter_box, geo_list))
    
    geo_header_layout.addWidget(geo_label)
    geo_header_layout.addStretch()
    geo_search_icon = QtGui.QLabel()
    search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
    geo_search_icon.setPixmap(search_pixmap)
    geo_header_layout.addWidget(geo_search_icon)
    geo_header_layout.addWidget(filter_box)
    
    geo = mari.geo.current()
    for geo in mari.geo.list():
        geo_list.addItem(geo.name())
        geo_list.item(geo_list.count - 1).setData(USER_ROLE, geo)
    
    geo_layout.addLayout(geo_header_layout)
    geo_layout.addWidget(geo_list)
    
    #Create middle button section
    middle_button_layout = QtGui.QVBoxLayout()
    add_button = QtGui.QPushButton("+")
    remove_button = QtGui.QPushButton("-")
    middle_button_layout.addStretch()
    middle_button_layout.addWidget(add_button)
    middle_button_layout.addWidget(remove_button)
    middle_button_layout.addStretch()
    
    #Add wrapped QtGui.QListWidget with custom functions
    geometry_to_copy_layout = QtGui.QVBoxLayout()
    geometry_to_copy_label = QtGui.QLabel("Geometry to export UV masks from.")
    setBold(geometry_to_copy_label)
    geometry_to_copy_widget = GeoToExportList()
    geometry_to_copy_layout.addWidget(geometry_to_copy_label)
    geometry_to_copy_layout.addWidget(geometry_to_copy_widget)
    
    #Hook up add/remove buttons
    remove_button.connect("clicked()", geometry_to_copy_widget.removeGeometry)
    add_button.connect("clicked()", lambda: geometry_to_copy_widget.addGeometry(geo_list))

    #Add widgets to centre layout
    centre_layout.addLayout(geo_layout)
    centre_layout.addLayout(middle_button_layout)
    centre_layout.addLayout(geometry_to_copy_layout)

    #Add centre layout to main layout
    eum_layout.addLayout(centre_layout)

    #Add bottom layout.
    bottom_layout = QtGui.QHBoxLayout()
    
    #Add file type options
    file_type_combo_text = QtGui.QLabel('File Types:')
    file_type_combo = QtGui.QComboBox()
    for file_type in g_file_types:
        file_type_combo.addItem(file_type)
    file_type_combo.setCurrentIndex(file_type_combo.findText('tif'))
    
    bottom_layout.addWidget(file_type_combo_text)
    bottom_layout.addWidget(file_type_combo)
    bottom_layout.addStretch()
    
    #Add OK Cancel buttons layout, buttons and add
    main_ok_button = QtGui.QPushButton("OK")
    main_cancel_button = QtGui.QPushButton("Cancel")
    main_ok_button.connect("clicked()", lambda: exportMasks(g_eum_window, geometry_to_copy_widget, file_type_combo))
    main_cancel_button.connect("clicked()", g_eum_window.reject)
    
    bottom_layout.addWidget(main_ok_button)
    bottom_layout.addWidget(main_cancel_button)
    
    #Add browse lines to main layout
    eum_layout.addLayout(bottom_layout)
    
    # Display
    g_eum_window.show()
    
# ------------------------------------------------------------------------------   
class GeoToExportList(QtGui.QListWidget):
    "Stores a list of operations to perform."
    
    def __init__(self, title="For Export"):
        super(GeoToExportList, self).__init__()
        self._title = title
        self.setSelectionMode(self.ExtendedSelection)
        
    def currentGeometry(self):
        return [self.item(index).data(USER_ROLE) for index in range(self.count)]
        
    def addGeometry(self, geo_list):
        "Adds an operation from the current selections of geometry and directories."
        selected_items = geo_list.selectedItems()
        if selected_items == []:
            mari.utils.message("Please select at least one object.")
            return
        
        # Add geometry that aren't already added
        current_geometry = set(self.currentGeometry())
        for item in selected_items:
            geo = item.data(USER_ROLE)
            if geo not in current_geometry:
                current_geometry.add(geo)
                self.addItem(geo.name())
                self.item(self.count - 1).setData(USER_ROLE, geo)
        
    def removeGeometry(self):
        "Removes any currently selected operations."
        for item in reversed(self.selectedItems()):     # reverse so indices aren't modified
            index = self.row(item)
            self.takeItem(index)
            
# ------------------------------------------------------------------------------
def updateFilter(filter_box, geo_list):
    "For each item in the geo list display, set it to hidden if it doesn't match the filter text."
    match_words = filter_box.text.lower().split()
    for item_index in range(geo_list.count):
        item = geo_list.item(item_index)
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
    "Checks project state and Mari version."
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
    exportUVMasks()