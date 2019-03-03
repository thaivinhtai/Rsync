#!/usr/bin/env python3
import argparse
import hashlib
from os import (path, open, read, write, sendfile, lseek, O_RDWR, O_CREAT,
                mkdir, stat, O_RDONLY, symlink, link, readlink, close,
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


def create_text_file(name, content):
    """
    Create a text file if it's not exist
    """
    file_descriptor = open(name, O_RDWR | O_CREAT)
    byte_object = str.encode(content)
    ret = write(file_descriptor, byte_object)
    close(file_descriptor)
    return 0


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
    try:
        return stat(file).st_size
    except FileNotFoundError:
        return 0


def file_mod_time(file):
    """
    Return most recent mod time of file
    """
    file = full_path(file)
    return stat(file).st_mtime


def file_access_time(file):
    """
    Return file's access time
    """
    file = full_path(file)
    return stat(file).st_atime


def file_mode(file):
    """
    return protection bits
    """
    file = full_path(file)
    return stat(file).st_mode


def hash_md5(file):
    """
    Return hash value of a file's content
    """
    return hashlib.md5(read_file(file).encode("utf-8")).hexdigest()


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
        self.dest_file = self.ARGS.destination_file  # destination file
        if len(self.ARGS.source_files) >= 2:
            self.dest_file = self.ARGS.source_files[-1]
            self.source_files.remove(self.dest_file)
        self.invalid_files = self.invalid_source_files(self.source_files)
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
        try:
            file_path = full_path(file)
            if path.isfile(file_path):
                return "file"
            if path.isdir(file_path):
                return "directory"
            if path.islink(file_path):
                return "symlink"
            return 0
        except FileNotFoundError:
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
        if hash_md5(file1) != hash_md5(file2):
            return False
        return True
    else:
        if file_mod_time(file1) != file_mod_time(file2):
            return False
    return True


def main():
    """
    Main funtion
    """
    error = 0
    argv = Get_args()
    # if there is no argument, print introduction
    if (len(argv.source_files) == 0):
        print(introduction())
        return 0
    # if there are invalid files, print error
    if len(argv.invalid_files) > 0:
        for file in argv.invalid_files:
            file = full_path(file)
            print("rsync: link_stat \"%s\" failed: " % file +
                  "No such file or directory (2)")
        error = error + 1
    # if destination file is not a directory or has not eisted, print error
    if (len(argv.source_files) >= 2):
        if (argv.check_path_file_type(argv.dest_file) not in ["directory", 0]):
            print("rsync error: errors selecting input/output files, " +
                  """dirs (code 3) at main.c(640)
 [Receiver=3.1.1]""")
        error = error + 1
    # there is one of above errors, exit.
    if error > 0:
        return 0
    # one source file and one destination file
    if len(argv.source_files) == 1 and argv.dest_file != "":
        if are_they_same(argv.source_files[0], argv.dest_file, argv.c_option):
            return 0
        else:
            if argv.check_path_file_type(argv.source_files[0]) == "directory":
                print("skipping directory " + argv.source_files[0])
                return 0
            elif argv.check_path_file_type(argv.source_files[0]) == "file":
                if argv.check_path_file_type(argv.dest_file) == 0:
                    create_text_file(argv.dest_file,
                                     read_file(argv.source_files[0]))
                    utime(full_path(argv.dest_file),
                          (file_access_time(argv.source_files[0]),
                           file_mod_time(argv.source_files[0])))
                    chmod(full_path(argv.dest_file),
                          file_mode(argv.source_files[0]))
                elif argv.check_path_file_type(argv.dest_file) == "file":
                    len_source_file = len(read_file(argv.source_files[0]))
                    len_dest_file = len(read_file(argv.dest_file))
                    if


if __name__ == "__main__":
    main()
