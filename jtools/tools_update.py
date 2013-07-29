# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
#                                     DO NOT DELETE THIS SCRIPT!
# ------------------------------------------------------------------------------
# Update J-Tools
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

import mari, sys, os, PythonQt

version = "0.01"

def update():
    "Update J-Tools"
    updater_path = mari.utils.misc.getOpenFileName(parent=None, caption='Update J-Tools', dir='', filter='*.py', selected_filter=None, options=0)
    if updater_path == '':
        return False
    if not "updater.py" in updater_path:
        mari.utils.message("Please select the updater.py file.")
        return False
    else:
        path = updater_path.replace("updater.py", "")
        path = os.path.abspath(path)
        sys.path.append(path)
        from updater import updating
        
        if updating():
            mari.utils.message("Update successful.")
        else:
            mari.utils.message("Update was unsuccessful.")

#-------------------------------------------------------------------------------    
if __name__ == "__main__":
    update()