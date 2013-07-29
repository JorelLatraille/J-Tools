# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Export all channels flattened for all geo in the project
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

# ------------------------------------------------------------------------------
def exportImagesFlattened():
    "Export all channels flattened for all geo in the project."
    if not isProjectSuitable(): #Check if project is suitable
        return False    
    
    geo_list = mari.geo.list()
    exportInput = mari.utils.misc.getSaveFileName(parent=None, caption='Export Images Flattened', dir='', filter='', selected_filter=None, options=0, save_filename='')
    if exportInput == '':
        return False
        
    if ".exr" in exportInput:
        mari.utils.message("Please remember that exr files can not be created with 8bit channels.")
        
    for geo in geo_list:
        channel_list = geo.channelList()
        for channel in channel_list:
            channel.exportImagesFlattened(exportInput)
    
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
    exportImagesFlattened()