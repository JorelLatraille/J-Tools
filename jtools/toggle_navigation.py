# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Toggle navigation lock
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
toggle = False

# ------------------------------------------------------------------------------
def toggleNavigation():
    "Toggle navigation lock"
    global toggle
    if not toggle:
        action = mari.actions.get('/Mari/Tools/Navigation/Orbit Disabled')
        action.trigger()
        action = mari.actions.get('/Mari/Tools/Navigation/Pan Disabled')
        action.trigger()       
        action = mari.actions.get('/Mari/Tools/Navigation/Zoom Disabled')
        action.trigger()
        toggle = True
    else:
        action = mari.actions.get('/Mari/Tools/Navigation/Orbit All')
        action.trigger()
        action = mari.actions.get('/Mari/Tools/Navigation/Pan All')
        action.trigger()       
        action = mari.actions.get('/Mari/Tools/Navigation/Zoom Enabled')
        action.trigger()
        toggle = False

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    toggleNavigation()

# ------------------------------------------------------------------------------
# Add action to Mari menu.
action = mari.actions.create("Toggle Navigation", "toggleNavigation()")
mari.menus.addAction(action, "MainWindow/&Camera")
icon_filename = "Lock.png"
icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
action.setIconPath(icon_path)