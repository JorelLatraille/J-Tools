# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Quick shortcuts to save typing the same thing over and over
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
def quick():
    "Shortcuts for useful Mari info such as geo name, etc. To use type jtools.quick.<attribute> e.g. jtools.quick.geo_list"
    if not isProjectSuitable():
        return
    
    else:
        quick.geo = mari.geo.current()
        quick.geo_list = list(mari.geo.list())
        quick.geo_index = quick.geo_list.index(quick.geo)
        quick.shader = quick.geo.currentShader()
        quick.shader_list = list(quick.geo.shaderList())
        quick.shader_index = quick.shader_list.index(quick.shader)
        quick.channel = quick.geo.currentChannel()
        quick.channel_list = list(quick.geo.channelList())
        quick.channel_index = quick.channel_list.index(quick.channel)
        quick.layer = quick.channel.currentLayer()
        quick.layer_list = getMatchingLayers(quick.channel.layerList(), returnTrue)
        quick.layer_index = quick.layer_list.index(quick.layer)
        
        print '\n'.join(['',
                "geo: %s" %(quick.geo),'',
                "geo_list: %s" %(quick.geo_list),'', 
                "geo_index: %d" %(quick.geo_index),'',
                "shader: %s" %(quick.shader),'',
                "shader_list: %s" %(quick.shader_list),'',
                "shader_index: %d" %(quick.shader_index),'',
                "channel: %s" %(quick.channel),'',
                "channel_list: %s" %(quick.channel_list),'',
                "channel_index: %d" %(quick.channel_index),'',
                "layer: %s" %(quick.layer),'',
                "layer_list: %s" %(quick.layer_list),'',
                "layer_index: %d" %(quick.layer_index)])
    
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
        
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    quick()