# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Resize all geometry channels or selected geometry's channels
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
import PythonQt.QtGui as QtGui
from PythonQt.QtCore import QSize

version = "0.02"

g_resolutions = [str(QSize.width()) for QSize in mari.images.supportedTextureSizes()]
g_rc_window = None

# ------------------------------------------------------------------------------
def resizeChannels(g_rc_window, resolutions, all_geo_box):
    "Resize all geometry channels or selected geometry's channels."
    g_rc_window.accept()
    resolution = int(resolutions.currentText)
    all_geo = all_geo_box.isChecked()
    
    if not all_geo:
        geo = mari.geo.current()
        channel_list = geo.channelList()
        for channel in channel_list:
            all_layers = getMatchingLayers(channel.layerList(), returnTrue)
            images = []
            for layer in all_layers:
                if layer.isPaintableLayer():
                    images.extend(layer.imageSet().imageList())
                if layer.hasMask() and not layer.hasMaskStack():
                    images.extend(layer.maskImageSet().imageList())
        
            for image in images:
                image.resize(QSize(resolution, resolution))
                
    else:
        geo_list = mari.geo.list()
        for geo in geo_list:
            channel_list = geo.channelList()
            for channel in channel_list:
                all_layers = getMatchingLayers(channel.layerList(), returnTrue)
                images = []
                for layer in all_layers:
                    if layer.isPaintableLayer():
                        images.extend(layer.imageSet().imageList())
                    if layer.hasMask() and not layer.hasMaskStack():
                        images.extend(layer.maskImageSet().imageList())
            
                for image in images:
                    image.resize(QSize(resolution, resolution))
                    
    mari.utils.message("Resize channels successful.")

# ------------------------------------------------------------------------------
def showUI():
    "Resize all geometry channels or selected geometry's channels."
    # Create GUI
    if not isProjectSuitable(): #Check if project is suitable
        return False        
    
    #Create main dialog, add main layout and set title
    global g_rc_window
    g_rc_window = QtGui.QDialog()
    rc_layout = QtGui.QVBoxLayout()
    g_rc_window.setLayout(rc_layout)
    g_rc_window.setWindowTitle("Resize Channels")
    
    #Add main layout.
    main_layout = QtGui.QHBoxLayout()
    
    #Add res options
    resolutions_text = QtGui.QLabel('Resolutions:')
    resolutions = QtGui.QComboBox()
    for resolution in g_resolutions :
        resolutions.addItem(resolution)
    resolutions.setCurrentIndex(resolutions.findText('1024'))
    
    all_geo_box = QtGui.QCheckBox('All Geo')
    
    main_layout.addWidget(resolutions_text)
    main_layout.addWidget(resolutions)
    main_layout.addStretch()
    main_layout.addWidget(all_geo_box)
    main_layout.addStretch()
    
    #Add main buttons layout, buttons and add
    main_ok_button = QtGui.QPushButton("OK")
    main_cancel_button = QtGui.QPushButton("Cancel")
    main_ok_button.connect("clicked()", lambda: resizeChannels(g_rc_window, resolutions, all_geo_box))
    main_cancel_button.connect("clicked()", g_rc_window.reject)
    
    main_layout.addWidget(main_ok_button)
    main_layout.addWidget(main_cancel_button)
    
    rc_layout.addLayout(main_layout)
    
    # Display
    g_rc_window.show()

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
def isProjectSuitable():
    "Checks project state and Mari version."
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
        
        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False
            
        geo = mari.geo.current()
        if geo is None:
            mari.utils.message("Please select an object to run.")
            return False
        
        chan = geo.currentChannel()
        if chan is None:
            mari.utils.message("Please select a channel to run.")
            return False
            
        if len(chan.layerList()) == 0:
            mari.utils.message("Please select a layer to run.")
            return False

        return True
        
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False   
        
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    showUI()