#!/usr/bin/env python3
'''
Parses the fstab file and for each cifs mount point creates
a monitor block for monit

Instead of configuring monit to send an email on failure,
a script will be created to log failures in /var/log/monit.log

At a set time interval, a service will check for errors in
the output of the 'monit summary' command and if an error is encountered,
an email will be sent

The parser can be done with the command below:
sudo monit summary | awk '{if(NR>2)print}' | grep -v 'OK'

An example log is on the machine srvexa02vm01
'''

import re


MONIT_TEMPLATE = '''
check filesystem $rootfs path $fs_file
        start program = "/bin/mount $fs_spec" timeout 5 seconds
        stop program = "/bin/umount $fs_spec" with timeout 5 seconds
        if does not exist for 3 cycles then restart
        if does not exist for 3 cycles then exec /usr/local/bin/log_monit_event
'''


'''
Module Constants
'''
FS_SPEC = 'fs_spec'
FS_FILE = 'fs_file'
FS_VFSTYPE = 'fs_vfstype'
FS_MNTOPS = 'fs_mntops'
FS_FREQ = 'fs_freq'
FS_PASSNO = 'fs_passno'


'''
A valid line in the fstab file can start with zero or more spaces and tabs
The six fields are required and must be separated by at least one space or tab
At the end a line can have spaces, tabs and comments
'''
FSTAB_LINE = re.compile(r'\s*(?P<fs_spec>\S+)'
                        r'\s+(?P<fs_file>\S+)'
                        r'\s+(?P<fs_vfstype>\S+)'
                        r'\s+(?P<fs_mntops>\S+)'
                        r'\s+(?P<fs_freq>\S+)'
                        r'\s+(?P<fs_passno>\S+)[\s#]*')


def open_fstab(filename):
    '''
    Parses the fstab file and returns an iterator
    '''
    with open(filename, 'r') as fstab:
        for line in fstab:
            result = re.match(FSTAB_LINE, line)
            if result:
                fs_spec = result.group(FS_SPEC)
                fs_file = result.group(FS_FILE)
                fs_vfstype = result.group(FS_VFSTYPE)
                fs_mntops = result.group(FS_MNTOPS)
                fs_freq = result.group(FS_FREQ)
                fs_passno = result.group(FS_PASSNO)
                yield {FS_SPEC: fs_spec,
                       FS_FILE: fs_file,
                       FS_VFSTYPE: fs_vfstype,
                       FS_MNTOPS: fs_mntops,
                       FS_FREQ: fs_freq,
                       FS_PASSNO: fs_passno}


def filter_fstab(fstab, field, value):
    '''
    Field-based filtering
    '''
    for line in fstab:
        if line[field] == value:
            yield line


def ext4_test():
    '''Test ext4'''
    fstab = open_fstab('./srvexa01vm01-fstab')

    filter_ext4 = filter_fstab(fstab, FS_VFSTYPE, 'ext4')
    print('Exibindo ext4')
    for mount in filter_ext4:
        print(mount)


def cifs_test():
    '''Test cifs'''
    fstab = open_fstab('./srvexa01vm01-fstab')

    filter_cifs = filter_fstab(fstab, FS_VFSTYPE, 'cifs')
    print('Exibindo cifs')
    for mount in filter_cifs:
        print(mount)


def main():
    '''
    Showl all tests!
    '''
    ext4_test()
    cifs_test()


if __name__ in "__main__":
    main()
