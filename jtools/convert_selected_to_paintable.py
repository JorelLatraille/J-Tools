# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Convert selected layers to paintable layers
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
import PySide.QtGui as QtGui

version = "0.04"

# ------------------------------------------------------------------------------
class ConvertToPaintableUI(QtGui.QDialog):
    "Create ConvertToPaintableUI"
    def __init__(self, parent=None):
        super(ConvertToPaintableUI, self).__init__(parent)

        #Set title and create the major layouts
        self.setWindowTitle('Convert To Paintable')
        main_layout = QtGui.QVBoxLayout()
        button_layout = QtGui.QHBoxLayout()

        message = QtGui.QLabel("Are you sure you wish to convert the selected layers to paintable?")
        yes = QtGui.QPushButton('Yes')
        no = QtGui.QPushButton('no')
        yes.clicked.connect(self.accept)
        no.clicked.connect(self.reject)

        button_layout.addWidget(yes)
        button_layout.addWidget(no)
        main_layout.addWidget(message)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

# ------------------------------------------------------------------------------
def convertSelectedToPaintable():
    "Convert selected layers to paintable layers."
    if not isProjectSuitable(): #Check if project is suitable
        return False
    
    #Create dialog and return inputs
    dialog = ConvertToPaintableUI()
    if not dialog.exec_():
        return

    geo = mari.geo.current()
    channel = geo.currentChannel()
    layer_list = getLayerList(channel.layerList(), returnTrue)
    selected = getSelected(layer_list)
        
    for layer in selected:
        layer.makeCurrent()
        convertToPaintable = mari.actions.get('/Mari/Layers/Convert To Paintable')
        convertToPaintable.trigger()
                
# ------------------------------------------------------------------------------    
def getSelected(layer_list):
    "Returns a list of selected layers."
    matching = []
    for layer in layer_list:
        if layer.isSelected():
            matching.append(layer)
            
    return matching
    
# ------------------------------------------------------------------------------    
def returnTrue(layer):
    "Returns True for any object passed to it."
    return True
    
# ------------------------------------------------------------------------------
def getLayerList(layer_list, criterionFn):
    "Returns a list of all of the layers in the stack that match the given criterion function, including substacks."
    matching = []
    for layer in layer_list:
        if criterionFn(layer):
            matching.append(layer)
        if hasattr(layer, 'layerStack'):
            matching.extend(getLayerList(layer.layerStack().layerList(), criterionFn))
        if layer.hasMaskStack():
            matching.extend(getLayerList(layer.maskStack().layerList(), criterionFn))
        if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
            matching.extend(getLayerList(layer.adjustmentStack().layerList(), criterionFn))
        
    return matching
    
# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state and Mari version."
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
        
        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False
            
        geo = mari.geo.current()
        if geo is None:
            mari.utils.message("Please select an object to run.")
            return False
        
        chan = geo.currentChannel()
        if chan is None:
            mari.utils.message("Please select a channel to run.")
            return False
            
        if len(chan.layerList()) == 0:
            mari.utils.message("Please select a layer to run.")
            return False

        return True
        
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    convertSelectedToPaintable()

# ------------------------------------------------------------------------------
# Add action to Mari menu.
action = mari.actions.create(
    "Convert Selected To Paintable", "mari.jtools.convertSelectedToPaintable()"
    )
mari.menus.addAction(action, "MainWindow/&Layers", "Convert To Paintable")
icon_filename = "Painting.png"
icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
action.setIconPath(icon_path)