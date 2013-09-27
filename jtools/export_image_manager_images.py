# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Export selected Image Manager images in your specified file type
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

version = "0.01"

USER_ROLE = 34
image_file_types = ['.bmp', '.jpg', '.jpeg', '.png', '.ppm', '.psd', '.tga', '.tif', '.tiff', '.xbm', '.xpm']
list.sort(image_file_types)

# ------------------------------------------------------------------------------
def exportImageManagerImages():
    "Export images from the image manager with either original extension or chosen extension to the path provided"
    if not isProjectSuitable():
        return

    dialog = exportImageManagerImagesGUI()
    if dialog.exec_():
        export_path = dialog.getExportPath()
        image_list = dialog.getImagesToExport()
        combo_text = dialog.getComboText()
        mari.app.startProcessing('Exporting images...', len(image_list), can_cancel=False)
        for image in image_list:
            mari.app.stepProgress()
            image_object = image.data(USER_ROLE)
            for type in image_file_types:
                if image.text().endswith(type):
                    image_name = image.text().split(type)
                    image_name = "".join(image_name)
                    break
            image_object.saveAs(os.path.join(export_path, image_name + combo_text), None, 0)
        mari.app.stopProcessing()
        mari.utils.message("Export Complete.")        
        
# ------------------------------------------------------------------------------
class exportImageManagerImagesGUI(QDialog):
    #Create UI
    def __init__(self, parent=None):
        super(exportImageManagerImagesGUI, self).__init__(parent)

        eimi_layout = QVBoxLayout()
        self.setLayout(eimi_layout)
        self.setWindowTitle("Export Image Manager Images")
        
        #Create layout for middle section
        centre_layout = QHBoxLayout()
        
        #Create images layout, label, and widget. Finally populate.
        images_layout = QVBoxLayout()
        images_header_layout = QHBoxLayout()
        images_label = QLabel("Images")
        setBold(images_label)
        images_list = QListWidget()
        images_list.setSelectionMode(images_list.ExtendedSelection)
        
        filter_box = QLineEdit()
        mari.utils.connect(filter_box.textEdited, lambda: updateFilter(filter_box, images_list))
        
        images_header_layout.addWidget(images_label)
        images_header_layout.addStretch()
        images_search_icon = QLabel()
        search_pixmap = QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
        images_search_icon.setPixmap(search_pixmap)
        images_header_layout.addWidget(images_search_icon)
        images_header_layout.addWidget(filter_box)
        
        image_list = []
        for image in mari.images.list():
            split_image_path = os.path.abspath(image.filePath()).split('\\')
            image_list.extend(split_image_path[-1:])    
        
        for image in mari.images.list():
            images_list.addItem("".join(os.path.abspath(image.filePath()).split('\\')[-1:]))
            images_list.item(images_list.count - 1).setData(USER_ROLE, image)
        
        images_layout.addLayout(images_header_layout)
        images_layout.addWidget(images_list)
        
        #Create middle button section
        middle_button_layout = QVBoxLayout()
        add_button = QPushButton("+")
        remove_button = QPushButton("-")
        middle_button_layout.addStretch()
        middle_button_layout.addWidget(add_button)
        middle_button_layout.addWidget(remove_button)
        middle_button_layout.addStretch()
        
        #Add wrapped QListWidget with custom functions
        images_to_export_layout = QVBoxLayout()
        images_to_export_label = QLabel("Images to export")
        setBold(images_to_export_label)
        self.images_to_export = ImagesToExportList()
        images_to_export_layout.addWidget(images_to_export_label)
        images_to_export_layout.addWidget(self.images_to_export)
        
        #Hook up add/remove buttons
        remove_button.connect("clicked()", self.images_to_export.removeImages)
        add_button.connect("clicked()", lambda: self.images_to_export.addImages(images_list))

        #Add widgets to centre layout
        centre_layout.addLayout(images_layout)
        centre_layout.addLayout(middle_button_layout)
        centre_layout.addLayout(images_to_export_layout)

        #Add centre layout to main layout
        eimi_layout.addLayout(centre_layout)

        #Add bottom layout.
        bottom_layout = QHBoxLayout()
        
        #Add file type options
        file_type_combo_text = QLabel('File Types:')
        self.file_type_combo = QComboBox()
        for file_type in image_file_types:
            self.file_type_combo.addItem(file_type)
        self.file_type_combo.setCurrentIndex(self.file_type_combo.findText('.tif'))
        
        #Add path line input and button
        path_label = QLabel('Path:')
        self.path = QLineEdit()
        path_pixmap = QPixmap(mari.resources.path(mari.resources.ICONS) + '/ExportImages.png')
        icon = QIcon(path_pixmap)
        path_button = QPushButton(icon, "")
        path_button.connect("clicked()", self.getPath)
        
        bottom_layout.addWidget(path_label)
        bottom_layout.addWidget(self.path)
        bottom_layout.addWidget(path_button)
        bottom_layout.addWidget(file_type_combo_text)
        bottom_layout.addWidget(self.file_type_combo)
        
        #Add OK Cancel buttons layout, buttons and add
        main_apply_button = QPushButton("Apply")
        main_cancel_button = QPushButton("Cancel")
        main_apply_button.connect("clicked()", self.accepted)
        main_cancel_button.connect("clicked()", self.reject)
        
        bottom_layout.addWidget(main_apply_button)
        bottom_layout.addWidget(main_cancel_button)
        
        #Add browse lines to main layout
        eimi_layout.addLayout(bottom_layout)

    def getPath(self):
        "Get export path and set the text in path LineEdit widget"
        file_path = mari.utils.misc.getExistingDirectory(parent=self, caption='Export Path', dir='')
        if file_path == "":
            return
        else:
            self.path.setText(file_path)
    
    def accepted(self):
        if len(self.images_to_export.currentImageNames()) == 0:
            mari.utils.message('Please add some images to export.')
            return
        if self.path.text == "":
            mari.utils.message('Please provide a path to export to.')
            return
        if not os.path.exists(os.path.abspath(self.path.text)):
            mari.utils.message('The path "%s" does not exist.' %(os.path.abspath(self.path.text)))
            return
        self.accept()
        
    def getExportPath(self):
        return os.path.abspath(r'%s' %self.path.text)
        
    def getImagesToExport(self):
        return self.images_to_export.currentImageNames()
        
    def getComboText(self):
        return self.file_type_combo.currentText
    
