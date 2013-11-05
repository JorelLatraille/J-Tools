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

import mari, re
from os.path import abspath, dirname, join
from inspect import getfile, currentframe

version = "0.02"

# ------------------------------------------------------------------------------
def createJToolsMenu():
    if not getImported():
        return False
        
    imported = getImported()
    imported = sorted(imported)
        
    action_dict = {}
    for key_name in imported:
        action_dict[key_name] = mari.actions.create(convert(key_name), "jtools." + key_name + "()")
        mari.menus.addAction(action_dict[key_name], "MainWindow/Sc&ripts/&J-Tools")
        if key_name == "update":
            icon_filename = "SaveToImageManager.png"
            icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
            action_dict[key_name].setIconPath(icon_path)

# ------------------------------------------------------------------------------        
def getImported():
    file_path = dirname(abspath(getfile(currentframe()))) # script directory
    file_path = join(file_path, "__init__.py")
    imported = []

    try:
        with open(file_path) as file:
            for line in file:
                if line[0] == "#":
                    quote = True
                elif line[0] == "v":
                    version = True
                elif line[0] == "d":
                    break
                elif len(line.strip()) > 0:
                    list_words = line.split()
                    imported.extend(list_words[-1:])
                else:
                    pass
    except IOError:
        print 'No __init__.py file'
        return False

    return imported

# ------------------------------------------------------------------------------   
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')
def convert(name):
    s1 = first_cap_re.sub(r'\1 \2', name)
    return all_cap_re.sub(r'\1 \2', s1).title()