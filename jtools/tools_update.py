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

import mari, sys, os

version = "0.02"

def update():
    "Update J-Tools"
    updater_path = mari.utils.misc.getOpenFileName(parent=None, caption='Update J-Tools', dir='', filter='jtools_updater.py', selected_filter=None, options=0)
    if updater_path == '':
        return
    if not updater_path.endswith("jtools_updater.py"):
        mari.utils.message("Please select the jtools_updater.py file.")
        return
    else:
        path = os.path.split(updater_path)[0]
        path = os.path.abspath(path)
        sys.path.append(path)
        from jtools_updater import updating
        
        if updating(path):
            mari.utils.message("Update successful, please restart Mari.")
        else:
            mari.utils.message("Update was unsuccessful.")

#-------------------------------------------------------------------------------    
if __name__ == "__main__":
    update()