fake-rsync  version 6.9.6.9  protocol version 69
NoCopyright (nC) 2019 by Tai.
Web site: None
Capabilities:
    64-bit files, 64-bit inums, 64-bit timestamps, 64-bit long ints,
    hardlinks, symlinks, batchfiles, inplace,
    append, ACLs, xattrs, iconv, symtimes, prealloc

fake-rsync comes with ABSOLUTELY NO WARRANTY.  This is free software, and you
are welcome to redistribute it under certain conditions.  See the GNU
General Public Licence for details.

rsync is a file transfer program capable of efficient remote update
via a fast differencing algorithm.

Usage: rsync [OPTION]... SRC [SRC]... DEST

The ':' usages connect via remote shell, while '::' & 'rsync://' usages connect
to an rsync daemon, and require SRC or DEST to start with a module name.

Options
 -c, --checksum              skip based on checksum, not mod-time & size
 -r, --recursive             recurse into directories
 -u, --update                skip files that are newer on the receiver
(-h) --help                  show this help (-h is --help only if used alone)
