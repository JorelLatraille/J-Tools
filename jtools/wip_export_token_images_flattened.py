# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Export all channels flattened for all geo in the project with specified token
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
def exportTokenImagesFlattened():
    "Export all channels flattened for all geo in the project with specified token."
    if not isProjectSuitable(): #Check if project is suitable
        return False    
    
    geo_list = mari.geo.list()

    for geo in geo_list:
        channel_list = geo.channelList()
        for channel in channel_list:
            channelSize = channel.width()
            channel.setMetadata('SIZE', channelSize)
            channel.setMetadataEnabled('SIZE', 0)
            channel.exportImagesFlattened("/path/to/export/directory/$ENTITY.$SIZE.$UDIM.tif")
            
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
    exportTokenImagesFlattened()