# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Batch extracting script for Mari projects through command line
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

import zipfile, sys, getopt, os, uuid, re

version = "0.01"

cache_path = ''
archive_path = ''
num_proj = 0
projects = []

# ------------------------------------------------------------------------------ 
def extract(argv):
    "archive projects"
    global num_files, copied, num_proj, projects
    
    if not _checkArgs(argv):
        return False
        
    dir_list = os.listdir(archive_path)

    for dir in dir_list:
        if ".mra" in dir and len(dir) > 36:
            projects.append(dir)
        
    if len(projects) == 0:
        print "\nNo projects found\n"
        return False
        
    print ""

    for project in projects:
        num_proj += 1
        uuid4 = str(uuid.uuid4())
        zip_path = os.path.join(archive_path, project)
        zip_file = zipfile.ZipFile(zip_path)
        extract_path = os.path.join(cache_path, uuid4)
        _extract(zip_file, extract_path, uuid4)
        print ""

# ------------------------------------------------------------------------------             
def _extract(zip_file, extract_path, uuid4):
    "Extract files and folders"
    num_files = len(zip_file.namelist())
    extracted_files = 0

    for file in zip_file.namelist():
        if file == "Summary.txt":
            zip_file.extract(file, extract_path)
            with open(os.path.join(extract_path, file), 'r+') as summary:
                lines = summary.readlines()
                summary.seek(0)
                summary.truncate()
                for line in lines:
                    if 'Uuid' in line:
                        line = re.sub(r'Uuid=.+', r'Uuid=%s' %uuid4, line)
                    summary.write(line)
        elif file == 'Project.mri' and not file == 'Project.mri.bak':
            zip_file.extract(file, extract_path)
            orig_zip = zipfile.ZipFile(os.path.join(extract_path, file), 'r')
            lines = []
            with open('Project.mri', 'w') as project:
                for filename in orig_zip.namelist():
                    for line in orig_zip.read(filename).split("\n"):
                        if 'uuid Type' in line:
                            line = re.sub(r'<uuid Type=.+', r'<uuid Type="QString">%s</uuid>' %(uuid4), line)
                        project.write("%s\n" %line)
            orig_zip.close()
            os.remove(os.path.join(extract_path, file))
            new_zip = zipfile.ZipFile(os.path.join(extract_path, file), 'w')
            new_zip.write('Project.mri')
            new_zip.close()
        else:
            zip_file.extract(file, extract_path)
        extracted_files += 1
        print "%d%% of project %d/%d extracted                   \r" % (extracted_files * 100/num_files, num_proj, len(projects)),

# ------------------------------------------------------------------------------             
def _checkArgs(argv):
    "Check arguments and paths given"
    global cache_path, archive_path
    
    if len(argv) == 0 or len(argv) == 3 or len(argv) > 4:
        print '\n' + 'extract_projects.py -a <archive_path> -c <cache_path>'
        return False
    else:
        try:
            opts, args = getopt.getopt(argv,"ha:c:",["apath=","cpath="])
        except getopt.GetoptError:
            print '\n' + 'extract_projects.py -a <archive_path> -c <cache_path>'
            return False
        for opt, arg in opts:
            if opt == "-h" and len(argv) == 1:
                print '\n' + 'extract_projects.py -a <archive_path> -c <cache_path>'
            elif opt in ("-a", "--apath") and _checkFlags(opts):
                archive_path = arg
            elif opt in ("-c", "--cpath") and _checkFlags(opts):
                cache_path = arg                
            else:
                print '\n' + 'extract_projects.py -a <archive_path> -c <cache_path>'
                return False
        
        cache_path = os.path.abspath(cache_path)
        archive_path = os.path.abspath(archive_path)
        
        if not os.path.isdir(cache_path) and not os.path.isdir(archive_path):
            print '\n' + 'Archive and cache path do not exist: -a %s -c %s' %(archive_path, cache_path)
            return False
        elif os.path.isdir(archive_path) and not os.path.isdir(cache_path):
            print '\n' + 'Cache path does not exist: ', cache_path
            return False
        elif os.path.isdir(cache_path) and not os.path.isdir(archive_path):
            print '\n' + 'Archive path does not exist: ', archive_path
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
   extract(sys.argv[1:])