# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
                          ----jorel-latraille.com----
# ------------------------------------------------------------------------------                                        
                                   J-TOOLS
                                   
                              Mari Python Scripts
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

DISCLAIMER & TERMS OF USE:

Copyright (c) The Foundry 2013.
All rights reserved.

This software is provided as-is with use in commercial projects permitted.
Redistribution in commercial projects is also permitted
provided that the above copyright notice and this paragraph are
duplicated in accompanying documentation,
and acknowledge that the software was developed
by The Foundry.  The name of the
The Foundry may not be used to endorse or promote products derived
from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

# ------------------------------------------------------------------------------

Installation Instructions:

1) Extract into the following directory (if you do not have a Scripts folder create one)
    this should be in the same place as your Mari Logs folder:

   /user/documents/Mari/Scripts/

2) Open Mari and you will see a new menu in the menu bar called Scripts. Inside Scripts you will find J-Tools.

3) You can assign keyboard shortcuts to these scripts the same way you assign shortcuts to other elements 
    within Mari. If you open the shortcuts GUI in the edit menu and expand the Scripts tab, at the very bottom
    you will find the name and description of the scripts in the J-Tools menu. You can then double click in the
    Shortcut(s) column and assign them a shortcut.
    
   For an example of this look at the provided keyboardShortcuts.jpg file and the red box
   highlights the J-Tools scripts and the blue box highlights where you need to double click
   to assign a shortcut.

# ------------------------------------------------------------------------------

How to use:

This package will create a new menu called Scripts on your Mari menu bar. Inside the Scripts
menu you will find J-Tools and the following:

Action Path Finder - Action path finder for Mari actions
Batch Archive - Batch archiving script for Mari projects
Class Method Finder - Class method finder for Mari class methods
*Convert Mask Color To Scalar - Converts all masks from color to scalar, ignores shared layers
Convert To Paintable - Convert selected layers to paintable layers
Copy Channels - Copy channels from one object to another
Copy Udim To Udim - Copy paint from one or more patches to other patches, for all layers and channels
Export Image Manager Images - Export selected Image Manager images in your specified file type
Export Images Flattened - Export all channels flattened for all geo in the project
Export Selected Channels - Export selected channels from one or more objects
*Export Token Images Flattened - Export all channels flattened for all geo in the project with specified token
Export UV Masks - Export UV Masks for selected geo
Import Images - Import images into geo layer or channel and rename layer/channel to match image name
Layer Visibility - Make selected layers visible or invisible
Quick - Quick shortcuts to save typing the same thing over and over (Shortcuts for useful Mari info such as geo name, etc. To use type in the python console: jtools.quick.<attribute> e.g. jtools.quick.geo_list)
Resize Channels - Resize all geometry channels or selected geometry's channels
Set All Current Shader - Set all geometry shaders to selected shader
Update - Update J-Tools (This is used to update the J-Tools scripts when a new version is available from jorel-latraille.com)

*In Development

# ------------------------------------------------------------------------------

Extras:

In the jtools folder you will find two scripts which are not in the J-Tools Mari Menu.
This is because they have been written to work in a command line/terminal.

archive_projects.py - An archiving script for creating archives for all projects with your cache directory
extract_projects.py - An extracting script for extracting archives into your project cache directory

# ------------------------------------------------------------------------------

History:

27/09/13 Update Version 0.03 - added several new scripts
29/07/13 Update Version 0.02 - bug fix for Linux and updates to several scripts, removed copy_patch_to_patches
18/07/13 Release Version 0.01
