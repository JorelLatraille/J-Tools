# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Get, set and create a channel template from a current channel, a template
# consists of the channel bit depth, and patch resolutions.
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

version = "0.01"
geo_dict = {}

# ------------------------------------------------------------------------------
def getChannelTemplate():
    "Get current channel's patch resolutions and create a template."
    if not _isProjectSuitable():
        return
    global geo_dict
    geo = mari.geo.current()
    channel = mari.current.channel()
    geo_dict[geo] = []
    geo_dict[geo].append(channel.depth())
    for patch in geo.patchList():
        geo_dict[geo].append([channel.width(patch.uvIndex()), patch.uvIndex()])

# ------------------------------------------------------------------------------
def setChannelFromTemplate():
    "Set current channel's patch resolutions from a template."
    if not _isProjectSuitable():
        return
    geo = mari.geo.current()
    if not geo_dict.has_key(geo):
        mari.utils.message('There is no template for the current geometry, please get a template.')
        return
    channel = mari.current.channel()
    for item in geo_dict[geo]:
        if item == geo_dict[geo][0]:
            continue
        try:
            channel.resize(item[0], [item[1],])
        except Exception, e:
            print(e)

# ------------------------------------------------------------------------------
def createChannelFromTemplate():
    "Create a channel from a template."
    if not _isProjectSuitable():
        return
    geo = mari.geo.current()
    if not geo_dict.has_key(geo):
        mari.utils.message('There is no template for the current geometry, please get a template.')
        return
    channel = geo.createChannel(name, geo_dict[geo][1][0], geo_dict[geo][1][0], geo_dict[geo][0])
    for item in geo_dict[geo]:
        if item == geo_dict[geo][0]:
            continue
        try:
            channel.resize(item[0], [item[1],])
        except Exception, e:
            print(e)

# ------------------------------------------------------------------------------
def _isProjectSuitable():
    "Checks project state."
    MARI_2_5V2_VERSION_NUMBER = 20502300    # see below
    if mari.app.version().number() >= MARI_2_5V2_VERSION_NUMBER:
    
        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False

        if mari.current.channel() is None:
            mari.utils.message("Please select a channel before running.")
            return False

        return True
    
    else:
        mari.utils.message("You can only run this script in Mari 2.5v2 or newer.")
        return False

# ------------------------------------------------------------------------------
# Add action to Mari menu.
action = mari.actions.create(
    "Get Channel Template", "mari.jtools.getChannelTemplate()"
    )
mari.menus.addAction(action, "MainWindow/&Channels/Template")
icon_filename = "Channel.png"
icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
action.setIconPath(icon_path)

action = mari.actions.create(
    "Create Channel From Template", "mari.jtools.createChannelFromTemplate()"
    )
mari.menus.addAction(action, "MainWindow/&Channels/Template")
icon_filename = "AddChannel.png"
icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
action.setIconPath(icon_path)

action = mari.actions.create(
    "Set Channel From Template", "mari.jtools.setChannelFromTemplate()"
    )
mari.menus.addAction(action, "MainWindow/&Channels/Template")
icon_filename = "ChannelPresets.png"
icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
action.setIconPath(icon_path)