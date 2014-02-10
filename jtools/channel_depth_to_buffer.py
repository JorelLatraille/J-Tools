# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Link the current channels bit depth to the buffer bit depth
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

_GEOS = set([])

# ------------------------------------------------------------------------------
def linkChannelDepthToBuffer():
    mari.utils.connect(mari.geo.entityMadeCurrent, _currentGeo)
    _currentGeo(mari.geo.current())

# ------------------------------------------------------------------------------
def _currentGeo(geo):
    global _GEOS
    _GEOS.add(geo)
    mari.utils.connect(geo.channelMadeCurrent, _setBuffer)
    _setBuffer(geo.currentChannel())

# ------------------------------------------------------------------------------
def unlinkChannelDepthToBuffer():
    global _GEOS
    mari.utils.disconnect(mari.geo.entityMadeCurrent, _currentGeo)
    for geo in _GEOS:
        mari.utils.disconnect(geo.channelMadeCurrent, _setBuffer)
    _GEOS = set([])

# ------------------------------------------------------------------------------
def _setBuffer(channel):
    if channel:
        mari.canvases.paintBuffer().setDepth(channel.depth())

# ------------------------------------------------------------------------------
# Add action to Mari menu.
action = mari.actions.create('Link Channel Depth To Buffer', 'linkChannelDepthToBuffer()')
mari.menus.addAction(action, "MainWindow/&Channels/&Buffer")
icon_filename = "Linked.png"
icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
action.setIconPath(icon_path)

action = mari.actions.create('Unlink Channel Depth To Buffer', 'unlinkChannelDepthToBuffer()')
mari.menus.addAction(action, "MainWindow/&Channels/&Buffer")
icon_filename = "Unlinked.png"
icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
action.setIconPath(icon_path)