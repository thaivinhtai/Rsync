#!/usr/bin/env python3
import argparse
import difflib
from os import (path, open, read, write, sendfile, lseek, mkdir, stat, O_RDONLY,
                symlink, link, readlink, scandir, unlink, utime, chmod, fdopen)
from sys import argv


def introduction():
    """
    Just making fake-rsync as same as the real one when there's no argument :D
    This is an introduction of fake-rsync
    """
    file_descriptors = open("introduction.md", O_RDONLY)
    introduction_file = fdopen(file_descriptors)
    return introduction_file.read()


def check_path_file_type(path_file):
    """
    Check if the path is file, directory, symlink
    """
    full_path = str(path_file)
    if full_path[0] == '~':
        full_path = path.expanduser(full_path)
    else:
        full_path = path.realpath(full_path)
    if path.isfile(full_path):
        return "file"
    if path.isdir(full_path):
        return "directory"
    if path.islink(full_path):
        return "symlink"


def which_files_hardlink(*args):
    """

    """


def main():
    """
    Main funtion
    """
    if (len(argv) == 1) or ('-h' in argv) or ('--help' in argv):
        print(introduction())
        return 0
    print("hello " + argv[1])


if __name__ == "__main__":
    main()
# import argparse
#
# parser = argparse.ArgumentParser(description="Example for store true & false")
# parser.add_argument("--set-false", "--s", "--sf", help="Set var_name to false", dest="var_name", action="store_false")
# parser.set_defaults(var_name=True)
#
# args = parser.parse_args()
#
# print ("var_name is %s" % args.var_name)
