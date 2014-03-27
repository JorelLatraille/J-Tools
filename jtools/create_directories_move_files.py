# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Creates a directory structure in the path provided using the names of the files in
# the path and moves the files into the newly created directory
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

version = "0.01"

dir_list = []
num_files = 0
moved = 0

# ------------------------------------------------------------------------------ 
def createDirectoriesMoveFiles():
    "Creates a directory structure in the path provided using the names of the files in the path and moves the files into the newly created directory"
    global dir_list, moved, num_files
    
    #Check directory given
    directory_path = mari.utils.misc.getExistingDirectory(parent=None, caption='Choose Directory', dir='')
    if directory_path == '':
        return

    #Print new line for cleanliness in terminal
    print '\n'
    
    #Walk the first level of the provided directory and return a list of file paths to dir_list
    for root, dirs, files in _walkLevel(directory_path):
        for _file in files:
            dir_list.append(os.path.join(directory_path, _file))
    
    #Get the number of files to move
    num_files = len(dir_list)
    
    #Create a file_list without paths and pop the extension
    file_list = []
    extension = ''
    for item in dir_list:
        if os.path.isfile(item):
            _file = os.path.split(item)[1]
            s_file = os.path.splitext(_file)
            file_list.append(s_file[0])
            extension = s_file[1]
    
    #Split the file name using either '.' or '_' and add it to file_dname_list
    file_dname_list = []
    for _file in file_list:
        if '.' in _file:
            file_dname_list.append(_file.split('.'))
            sep = '.'
        elif '_' in _file:
            file_dname_list.append(_file.split('_'))
            sep = '_'
        else:
            file_dname_list.append([_file,])
    
    #Remove the UDIM number from the file name in file_dname_list
    for name_list in file_dname_list:
        for item in name_list:
            try:
                if int(item):
                    name_list.remove(item)
            except:
                pass
    
    #Create directories using the file name structure if they dont already exist
    for dstructure in file_dname_list:
        d_path = ''
        for i in range(len(dstructure)):
            d_path += '%s\\' %dstructure[i]
            if not os.path.exists((os.path.join(directory_path, d_path))):
                print 'mkdir :', os.path.join(directory_path, d_path)
                os.mkdir(os.path.join(directory_path, d_path))

    #Print new line for cleanliness in terminal
    print '\n'
    
    #Move the files from the dir_list to the correct directory in the new directory structure
    for _file in dir_list:
        if os.path.isfile(_file):
            name = os.path.split(_file)[1]
            s_name = os.path.splitext(name)[0]

            #Split the file name with the separator
            if '.' in s_name:
                s_name = s_name.split('.')
            elif '_' in s_name:
                s_name = s_name.split('_')

            #Remove the UDIM number from the file name
            if type(s_name) == list:
                for item in s_name:
                    try:
                        if int(item):
                            s_name.remove(item)
                    except:
                        pass
             
            #Create a path version of the file name which should be the same as the new directory structure
            if type(s_name) == list:
                d_path = '\\'.join(s_name)
            else:
                d_path = s_name
            
            #Try to move the file to the new directory
            try:
                shutil.move(_file, os.path.join(directory_path, d_path))
                print 'mv: %s ---> %s' %(_file, (os.path.join(directory_path, d_path)))
                _progress() #Print the progress
            except Exception, e:
                print "mv Failed: '%s'" %str(e) 
    
    #Print new line for cleanliness in terminal
    print '\n'
        
# ------------------------------------------------------------------------------
def _walkLevel(some_dir, level=0):
    "This is the same as os.walk but you can set the level of directories you wish to search through"
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]
            
# ------------------------------------------------------------------------------                 
def _progress():
    "progress"
    global moved
    moved += 1
    prog = int(moved * 100 / num_files)
    print "%d%% of files %d/%d moved" %(prog, moved, num_files),
            
# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state."
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
        return True
    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False

# ------------------------------------------------------------------------------ 
if __name__ == "__main__":
   createDirectoriesMoveFiles()

# ------------------------------------------------------------------------------
# Add action to Mari menu.
action = mari.actions.create(
    "Create Directories Move Files", "mari.jtools.createDirectoriesMoveFiles()"
    )
mari.menus.addAction(action, "MainWindow/&Tools")
icon_filename = "DuplicateChannel.png"
icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
action.setIconPath(icon_path) 