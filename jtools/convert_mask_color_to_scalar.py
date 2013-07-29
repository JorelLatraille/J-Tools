# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Converts all masks from color to scalar, ignores shared layers
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

version = "0.02"

# ------------------------------------------------------------------------------ 
def convertMaskColorToScalar():
    "Converts all masks on non shared layers from Color to Scalar"
    
    if not isProjectSuitable(): #Check if project is suitable
        return False
    
    geometry_list = mari.geo.list()
    
    for geo in geometry_list:
        channel_list = geo.channelList()
        for channel in channel_list:
            all_layers = getMatchingLayers(channel.layerList(), returnTrue)
            mask_layers = []
            for layer in all_layers:
                if layer.hasMask() and not layer.hasMaskStack():
                    mask_layers.append(layer)
                if layer.hasMaskStack():
                    mask_layers.extend(layer.maskStack().layerList())
            
            mask_shared_layers = getSharedLayers(mask_layers)
            
            # Remove shared layers from the list
            mask_layer_list = []
            for layer in mask_layers:
                if layer in mask_shared_layers:
                    pass
                else:
                    mask_layer_list.append(layer)
            
            # Get list of images
            mask_images = {}
            for layer in mask_layer_list:
                if layer.hasMask() and not layer.hasMaskStack():
                    mask_images[layer.name()] = layer.maskImageSet().imageList()
                elif layer.isPaintableLayer():
                    mask_images[layer.name()] = layer.imageSet().imageList()
            
            for key in mask_images:
                print "%s old color space: %d" %(key, mask_images[key][0].colorSpace())
                for image in mask_images[key]:
                    image.setColorSpace(1)
            
            print ""
            
            for key in mask_images:
                print "%s new color space: %d" %(key, mask_images[key][0].colorSpace())

# ------------------------------------------------------------------------------    
def returnTrue(layer):
    "Returns True for any object passed to it."
    return True
    
# ------------------------------------------------------------------------------
def getSharedLayers(layer_list):
    "Returns a list of all of the layers in the layer stack, including in substacks which are shared."
    return getMatchingLayers(layer_list, mari.Layer.isShared)

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
    MARI_2_0V1_VERSION_NUMBER = 20101201    # see below
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
        mari.utils.message("Currently in development this is just a place holder.")
        return False

# ------------------------------------------------------------------------------    
if __name__ == "__main__":
    convertMaskColorToScalar()