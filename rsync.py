#!/usr/bin/env python3
import argparse
import difflib
from os import (path, open, read, write, sendfile, lseek,
                mkdir, stat, O_RDONLY, symlink, link, readlink,
                scandir, unlink, utime, chmod, fdopen)


def introduction():
    """
    Just making fake-rsync as same as the real one when there's no argument :D
    This is an introduction of fake-rsync
    """
    file_descriptors = open("introduction.md", O_RDONLY)
    introduction_file = fdopen(file_descriptors)
    return introduction_file.read()


class Get_args():
    """
    This class uses argparse for get args and do some stuffs with them to get
    data for progressing.
    """

    PARSER = argparse.ArgumentParser(description=introduction())
    PARSER.add_argument('source_files', nargs='*')
    PARSER.add_argument('destination_file', nargs='?')
    # PARSER.add_argument('-h', '--help',
    #                      action='store_true')
    PARSER.add_argument('-u', '--update',
                        action='store_true', default=False,
                        help='skip files that are newer on the receiver')
    PARSER.add_argument('-c', '--checksum',
                        action='store_true', default=False,
                        help='skip based on checksum, not mod-time & size')
    PARSER.add_argument('-H', '--hard_links',
                        action='store_true', default=True,
                        help='preserve hard links')
    PARSER.add_argument('-l', '--links',
                        action='store_true', default=True,
                        help='copy symlinks as symlinks')
    ARGS = PARSER.parse_args()

    def __init__(self):
        self.source_files = self.ARGS.source_files
        self.invalid_files = self.invalid_source_files(self.source_files)
        self.dest_file = self.ARGS.destination_file
        # self.h_option = self.ARGS.help
        self.u_option = self.ARGS.update
        self.c_option = self.ARGS.checksum
        self.H_option = self.ARGS.hard_links
        self.l_option = self.ARGS.links
        self.hardlink_files = dict()

    def check_path_file_type(self, path_file):
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
        return 0

    def invalid_source_files(self, list_files):
        """
        Check if the source files are not exist and group them into a list
        """
        invalid_files = []
        if len(list_files) > 0:
            # for file in self.source_files:
            #     if self.check_path_file_type(file) == 0:
            #         invalid_files.append(file)
            invalid_files = [file for file in list_files
                             if self.check_path_file_type(file) == 0]
        return invalid_files

    def which_files_hardlink(self, list_files):
        """
        Group files have same INODE together in a dictionary,
        which INODE is key and value is list of files.
        """
        groups_of_hardlinks = {}


def main():
    """
    Main funtion
    """
    argv = Get_args()
    if (len(argv.source_files) == 0) or (argv.help):
        print(introduction())
        return 0
    print("Fail")


if __name__ == "__main__":
    main()
