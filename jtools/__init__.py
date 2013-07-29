# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
#                                DO NOT DELETE THIS SCRIPT!
# ------------------------------------------------------------------------------
# Initialisation script for J-Tools
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

version = "0.02"

# ------------------------------------------------------------------------------
# Use from and import, to import the main function from the module
from batch_archive import batchArchive
from convert_mask_color_to_scalar import convertMaskColorToScalar
from convert_to_paintable import convertToPaintable
from copy_channels import copyChannels
from copy_udim_to_udim import showUI as copyUdimToUdim
from export_images_flattened import exportImagesFlattened
from layer_visibility import layerVisibility
from resize_channels import showUI as resizeChannels
from set_all_current_shader import setAllCurrentShader
from shortcuts import quick
from wip_export_channels import showUI as exportChannels
from wip_export_token_images_flattened import exportTokenImagesFlattened
from tools_update import update

# ------------------------------------------------------------------------------
# Only del the module name if you dont wish users to have access to its other functions
del batch_archive
del convert_mask_color_to_scalar
del convert_to_paintable
del copy_channels
del copy_udim_to_udim
del export_images_flattened
del layer_visibility
del resize_channels
del set_all_current_shader
del shortcuts
del wip_export_channels
del wip_export_token_images_flattened
del tools_update

# ------------------------------------------------------------------------------
# DO NOT REMOVE THE BELOW! This is used to generate the menu inside of Mari!

from tools_menu import createJToolsMenu

createJToolsMenu()

del tools_menu
del createJToolsMenu