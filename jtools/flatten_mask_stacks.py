# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Flatten mask stacks for current entity channel layers.
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

import mari
from PythonQt.QtGui import *

version = "0.01"

# ------------------------------------------------------------------------------
class flattenMaskStacksGUI(QDialog):
    "Create ImportImagesGUI"
    def __init__(self, parent=None):
        super(flattenMaskStacksGUI, self).__init__(parent)

        #Set title and create the major layouts
        self.setWindowTitle('Flatten Mask Stacks')
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        message = QLabel("Are you sure you wish to flatten all the current geo's channel layer mask stacks?")
        yes = QPushButton('Yes')
        no = QPushButton('no')
        yes.connect('clicked()', self.accept)
        no.connect('clicked()', self.reject)

        button_layout.addWidget(yes)
        button_layout.addWidget(no)
        main_layout.addWidget(message)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

# ------------------------------------------------------------------------------
def flattenMaskStacks():
    "Flatten mask stacks for current entity channel layers."
    if not isProjectSuitable():
        return

    #Create dialog and return inputs
    dialog = flattenMaskStacksGUI()
    if dialog.exec_():

        geo = mari.geo.current()
        channel_list = geo.channelList()
        for channel in channel_list:
            layer_list = channel.layerList()
            layer_list = getMatchingLayers(layer_list, returnTrue)
            for layer in layer_list:
                if layer.hasMaskStack():
                    mask_stack = layer.maskStack()
                    mask_stack.mergeLayers(mask_stack.layerList())
                    mask_layer = mask_stack.layerList()[0]
                    mask_layer.setName(layer.name() + '.Mask') #Rename new flattened layer to layer name + .Mask

        mari.utils.message('Flatten process complete.')

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
        
    return matching

# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state."
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
    
        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False

        return True
    
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False

# ------------------------------------------------------------------------------ 
if __name__ == "__main__":
   flattenMaskStacks()