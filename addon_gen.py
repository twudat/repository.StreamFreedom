#!/usr/bin/env python2.7
# *
# *  Copyright (C) 2012-2013 Garrett Brown
# *  Copyright (C) 2010      j48antialias
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# *  Based on code by j48antialias:
# *  https://anarchintosh-projects.googlecode.com/files/addons_xml_generator.py

""" addons.xml generator """

import os
import sys
import zipfile
import re
import time
import shutil
import xml.etree.ElementTree as ET

KODI_VERSIONS = ["krypton", "leia", "matrix", "nexus", "omega" , "addons", 'repo']

# Compatibility with 3.0, 3.1 and 3.2 not supporting u"" literals
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """
    # we're gonna return this so there's only be traversal of known good folders\
    addons=[]
    def get_addons(self ):
        return self.addons

    def dump(self):
        for i in self.addons:
            print(i)

    def __init__( self ):
        # we're gonna return this so there's only be traversal of known good folders\
        self.addons=[]
        self.startdir=os.getcwd()
        # generate files
        self._generate_addons_file()
        self._generate_md5_file()
        # notify user
        print("Finished updating addons xml and md5 files")


    def _generate_addons_file( self ):
        # addon list
        # addons = os.listdir( "." )
        ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        # print(ROOT_DIR)
        # sys.exit()
        cwd=os.getcwd()
        for release in KODI_VERSIONS :
            aodir=os.path.join(cwd,release)
            # print(aodir)
            if os.path.isdir(aodir):
                # print(aodir)
                for ao in os.listdir(aodir):
                    addon=os.path.join(aodir,ao)
                    # print("addon=%s  ao=%s" %(addon, ao))
                    if ( not os.path.isdir( addon ) or ao == ".svn" or ao == ".git" or ao == "zips"): continue
                    self.addons.append(addon)
                    # print(addon)



        # final addons text
        addons_xml = u("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n")
        # loop thru and add each addons addon.xml file
        for addon in self.addons:
            try:
                # skip any file or .svn folder or .git folder
                # we have no pre-prepares a list of folders to parse
                # if ( not os.path.isdir( addon ) or addon == ".svn" or addon == ".git" ): continue
                # create path
                _path = os.path.join( addon, "addon.xml" )
                # generate md5 for all the smaller xml files
                self._generate_md5_file(_path)
                # split lines for stripping
                xml_lines = open( _path, "r" ).read().splitlines()
                # new addon
                addon_xml = ""
                # loop thru cleaning each line
                for line in xml_lines:
                    # skip encoding format line
                    if ( line.find( "<?xml" ) >= 0 ): continue
                    # add line
                    if sys.version < '3':
                        addon_xml += unicode( line.rstrip() + "\n", "UTF-8" )
                    else:
                        addon_xml += line.rstrip() + "\n"
                # we succeeded so add to our final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
            except Exception as e:
                # missing or poorly formatted addon.xml
                print("%s Excluding %s " % ( e,  _path ))
        # clean and add closing tag
        addons_xml = addons_xml.strip() + u("\n</addons>\n")
        # save file
        self._save_file( addons_xml.encode( "UTF-8" ), file="addons.xml" )

    def _generate_md5_file( self , addonxmlpath=None ):
        if addonxmlpath:
            addonxmlfile=addonxmlpath
        else:
            addonxmlfile=os.path.join(self.startdir,"addons.xml")
        # create a new md5 hash
        try:
            import md5
            m = md5.new( open( addonxmlfile, "r" ).read() ).hexdigest()
        except ImportError:
            import hashlib
            m = hashlib.md5( open( addonxmlfile, "r", encoding="UTF-8" ).read().encode( "UTF-8" ) ).hexdigest()

        # save file
        try:
            self._save_file( m.encode( "UTF-8" ), file="%s.md5" % addonxmlfile )
        except Exception as e:
            # oops
            print("%s - An error occurred creating addons.xml.md5 file!\n" % e)

    def _save_file( self, data, file ):
        try:
            # write data to the file (use b for Python 3)
            open( file, "wb" ).write( data )
        except Exception as e:
            # oops
            print("%s - An error occurred saving %s file!\n" % ( e,file ))




def zipfolder(source_dir, target_file , verbose=False):
    zipobj = zipfile.ZipFile(target_file, 'w', zipfile.ZIP_DEFLATED)

    folder = os.path.abspath(source_dir) # make sure folder is absolute

    folder_base=os.path.basename(folder.strip(os.path.sep))

    # print("folder base = %s" % folder_base)

    # Walk the entire folder tree and compress the files in each folder.
    for foldername, subfolders, filenames in os.walk(source_dir):

        if foldername == folder:
             archive_folder_name = folder_base  #''
        else:
             archive_folder_name = os.path.relpath(foldername, folder)
             archive_folder_name=os.path.join(folder_base,archive_folder_name)
             # ignore fuse (ntfs) folder and .git folders
             if re.search(".fuse_hidden", filename): continue
             if not ".git" in foldername and not "zips" in foldername:
                 # Add the current folder to the ZIP file.
                 # print("storing %s" % archive_folder_name)
                 zipobj.write(foldername, arcname=archive_folder_name)

        # Add all the files in this folder to the ZIP file.
        for filename in filenames:
            if re.search(".fuse_hidden", filename): continue
            if not ".git" in foldername and not "zips" in foldername:
                if verbose:
                    print("storing %s" % os.path.join(archive_folder_name, filename))
                zipobj.write(os.path.join(foldername, filename), arcname=os.path.join(archive_folder_name, filename))
    zipobj.close()

if ( __name__ == "__main__" ):
    # start
    gen=Generator()
    #rezip files an move
    print ('Removing all pyo and pyc files from addons...')
    cwd=os.getcwd()
    zipsfolder = os.path.join(cwd,'zips')
    if not os.path.exists(zipsfolder):
        os.mkdir(zipsfolder)
        # print ('Directory doesn\'t exist, creating: ' + zipsfolder)

    #remove all pyo file from addons.
    for root, dirs, files in os.walk(cwd):
        # rem_folder = ['_MACOSX','zips']
        rem_folder = ['_MACOSX']
        rem_files  = ['.pyo','DS_Store', '.pyc']
        for f in files:
            try:
                if any(x in f for x in rem_files):
                    os.unlink(os.path.join(root, f))
                    print ('Removing: ' + os.path.join(root, f))
                else: continue
            except: pass
        for d in dirs:
            try:
                if any(x in d for x in rem_folder):
                    shutil.rmtree(os.path.join(root, d))
                    print ('Removing: ' + os.path.join(root, d))
                else: continue
            except: pass

    print ('Starting zip file creation...')
    filesinrootdir = os.listdir(cwd)
    for foldertozip in gen.get_addons():
        version="unknown"
        print('folder to zip =' , foldertozip)
        zipfilenamefirstpart,zipfilenamelastpart = os.path.split(foldertozip)
        addon_path=os.path.basename(foldertozip.strip())
        ziptarget=os.path.join(zipsfolder,addon_path)


        #check if and move changelog, fanart and icon to zipdir
        filesinfoldertozip = os.listdir(foldertozip)
        for filetozip in filesinfoldertozip:
            if filetozip == "zips" : continue

            sourcefile=os.path.join(foldertozip,filetozip)
            print ('processing file: ' + sourcefile)

            if re.search("addon.xml", filetozip) and not re.search("addon.xml.md5", filetozip) : # get version number of plugin
                try:
                    tree = ET.parse(sourcefile)
                except:
                    print("Exception about to be raised...")
                    print("file is %s" % sourcefile)
                    print("Element Tree lookes like this ...")
                    print(ET.dump(tree))
                    raise
                root = tree.getroot()
                for elem in root.iter('addon'):
                    # print (elem.tag + ': ' + elem.attrib['version'])
                    version = elem.attrib['version']
                continue

            zipfilename = os.path.join(ziptarget,zipfilenamelastpart + "-" + version + '.zip')


        #  we want to recreate zips when version doesnt change but when the addon.xml changes
        # have to write some code to do the md5 check and the skip this bit its unchanged
        if os.path.isfile(zipfilename):
            os.unlink(zipfilename)

        # make sure the zip/addon-name/   structure exists
        if not os.path.exists(ziptarget):
            os.mkdir(ziptarget)

        if not os.path.isfile(zipfilename):  # only do it on new changes/versions
            print (' zipping file: ' + zipfilename)
            zipfolder(foldertozip, zipfilename , False ) #git hell if it re-zips the samething each time


            #this bit is for my repo structure - it wont work for yours
            if re.search("repository", foldertozip):
                publicrepo=os.path.join(cwd,"..", "twudat.github.io",os.path.basename(zipfilename))
                publicrepo=os.path.abspath(publicrepo)
                # print (publicrepo)
                shutil.copyfile(zipfilename,publicrepo)
        else:
            print (' skip zipping file: ' + zipfilename)
