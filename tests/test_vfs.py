#!/usr/bin/env python3
"""Unit tests for the Virtual File System."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from filesystem.vfs import VirtualFileSystem, VFSNode


class TestVFS(unittest.TestCase):
    def setUp(self):
        self.vfs = VirtualFileSystem(disk_size=1024)

    def test_mkdir_and_cd(self):
        self.vfs.mkdir("/home")
        self.vfs.mkdir("/home/user")
        self.assertEqual(self.vfs.cd("/home/user"), "/home/user")
        self.assertEqual(self.vfs.pwd(), "/home/user")

    def test_create_and_read(self):
        self.vfs.mkdir("/tmp")
        self.vfs.create("/tmp/hello.txt", b"world")
        self.assertEqual(self.vfs.read("/tmp/hello.txt"), b"world")

    def test_write_and_size(self):
        self.vfs.mkdir("/tmp")
        self.vfs.create("/tmp/a.txt", b"abc")
        self.vfs.write("/tmp/a.txt", b"abcdef")
        self.assertEqual(self.vfs.read("/tmp/a.txt"), b"abcdef")
        info = self.vfs.stat("/tmp/a.txt")
        self.assertEqual(info["size"], 6)

    def test_ls(self):
        self.vfs.mkdir("/dir")
        self.vfs.create("/dir/f1.txt", b"1")
        self.vfs.create("/dir/f2.txt", b"22")
        entries = self.vfs.ls("/dir")
        names = [e[0] for e in entries]
        self.assertIn("f1.txt", names)
        self.assertIn("f2.txt", names)

    def test_delete_file(self):
        self.vfs.mkdir("/tmp")
        self.vfs.create("/tmp/del.txt", b"xxx")
        self.vfs.delete("/tmp/del.txt")
        with self.assertRaises(FileNotFoundError):
            self.vfs.read("/tmp/del.txt")

    def test_delete_nonempty_dir_fails(self):
        self.vfs.mkdir("/tmp")
        self.vfs.create("/tmp/x.txt", b"x")
        with self.assertRaises(OSError):
            self.vfs.delete("/tmp")

    def test_disk_full(self):
        small = VirtualFileSystem(disk_size=10)
        small.mkdir("/tmp")
        small.create("/tmp/a.txt", b"12345")
        with self.assertRaises(OSError):
            small.create("/tmp/b.txt", b"123456")

    def test_relative_paths(self):
        self.vfs.mkdir("/home")
        self.vfs.mkdir("/home/docs")
        self.vfs.cd("/home")
        self.vfs.create("docs/rel.txt", b"relative")
        self.assertEqual(self.vfs.read("docs/rel.txt"), b"relative")


if __name__ == '__main__':
    unittest.main()
