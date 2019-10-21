#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Test
'''

import unittest
import fstab.file


class TestStringMethods(unittest.TestCase):

    def test_fs_file(self):
        self.assertEqual(fstab.file.FS_FILE, 'fs_file')

    def test_fs_spec(self):
        self.assertEqual(fstab.file.FS_SPEC, 'fs_spec')

    def test_fs_freq(self):
        self.assertEqual(fstab.file.FS_FREQ, 'fs_freq')

    def test_fs_passno(self):
        self.assertEqual(fstab.file.FS_PASSNO, 'fs_passno')

    def test_fs_mntops(self):
        self.assertEqual(fstab.file.FS_MNTOPS, 'fs_mntops')

    def test_fs_vfstype(self):
        self.assertEqual(fstab.file.FS_VFSTYPE, 'fs_vfstype')


if __name__ in '__main__':
    unittest.main()
