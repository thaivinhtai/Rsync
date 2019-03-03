#!/usr/bin/env python3
import argparse
from os import (path, open, read, write, sendfile, lseek, O_RDWR,
                mkdir, stat, O_RDONLY, symlink, link, readlink,
                scandir, unlink, utime, chmod, fdopen)


def full_path(file):
    """
    This funtion return full path of any file
    """
    file_path = str(file)
    if file_path[0] == '~':
        file_path = path.expanduser(file_path)
    else:
        file_path = path.realpath(file_path)
    return file_path


def read_file(file):
    """
    Get contain of a file
    """
    file = full_path(file)
    file = open(file, O_RDWR)
    file = fdopen(file)
    content = file.read()
    file.close()
    return content


def write_file(file):
    return 0


def file_size(file):
    """
    Reuturn size of file in byte
    """
    file = full_path(file)
    return stat(file).st_size


def file_mod_time(file):
    """
    Return most recent mod time of file
    """
    file = full_path(file)
    return stat(file).st_mtime


def introduction(file="introduction.md"):
    """
    Just making fake-rsync as same as the real one when there's no argument :D
    This is an introduction of fake-rsync
    """
    return read_file(file)


class Get_args():
    """
    This class uses argparse for get args and do some stuffs with them to get
    data for progressing.
    """

    PARSER = argparse.ArgumentParser(description=introduction("quick_intro"))
    PARSER.add_argument('source_files', nargs='*',
                        help="""the file or directory (or a list of multiple
                                files and directories) to copy from.""")
    PARSER.add_argument('destination_file', nargs='?',
                        help="""the file or directory to copy to, and square
                                brackets indicate optional parameters.""")
    PARSER.add_argument('-c', '--checksum',
                        action='store_true', default=False,
                        help='skip based on checksum, not mod-time & size')
    PARSER.add_argument('-r', '--recursive',
                        action='store_true', default=False,
                        help='recurse into directories')
    PARSER.add_argument('-u', '--update',
                        action='store_true', default=False,
                        help='skip files that are newer on the receiver')
    PARSER.add_argument('-H', '--hard_links',
                        action='store_true', default=True,
                        help='preserve hard links')
    PARSER.add_argument('-l', '--links',
                        action='store_true', default=True,
                        help='copy symlinks as symlinks')
    PARSER.add_argument('-alg', '--algorithm',
                        help='algorithm will be used', default="LCS")
    ARGS = PARSER.parse_args()

    def __init__(self):
        self.source_files = self.ARGS.source_files
        # list of files which does not exist
        self.invalid_files = self.invalid_source_files(self.source_files)
        self.dest_file = self.ARGS.destination_file  # destination file
        if len(self.ARGS.source_files) >= 2:
            self.dest_file = self.ARGS.source_files[-1]
            self.source_files.remove(self.dest_file)
        self.u_option = self.ARGS.update
        self.c_option = self.ARGS.checksum
        self.H_option = self.ARGS.hard_links
        self.l_option = self.ARGS.links
        self.r_option = self.ARGS.recursive
        # dictionary of [1]INODE and list of files have same INODE
        self.hardlink_files = self.which_files_hardlink(self.source_files)

    def check_path_file_type(self, file):
        """
        Check if the path is file, directory, symlink
        """
        file_path = full_path(file)
        if path.isfile(file_path):
            return "file"
        if path.isdir(file_path):
            return "directory"
        if path.islink(file_path):
            return "symlink"
        return 0

    def invalid_source_files(self, list_files):
        """
        Check if the source files are not exist and group them into a list
        """
        invalid_files = []
        if len(list_files) > 0:
            invalid_files = [file for file in list_files
                             if self.check_path_file_type(file) == 0]
        return invalid_files

    def which_files_hardlink(self, list_files):
        """
        Group files have same INODE together in a dictionary,
        which INODE is key and value is list of files.
        """
        groups_of_hardlinks = {}
        for file in list_files:
            if file not in self.invalid_files:
                Inode = stat(file)
                if Inode.st_ino not in groups_of_hardlinks.keys():
                    groups_of_hardlinks[Inode.st_ino] = []
                groups_of_hardlinks[Inode.st_ino].append(file)
        return groups_of_hardlinks


def lcs(content1, content2):
    """
    Solution to the Longest Common Subsequence problem.
    """
    # find the length of the strings
    len1 = len(content1)
    len2 = len(content2)
    # declaring the array for storing the dp values
    L = [[None]*(len2 + 1) for i in range(len1 + 1)]
    """
    Following steps build L[len1 + 1][len2 + 1] in bottom up fashion
    Note: L[i][j] contains length of LCS of content1[0..i-1]
    and content2[0..j-1]
    """
    for i in range(len1 + 1):
        for j in range(len2 + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif content1[i-1] == content2[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    """
    L[len1][len2] contains the length of LCS
    of content1[0..len2-1] & content2[0..len1-1]
    """
    return L[len1][len2]


def are_they_same(file1, file2, checksum=False):
    """
    compare 2 files in normal case or -c case
    """
    if file_size(file1) != file_size(file2):
        return False
    if checksum:
        return 0
    else:
        if file_mod_time(file1) != file_mod_time(file2):
            return False
    return True


def main():
    """
    Main funtion
    """
    argv = Get_args()
    if (len(argv.source_files) == 0):
        print(introduction())
        return 0
    print(argv.source_files)
    print(argv.invalid_files)
    print(argv.dest_file)
    print(argv.hardlink_files)
    print(lcs("ABCD", "BCAD"))
    print(file_size(argv.dest_file))


if __name__ == "__main__":
    main()
