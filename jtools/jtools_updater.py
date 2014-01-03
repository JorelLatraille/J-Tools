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

import mari, os, shutil
from inspect import getfile, currentframe

# ------------------------------------------------------------------------------
def locate(pattern, path):
    "Locate all files matching supplied filename pattern in and below supplied directory"
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir == pattern:
                return os.path.join(root, dir)
            
    return False

# ------------------------------------------------------------------------------
def updating(update_path):
    "Update J-Tools with supplied updater, also remove depricated files if they exist"
    scripts_path = os.path.abspath(mari.resources.path(mari.resources.USER_SCRIPTS))

    if mari.app.version().isWindows():
        split_scripts_path = scripts_path.split(';')
    else:
        split_scripts_path = scripts_path.split(':')

    found = False
    path = ''
    for s_path in split_scripts_path:
        if locate("jtools", s_path):
            found = True
            path = s_path
            break

    if not found:
        mari.utils.message("Could not find J-Tools script directory.")
        return False

    jtools_path = locate("jtools", path)
            
    #Version 0.01 files to remove
    depricated = [os.path.join(jtools_path, "copy_patch_to_patches.py"), os.path.join(jtools_path, "copy_patch_to_patches.pyc"),
    #Version 0.03 files to remove
    os.path.join(jtools_path, "export_images_flattened.py"), os.path.join(jtools_path, "export_images_flattened.pyc"),
    os.path.join(jtools_path, "wip_export_token_images_flattened.py"), os.path.join(jtools_path, "wip_export_token_images_flattened.pyc"),
    os.path.join(jtools_path, "updater.py"), os.path.join(jtools_path, "updater.pyc")]

    for file in depricated:
        if os.path.exists(file):
            try:
                os.remove(file)    
            except Exception, e:
                mari.app.log(e)
                print(e)
        
    source_files = os.listdir(update_path)
    for file_name in source_files:
        if not file_name == "jtools_updater.py":
            full_file_name = os.path.join(update_path, file_name)
            if (os.path.isfile(full_file_name)):
                try:
                    shutil.copy(full_file_name, jtools_path)
                except Exception, e:
                    mari.app.log(e)
                    print(e)
            
    return True
                
# ------------------------------------------------------------------------------    
if __name__ == "__main__":
    updating(update_path)