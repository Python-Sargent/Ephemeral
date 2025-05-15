# python 3.13
#
# Ephemeral Version
# 

class __Version__:
    def __init__(self, major, minor, patch, minor_patch = None):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.version = str(major) + "." + str(minor) + "." + str(patch)
        if minor_patch != None:
            self.version += str(minor_patch)

class Version:
    Version = __Version__(0, 1, 0) # Game version
    ServerVersion = __Version__(0, 1, 0, 1)
    ClientVersion = __Version__(0, 1, 0, 1)