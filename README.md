# repository.StreamFreedom

## And a patching system for StreamArmy addons

### And just one (for now) adult-content kodi addon

StreamFreedom Patcher can remove the pinsystem requirements and other malicious
code from StreamArmy repo addons.

Wich includes the nemzzy service (script.module.nemzzy) is a script that is part of the 
StreamArmy addons and is run as a service inside Kodi.
This script installs and loads a windows dll or android .so - ( possibly admaven ) 
https://www.ad-maven.com

These files function is not known at this time.

The service will run at Kodi's start and then again every time one of the StreamArmy Addons is used.
Every time it is run it checks if the dll or .so file is installed, or needs updating then it 
runs the library and attaches it to the Kodi Process

The suspicious dlls and libraries are contained in nemzzy's addon and available for your inspection here
https://github.com/nemesis668/repository.streamarmy18-19/tree/main/script.module.nemzzy/lib

The original addon script source for script.module.nemzzy can be inspected here:
https://github.com/nemesis668/repository.streamarmy18-19/tree/main/script.module.nemzzy
The key files are obfuscated however.

StreamFreedom Patcher can deobfuscate the obfuscated python files in all the StreamArmy addons
and patch the files to remove:
```
1    calls to the nemzzy service (script.module.nemzzy) 
2    calls to the pin check system - no more annoying popups asking yoou to look at
        advertising on https://pinsystem.co.uk/

3    all StreamArmy addon requirements the script.module.nemzzy in addon.xml by removing the line
            <import addon="script.module.nemzzy" />
        from each addons addon.xml file
        NOTE: I may revert to not changing the import line if it turns out any modules
        are calling the nemzzy() function, because they will raise an exception when python 
        cant find the function - I may do it anyway :)
         
4    stop the nemzyy service code ever running by making a minor change to the entry point
        in neupop.py :
                    def nemzzy():
                        return #without executing any code # StreamFreedom patch
        This is an axample of the method used to remove the pin system calls also
        The patcher also changes script.module.nemzzy/addon.xml, changing.... 
              <extension point="xbmc.service" library="neupop.py" start="startup">
        to 
              <extension point="xbmc.service" library="main.py" >
              main.py is a python file containing no code, so nothing happens, its a no-op
```
Deobfuscated files have been modified where neccessary to disable the pin system 
and any calls to the nemzzy service script 

Deobfuscated files will contain the following comment at the top 

\# Deobfuscated by StreamFreedom

Changes to files will be commented with

\# StreamFreedom patch

near the location of changes

NOTE:
    At the time of writing I had spent several hours on a windows virtual machine
    figuring out what is happening inside the nemzzy service script
    I have not conclusively determined what the dll does nor managed to intercept 
    any internet traffic initiated by the dll.
    What I do know is that the dll's are started by the service, attached to the Kodi 
    process and then terminated when Kodi closes.


The XXX-O-DUS plugin has some code added to override some menu options.
The new menu has some additional functionality and improved version information.
There is a cache clean function that for now, only clears the thumbcache but will 
do more, in the fullness of time. 

Enjoy!



