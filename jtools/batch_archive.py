# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Batch archiving script for Mari projects
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
def batchArchive():
    "Batch archiving script for Mari projects"
    
    if not isProjectSuitable():
        return False
        
    archive_path = mari.utils.misc.getExistingDirectory(parent=None, caption='Batch Archive', dir='')
    if archive_path == '':
        return
    
    projects_list = mari.projects.list()
    for project in projects_list:
        project_name = project.name()
        uuid = project.uuid()
        mari.projects.archive(uuid, archive_path + project_name + ".mra")
        mari.app.startProcessing("Archiving Projects", num_steps=100, can_cancel=True)
        mari.app.stopProcessing()
        mari.app.log("Archived: %s in directory: %s" %(project_name, archive_path))
        print "Archived: %s in directory: %s" %(project_name, archive_path)
    
    mari.utils.message("Archive Successful.")
        
# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state and Mari version."
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
        
        if mari.projects.current() is not None:
            mari.utils.message("Please close project before running.")
            return False
            
        return True
        
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False

# ------------------------------------------------------------------------------         
if __name__ == "__main__":
    batchArchive()