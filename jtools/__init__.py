# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
#                                DO NOT DELETE THIS SCRIPT!
# ------------------------------------------------------------------------------
# Initialisation script for J-Tools
# coding: utf-8
# Written by Jorel Latraille
# ------------------------------------------------------------------------------
#                                       VERSION 0.05
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

import mari, inspect, os

version = "0.05"

# ------------------------------------------------------------------------------
# Use from and import, to import the main function from the module
import action_path_finder
import batch_archive
import change_geo_version_path
import channel_template
import class_method_finder
import convert_mask_color_to_scalar
import convert_to_paintable
import copy_channels
import copy_udim_to_udim
import create_directories_move_files
import export_image_manager_images
import export_selected_channels
import export_uv_masks
import flatten_mask_stacks
import flatten_selected_channels
import import_images
import layer_visibility
import playblaster
import resize_channels
import set_all_current_shader
import shortcuts
import toggle_navigation
import tools_update

# ------------------------------------------------------------------------------
class JTools():

    def actionPathFinder(self):
        action_path_finder.actionPathFinder()

    def batchArchive(self):
        batch_archive.batchArchive()

    def changeGeoVersionPath(self):
        change_geo_version_path.changeGeoVersionPath()

    def classMethodFinder(self):
        class_method_finder.classMethodFinder()

    def convertMaskColorToScalar(self):
        convert_mask_color_to_scalar.convertMaskColorToScalar()

    def convertToPaintable(self):
        convert_to_paintable.convertToPaintable()

    def copyChannels(self):
        copy_channels.copyChannels()

    def copyUdimToUdim(self):
        copy_udim_to_udim.showUI()

    def createChannelTemplate(self):
        channel_template.createChannelTemplate()
        
    def createDirectoriesMoveFiles(self):
        create_directories_move_files.createDirectoriesMoveFiles()

    def exportImageManagerImages(self):
        export_image_manager_images.exportImageManagerImages()

    def exportSelectedChannels(self):
        export_selected_channels.exportSelectedChannels()

    def exportUVMasks(self):
        export_uv_masks.exportUVMasks()

    def flattenMaskStacks(self):
        flatten_mask_stacks.flattenMaskStacks()

    def flattenSelectedChannels(self):
        flatten_selected_channels.flattenSelectedChannels()

    def getChannelTemplate(self):
        channel_template.getChannelTemplate()

    def importImages(self):
        import_images.importImages()

    def layerVisibility(self):
        layer_visibility.layerVisibility()

    def playblast(self):
        playblaster.playblast()

    def resizeChannels(self):
        resize_channels.showUI()

    def setAllCurrentShader(self):
        set_all_current_shader.setAllCurrentShader()

    def setChannelTemplate(self):
        channel_template.setChannelTemplate()

    def quick(self):
        shortcuts.quick()

    def toggleNavigation(self):
        toggle_navigation.toggleNavigation()

    def update(self):
        tools_update.update()

# ------------------------------------------------------------------------------
mari.jtools = JTools()

# ------------------------------------------------------------------------------
# DO NOT REMOVE THE BELOW! This is used to generate the menu inside of Mari!
import tools_menu

tools_menu.createJToolsMenu([method for method, instance in inspect.getmembers(mari.jtools, predicate=inspect.ismethod)])

# ------------------------------------------------------------------------------
# DO NOT REMOVE THE BELOW! This is used to cleanup any residual update files!
scripts_path = os.path.abspath(mari.resources.path(mari.resources.USER_SCRIPTS))

if mari.app.version().isWindows():
    split_scripts_path = scripts_path.split(';')
else:
    split_scripts_path = scripts_path.split(':')

for s_path in split_scripts_path:
    jtools_path = os.path.join(s_path, "jtools")
    depricated = [os.path.join(jtools_path, "updater.py"), os.path.join(jtools_path, "updater.pyc"),
    os.path.join(jtools_path, "jtools_updater.py"), os.path.join(jtools_path, "jtools_updater.pyc")]
    for file in depricated:
        if os.path.exists(file):
            os.remove(file)