# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Make selected layers visible or invisible
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

version = "0.01"

# ------------------------------------------------------------------------------
def layerVisibility():
    "Make selected layers visible or invisible."
    if not isProjectSuitable(): #Check if project is suitable
        return False        

    geo = mari.geo.current()
    channel = geo.currentChannel()
    layer_list = getLayerList(channel.layerList())
    selected = getSelected(layer_list)
    selectedVisible = getSelectedVisible(selected)
     
    if len(selectedVisible) < len(selected) / 2 or len(selectedVisible) == 0:
        for layer in selected:
            layer.setVisibility(True)
    else:
        for layer in selected:
            layer.setVisibility(False)
                
# ------------------------------------------------------------------------------ 
def checkSelected(selected):
    "Returns a list of non maskStack and non adjustmentStack layers."
    matching = []
    for layer in selected:
            matching.append(layer)
            
    return matching
                
# ------------------------------------------------------------------------------    
def getSelected(layer_list):
    "Returns a list of selected layers."
    matching = []
    for layer in layer_list:
        if layer.isSelected():
            matching.append(layer)
            
    return matching
    
# ------------------------------------------------------------------------------    
def getSelectedVisible(layer_list):
    "Returns a list of visible layers."
    matching = []
    for layer in layer_list:
        if layer.isVisible():
            matching.append(layer)
            
    return matching
    
# ------------------------------------------------------------------------------
def getLayerList(layer_list):
    "Returns a list of all of the layers in the stack and substacks but not those in a maskStack or adjustmentStack."
    matching = []
    for layer in layer_list:
        matching.append(layer)
        if layer.isGroupLayer():
            matching.extend(getLayerList(layer.layerStack().layerList()))
    
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
    layerVisibility()