# ------------------------------------------------------------------------------   
class ImagesToExportList(QListWidget):
    "Stores a list of operations to perform."
    
    def __init__(self, title="For Export"):
        super(ImagesToExportList, self).__init__()
        self._title = title
        self.setSelectionMode(self.ExtendedSelection)
        
    def currentImages(self):
        return [self.item(index).data(USER_ROLE) for index in range(self.count)]
        
    def currentImageNames(self):
        return [self.item(index) for index in range(self.count)]
        
    def addImages(self, images_list):
        "Adds an operation from the current selections of images and directories."
        selected_items = images_list.selectedItems()
        
        # Add images that aren't already added
        current_images = set(self.currentImages())
        for item in selected_items:
            image = item.data(USER_ROLE)
            if image not in current_images:
                current_images.add(image)
                self.addItem(item.text())
                self.item(self.count - 1).setData(USER_ROLE, image)
        
    def removeImages(self):
        "Removes any currently selected operations."
        for item in reversed(self.selectedItems()):     # reverse so indices aren't modified
            index = self.row(item)
            self.takeItem(index)
        
# ------------------------------------------------------------------------------
def updateFilter(filter_box, images_list):
    "For each item in the image list display, set it to hidden if it doesn't match the filter text."
    match_words = filter_box.text.lower().split()
    for item_index in range(images_list.count):
        item = images_list.item(item_index)
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

        return True
        
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False

# ------------------------------------------------------------------------------    
if __name__ == "__main__":
    exportImageManagerImages()