# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Resize all geometry channels or selected geometry's channels
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
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

version = "0.04"

g_resolutions = [str(QtCore.QSize.width()) for QtCore.QSize in mari.images.supportedTextureSizes()]
g_rc_window = None

# ------------------------------------------------------------------------------
def resizeChannels(g_rc_window, resolutions, all_geo_box):
    "Resize all geometry channels or selected geometry's channels."
    g_rc_window.accept()
    resolution = int(resolutions.currentText())
    all_geo = all_geo_box.isChecked()
    
    if not all_geo:
        geo = mari.geo.current()
        channel_list = geo.channelList()
        for channel in channel_list:
            channel.resize(resolution)
                
    else:
        geo_list = mari.geo.list()
        for geo in geo_list:
            channel_list = geo.channelList()
            for channel in channel_list:
                channel.resize(resolution)
                    
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
    main_ok_button.clicked.connect(lambda: resizeChannels(g_rc_window, resolutions, all_geo_box))
    main_cancel_button.clicked.connect(g_rc_window.reject)
    
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

    # ------------------------------------------------------------------------------
# Add action to Mari menu.
action = mari.actions.create(
    "Resize Channels", "mari.jtools.resizeChannels()"
    )
mari.menus.addAction(action, 'MainWindow/&Channels/Resize')
mari.menus.addSeparator('MainWindow/&Channels/Resize', 'Resize Channels')
icon_filename = "ManageToolbars.png"
icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
action.setIconPath(icon_path)