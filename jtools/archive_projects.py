# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Batch archiving script for Mari projects through command line
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

import zipfile, sys, getopt, os

version = "0.02"

cache_path = ''
archive_path = ''
num_files = 0
copied = 10
num_proj = 0
projects = []

# ------------------------------------------------------------------------------ 
def archive(argv):
    "archive projects"
    global num_files, copied, num_proj, projects
    
    if not _checkArgs(argv):
        return False

    dir_list = os.listdir(cache_path)
        
    for dir in dir_list:
        if "-" in dir and len(dir) == 36:
            projects.append(dir)
            
    if len(projects) == 0:
        print "\nNo projects found\n"
        return False
        
    print ""
        
    for project in projects:
        num_proj += 1
        copied = 10
        cache_proj_path = os.path.join(cache_path, project)
        files_folders = os.listdir(cache_proj_path)
        all = list(files_folders)
        for item in files_folders:
            if not os.path.isfile(os.path.join(cache_proj_path, item)):
                all.extend(os.listdir(os.path.join(cache_proj_path, item)))
        num_files = len(all)
        archive_proj_path = os.path.join(archive_path, project)
        zip = zipfile.ZipFile(archive_proj_path + '.mra', 'w', allowZip64=True)
        _zipdir(os.path.join(cache_path, project), zip)
        print ""
            
# ------------------------------------------------------------------------------ 
def _zipdir(path, zip):
    "Zip files and folders"
    for root, subdirs, files in os.walk(path):
        for file in files:
            absfile = os.path.join(root, file)
            relfile = absfile[len(root)+len(os.sep):]
            zip.write(absfile, relfile)
            _progress()

# ------------------------------------------------------------------------------                 
def _progress():
    "progress"
    global copied
    copied += 1
    prog = int(copied * 100 / num_files)
    print "%d%% of project %d/%d archived                   \r" %(prog, num_proj, len(projects)),
    
# ------------------------------------------------------------------------------             
def _checkArgs(argv):
    "Check arguments and paths given"
    global cache_path, archive_path
    
    if len(argv) == 0 or len(argv) == 3 or len(argv) > 4:
        print '\n' + 'archive_projects.py -c <cache_path> -a <archive_path>'
        return False
    else:
        try:
            opts, args = getopt.getopt(argv,"hc:a:",["cpath=","apath="])
        except getopt.GetoptError:
            print '\n' + 'archive_projects.py -c <cache_path> -a <archive_path>'
            return False
        for opt, arg in opts:
            if opt == "-h" and len(argv) == 1:
                print '\n' + 'archive_projects.py -c <cache_path> -a <archive_path>'
            elif opt in ("-c", "--cpath") and _checkFlags(opts):
                cache_path = arg
            elif opt in ("-a", "--apath") and _checkFlags(opts):
                archive_path = arg
            else:
                print '\n' + 'archive_projects.py -c <cache_path> -a <archive_path>'
                return False
        
        cache_path = os.path.abspath(cache_path)
        archive_path = os.path.abspath(archive_path)
        
        if not os.path.isdir(cache_path) and not os.path.isdir(archive_path):
            print '\n' + 'Cache and archive path do not exist: -c %s -a %s' %(cache_path, archive_path)
            return False
        elif os.path.isdir(cache_path) and not os.path.isdir(archive_path):
            print '\n' + 'Archive path does not exist: ', archive_path
            return False
        elif os.path.isdir(archive_path) and not os.path.isdir(cache_path):
            print '\n' + 'Cache path does not exist: ', cache_path
            return False
        else:
            return True
            
# ------------------------------------------------------------------------------         
def _checkFlags(opts):
    for opt in opts:
        if "-h" in opt:
            return False
        else:
            return True
            
# ------------------------------------------------------------------------------ 
if __name__ == "__main__":
   archive(sys.argv[1:])