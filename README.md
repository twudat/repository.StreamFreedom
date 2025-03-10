# repository.StreamFreedom

A collection of Kodi Addons

Mostly adult content related

Includes the StreamFreedom Patcher for removing pinsystem requirements and malicious
code from StreamArmy repo addons.

The StreamFreedom Patcher can disable the nemzzy service which will infect your windows
or android system with admaven dll's, or libraries (https://ad-maven.com/) 
which is not in the spriit of open source or Kodi addons

It is likeley illegal to do so without your permission and without warning.

The original addon script source for script.module.nemzzy can be inspected here:
https://github.com/nemesis668/repository.streamarmy18-19/tree/main/script.module.nemzzy
The key files are obfiscated however.

The patcher contains the unmodified deobfiscated files. It simply replaces the call to
the service python file to main.py which contains a single variable assignement that 
is never used.
In practice the file is a no-op

The import line in all the StreamArmy addons.xml files 	<import addon="script.module.nemzzy" />
has also been removed, therbey removing the dependancy.

The StreamFreedom Patcher also de-obfiscates python code contained in the Streamarmy
addons leaving the original files intact but renamed to <filename>_py.obf for your perusal.

The-deobfiscated files have been modified where neccessarye to disable the pin system 
and any calls to the nemzzy script

Deobfiscated files will contain the following comment at the top 

#  # Deobfuscated by StreamFreedom

Changes to files will be commented with
#  # StreamFreedom patch
near the location of changes


The XXX-O-DUS plugin has code added to override some menu options.
The new menu has some additional functionality and improved version information.

Enjoy!



