# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
#                                     DO NOT DELETE THIS SCRIPT!
# ------------------------------------------------------------------------------
# Create J Tools menu
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

import mari, re
from os.path import abspath, dirname, join
from inspect import getfile, currentframe

version = "0.03"

# ------------------------------------------------------------------------------
def createJToolsMenu(menu_items):
    menu_items = sorted(menu_items)
    action_dict = {}
    for key_name in menu_items:
        action_dict[key_name] = mari.actions.create(convert(key_name), "mari.jtools." + key_name + "()")
        if "channel" in key_name.lower() and not "template" in key_name.lower():
            mari.menus.addAction(action_dict[key_name], "MainWindow/Sc&ripts/&J-Tools/Channel")
        elif "template" in key_name.lower():
            mari.menus.addAction(action_dict[key_name], "MainWindow/Sc&ripts/&J-Tools/Channel/Template")
        else:
            mari.menus.addAction(action_dict[key_name], "MainWindow/Sc&ripts/&J-Tools")
        if key_name == "update":
            icon_filename = "SaveToImageManager.png"
            icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
            action_dict[key_name].setIconPath(icon_path)

# ------------------------------------------------------------------------------   
def convert(name):
    first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    all_cap_re = re.compile('([a-z0-9])([A-Z])')
    s1 = first_cap_re.sub(r'\1 \2', name)
    return all_cap_re.sub(r'\1 \2', s1).title()