#!/usr/bin/env python3
'''
TODO
'''

from string import Template
import fstab


MONIT_TEMPLATE = '''
check filesystem $rootfs path $fs_file
        start program = "/bin/mount $fs_spec" timeout 5 seconds
        stop program = "/bin/umount $fs_spec" with timeout 5 seconds
        if does not exist for 3 cycles then restart
        if does not exist for 3 cycles then exec /usr/local/bin/log_monit_event
'''


def rootfs_format(string):
    '''
    TODO
    '''
    return (string[1:]).replace('/', '-')


def build_template(fs_spec, fs_file):
    '''
    TODO
    '''
    check = Template(MONIT_TEMPLATE)
    rootfs = rootfs_format(fs_file)
    monit = check.substitute(fs_spec=fs_spec, fs_file=fs_file,
                             rootfs=rootfs)
    print(monit)


def main():
    '''
    TODO
    '''
    filename = './srvexa01vm01-fstab'
    filter_cifs = fstab.filter_fstab(fstab.open_fstab(filename),
                                     fstab.FS_VFSTYPE, 'cifs')
    for mount in filter_cifs:
        build_template(mount[fstab.FS_SPEC], mount[fstab.FS_FILE])


if __name__ in "__main__":
    main()
