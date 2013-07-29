# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
#                                     DO NOT DELETE THIS SCRIPT!
# ------------------------------------------------------------------------------
# Updater for J-Tools
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

import mari, os, shutil
from inspect import getfile, currentframe

# ------------------------------------------------------------------------------
def updating():
    update_path = os.path.dirname(os.path.abspath(getfile(currentframe())))
    scripts_path = os.path.abspath(mari.resources.path(mari.resources.USER_SCRIPTS))
    if not locate("jtools", scripts_path):
        mari.utils.message("Could not find J-Tools script directory.")
        return False
    jtools_path = locate("jtools", scripts_path)
    
    source_files = os.listdir(update_path)
    for file_name in source_files:
        full_file_name = os.path.join(update_path, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, jtools_path)
    
    depricated = os.path.join(jtools_path, "copy_patch_to_patches.py"), os.path.join(jtools_path, "copy_patch_to_patches.pyc")

    for file in depricated:
        if os.path.exists(file):
            os.remove(file)
            
    return True
    
# ------------------------------------------------------------------------------
def locate(pattern, root):
    "Locate all files matching supplied filename pattern in and below supplied directory"
    for path, dirs, files in os.walk(root):
        for dir in dirs:
            if dir == pattern:
                return os.path.join(path, dir)
            
    return False
    
# ------------------------------------------------------------------------------    
if __name__ == "__main__":
    updating()