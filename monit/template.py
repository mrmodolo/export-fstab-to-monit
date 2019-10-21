#!/usr/bin/env python3
'''
TODO
'''

from string import Template


_MONIT_TEMPLATE = '''
check filesystem $rootfs path $fs_file
        start program = "/bin/mount $fs_spec" timeout 5 seconds
        stop program = "/bin/umount $fs_spec" with timeout 5 seconds
        if does not exist for 3 cycles then restart
        if does not exist for 3 cycles then exec /usr/local/bin/log_monit_event
'''


_MONIT_TEMPLATE_GROUP = '''
check filesystem $rootfs path $fs_file
        start program = "/bin/mount $fs_spec" timeout 5 seconds
        stop program = "/bin/umount $fs_spec" with timeout 5 seconds
        if does not exist for 3 cycles then restart
        if does not exist for 3 cycles then exec /usr/local/bin/log_monit_event
        group $group
'''


def _rootfs_format(string):
    '''
    TODO
    '''
    return (string[1:]).replace('/', '-')


def build(fs_spec, fs_file, group=None):
    '''
    TODO
    '''
    rootfs = _rootfs_format(fs_file)
    if group:
        tplt = Template(_MONIT_TEMPLATE_GROUP)
        return tplt.substitute(fs_spec=fs_spec, fs_file=fs_file,
                               rootfs=rootfs, group=group)
    tplt = Template(_MONIT_TEMPLATE)
    return tplt.substitute(fs_spec=fs_spec, fs_file=fs_file,
                           rootfs=rootfs)
