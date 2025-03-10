import sys, shutil, os ,re , pprint
print=pprint.pp
srcdir="/home/martin/.kodi/addons/plugin.video.StreamFreedom/resources/patchfiles/"
print(srcdir)


def list_files(filepath):
    paths = []
    for path, dirs, files in os.walk(filepath):
        for file in files:
            fp=os.path.join(path, file)
            if os.path.isfile(fp):
                paths.append(fp)
    return(paths)


addons={}
for addon in os.listdir(srcdir):
    if addon == "plugin.video.xxx-o-dus":
        addonroot=os.path.join(srcdir, addon)
        if os.path.isdir(addonroot):
            addons[addon]=list_files(addonroot)

# print(addons)
for name in addons:
    print(name)
    for path in addons[name]:
        print(path)#.split("/plugin.video.StreamFreedom/resources/patchfiles/")[1]))
        print(os.path.join("/home/martin/.kodi/addons/",path.split("/plugin.video.StreamFreedom/resources/patchfiles/")[1]))



print ("done")