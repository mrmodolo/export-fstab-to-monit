#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Export cifs mount point to monit
'''


import fstab.file
import monit.template


def main():
    '''
    Export to stdout
    '''
    filename = './srvexa01vm01-fstab'
    filter_cifs = fstab.file.apply_filter(
        fstab.file.get_lines(filename),
        fstab.file.FS_VFSTYPE, 'cifs')
    for mount in filter_cifs:
        monitor = monit.template.build(
            mount[fstab.file.FS_SPEC],
            mount[fstab.file.FS_FILE],
            group='FSTAB')
        print(monitor)


if __name__ in '__main__':
    main()
