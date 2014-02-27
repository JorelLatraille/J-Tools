# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Copy channels from one object to another
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
import PythonQt.QtGui as QtGui

version = "0.03"

# ------------------------------------------------------------------------------
def copyChannels():
    "Copy channels from one object to another."
    if not isProjectSuitable(): #Check if project is suitable
        return False    
    
    geo_list = mari.geo.list()
    if not fromGeoToGeo():
        return False
    geo_names = fromGeoToGeo()
    geo_copy = geo_names[0]
    geo_paste = geo_names[1]
    
    for geo in geo_list:
        if geo_copy == geo.name():
            geo_copy = geo
        elif geo_paste == geo.name():
            geo_paste = geo
        else:
            pass
    
    checkGeoNames(geo_copy, geo_paste)
    
# ------------------------------------------------------------------------------        
def fromGeoToGeo():
    "GUI's for user input."
    fu = QtGui.QInputDialog()
    fuInput = fu.getText(fu, 'To copy from','Object name e.g. head_old')
    tu = QtGui.QInputDialog()
    tuInput = tu.getText(tu, 'To copy to','Object name e.g. head_new')
    geo_names = (fuInput,tuInput)
    if '' in geo_names:
        return False
    return geo_names

# ------------------------------------------------------------------------------            
def checkGeoNames(geo_copy, geo_paste):
    "Check the names given are unique and are in the object list"
    if geo_copy == geo_names[0] or geo_paste == geo_names[1]:
        mari.utils.message("Please make sure the names of the objects given match the names in the object list.")
        copyChannels()
    elif geo_copy == geo_paste:
        mari.utils.message("Please make sure the names of the objects given are unique.")
        copyChannels()
    else:
        copy = mari.actions.get('/Mari/Channels/Copy')
        paste = mari.actions.get('/Mari/Channels/Paste')
        
        for channel in geo_copy.channelList():
            geo_copy.setSelected(True)
            channel.makeCurrent()
            copy.trigger()
            geo_paste.setSelected(True)
            paste.trigger()
    
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
    copyChannels()

# ------------------------------------------------------------------------------
# Add action to Mari menu.
action = mari.actions.create(
    "Copy Channels", "mari.jtools.copyChannels()"
    )
mari.menus.addAction(action, "MainWindow/&Channels", "Copy")
icon_filename = "CopyChannel.png"
icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
action.setIconPath(icon_path)