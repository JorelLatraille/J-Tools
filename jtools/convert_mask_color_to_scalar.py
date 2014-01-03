# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Converts all masks from color to scalar on current geometry
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
import PythonQt.QtGui as QtGui

version = "0.04"

# ------------------------------------------------------------------------------
class ConvertMaskColorToScalarGUI(QtGui.QDialog):
    "Create ConvertMaskColorToScalarGUI"
    def __init__(self, parent=None):
        super(ConvertMaskColorToScalarGUI, self).__init__(parent)

        #Set title and create the major layouts
        self.setWindowTitle('Convert Mask Color To Scalar')
        main_layout = QtGui.QVBoxLayout()
        button_layout = QtGui.QHBoxLayout()

        message = QtGui.QLabel("Are you sure you wish to convert the current geo's masks from color to scalar?")
        yes = QtGui.QPushButton('Yes')
        no = QtGui.QPushButton('no')
        yes.connect('clicked()', self.accept)
        no.connect('clicked()', self.reject)

        button_layout.addWidget(yes)
        button_layout.addWidget(no)
        main_layout.addWidget(message)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

# ------------------------------------------------------------------------------ 
def convertMaskColorToScalar():
    "Converts all masks on non shared layers from Color to Scalar"

    if not isProjectSuitable(): #Check if project is suitable
        return False
    
    #Create dialog and return inputs
    dialog = ConvertMaskColorToScalarGUI()
    if dialog.exec_():

        channel_list = mari.geo.current().channelList()
        mask_layer_list = []
        for channel in channel_list:
            all_layers = getMatchingLayers(channel.layerList(), returnTrue)
            mask_layers = []
            for layer in all_layers:
                if layer.hasMask() and not layer.hasMaskStack():
                    mask_layers.append(layer)
                if layer.hasMaskStack():
                    mask_layers.extend(layer.maskStack().layerList())
            
            # Remove shared layers from the list
            for layer in mask_layers:
                if layer in mask_layer_list:
                    pass
                else:
                    mask_layer_list.append(layer)

        # Get list of images
        mask_images = {}
        for layer in mask_layer_list:
            if layer.hasMask() and not layer.hasMaskStack():
                mask_images[layer.name()] = layer.maskImageSet().imageList()
            elif layer.isPaintableLayer():
                mask_images[layer.name()] = layer.imageSet().imageList()
        
        for key in mask_images:
            print "%s old color space: %d" %(key, mask_images[key][0].colorSpace())
            for image in mask_images[key]:
                image.setColorSpace(1)
        
        print ""
        
        for key in mask_images:
            print "%s new color space: %d" %(key, mask_images[key][0].colorSpace())

        mari.utils.message('Conversion complete.')

# ------------------------------------------------------------------------------    
def returnTrue(layer):
    "Returns True for any object passed to it."
    return True
    
# ------------------------------------------------------------------------------
def getMatchingLayers(layer_list, criterionFn):
    "Returns a list of all of the layers in the stack that match the given criterion function, including substacks."
    matching = []
    for layer in layer_list:
        if criterionFn(layer):
            matching.append(layer)
        if hasattr(layer, 'layerStack'):
            matching.extend(getMatchingLayers(layer.layerStack().layerList(), criterionFn))
        if layer.hasMaskStack():
            matching.extend(getMatchingLayers(layer.maskStack().layerList(), criterionFn))
        if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
            matching.extend(getMatchingLayers(layer.adjustmentStack().layerList(), criterionFn))
        
    return matching
    
# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state and Mari version."
    MARI_2_5V1_VERSION_NUMBER = 20501300    # see below
    if mari.app.version().number() >= MARI_2_5V1_VERSION_NUMBER:
        
        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False
        
        chan = mari.geo.current().currentChannel()
        if chan is None:
            mari.utils.message("Please create a channel to run.")
            return False

        return True
        
    else:
        mari.utils.message("You can only run this script in Mari 2.5v1 or newer.")
        return False

# ------------------------------------------------------------------------------    
if __name__ == "__main__":
    convertMaskColorToScalar()