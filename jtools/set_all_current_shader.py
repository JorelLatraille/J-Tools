# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Set all geometry shaders to selected shader
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

version = "0.01"

# ------------------------------------------------------------------------------
def setAllCurrentShader():
    "Set all geometry shaders to selected shader"
    if not isProjectSuitable(): #Check if project is suitable
        return False        
        
    geo = mari.geo.current()
    geo_list = mari.geo.list()
    shader = geo.currentShader()
    shader_list = list(geo.shaderList())
    sIndex = shader_list.index(shader)
        
    for geo in geo_list:
        if len(geo.shaderList()) == len(shader_list):
            geo_shader_list = geo.shaderList()
            geo_shader = geo_shader_list[sIndex]
            geo.setCurrentShader(geo_shader)
        elif sIndex < len(geo.shaderList()):
            geo_shader_list = geo.shaderList()
            geo_shader = geo_shader_list[sIndex]
            geo.setCurrentShader(geo_shader)
    
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
            mari.utils.message("Please select an object to set shader from.")
            return False

        shader = mari.geo.current().currentShader()
        if shader is None:
            mari.utils.message("Please select a shader to set shader from.")
            return False

        return True
        
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False   

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    setAllCurrentShader()