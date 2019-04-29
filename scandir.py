import os
from distutils.extension import Extension


# scan the 'dvedit' directory for extension files, converting
# them to extension names in dotted notation
def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path):
            if path.endswith(".pyx"):
               pathName =path.replace(os.path.sep, ".")[6:-4]
            elif path.endswith(".py"):
               pathName = path.replace(os.path.sep, ".")[6:-3]
            else:
                continue
            files.append ((path, pathName))   
        elif os.path.isdir(path):
            scandir(path, files)
    return files

libdvIncludeDir = "/home/lozinski/code/cromlech/wiki/src/zopache/src/zopache"
# generate an Extension object from its dotted name
def makeExtension(names):
    extPath = names [0]
    extName = names [1]
    #print (extName, extPath)
    return Extension(
        extName,
        [extPath],
        include_dirs = [libdvIncludeDir, "."],   # adding the '.' to include_dirs is CRUCIAL!!
        extra_compile_args = ["-O3", "-Wall"],
        extra_link_args = ['-g'],
        libraries = ["zopache",],
        )

# get the list of extensions
extNames = scandir("./src")
extensions = [makeExtension(name) for name in extNames]



#for item in extNames:
#    print (item)
