import os

def check_file_exists(filename):
    """Check to see if file exists, if not raise IOError."""
    if not os.path.isfile(filename):
        raise IOError('File %s does not exist' % filename)


def check_dir_exists(directory):
    """Check to see if directory exists, if not raise IOError."""
    if not os.path.isdir(directory):
        raise IOError('Directory %s does not exist' % directory)


def check_create_dir(directory, info=False):
    """Check to see if directory exists, if not make it.

    Can optionally display message to user.
    """
    if not os.path.isdir(directory):
        if os.path.isfile(directory):
            raise RuntimeError("Cannot create directory %s, already "
                               "exists as a file object" % directory)
        os.makedirs(directory)
        if info:
            print "Making dir %s" % directory
