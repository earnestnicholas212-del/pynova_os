#!/usr/bin/env python3
"""
Virtual File System (VFS)
A simple in-memory hierarchical filesystem for the OS simulator.
Supports directories, files, create, read, write, delete, and listing.
"""

import time
from collections import defaultdict


class VFSNode:
    def __init__(self, name, is_dir=False, parent=None):
        self.name = name
        self.is_dir = is_dir
        self.parent = parent
        self.children = {} if is_dir else None
        self.content = b"" if not is_dir else None
        self.size = 0
        self.created = time.time()
        self.modified = time.time()
        self.permissions = "rw-r--r--"

    def path(self):
        if self.parent is None:
            return "/"
        parts = []
        node = self
        while node.parent is not None:
            parts.append(node.name)
            node = node.parent
        return "/" + "/".join(reversed(parts))


class VirtualFileSystem:
    def __init__(self, disk_size=4096):
        self.disk_size = disk_size
        self.used = 0
        self.root = VFSNode("", is_dir=True)
        self._wd = self.root  # working directory

    def _resolve(self, path):
        if path.startswith("/"):
            node = self.root
            parts = path.split("/")[1:]
        else:
            node = self._wd
            parts = path.split("/")
        for part in parts:
            if part == "" or part == ".":
                continue
            if part == "..":
                if node.parent is not None:
                    node = node.parent
                continue
            if not node.is_dir:
                raise FileNotFoundError(f"Not a directory: {node.path()}")
            if part not in node.children:
                raise FileNotFoundError(f"No such file or directory: {part}")
            node = node.children[part]
        return node

    def mkdir(self, path):
        parts = path.strip("/").split("/")
        node = self.root if path.startswith("/") else self._wd
        for part in parts:
            if part == "" or part == ".":
                continue
            if part == "..":
                if node.parent is not None:
                    node = node.parent
                continue
            if not node.is_dir:
                raise NotADirectoryError(f"Not a directory: {node.path()}")
            if part not in node.children:
                node.children[part] = VFSNode(part, is_dir=True, parent=node)
            node = node.children[part]
        return True

    def create(self, path, content=b""):
        if self.used + len(content) > self.disk_size:
            raise OSError("Disk full")
        parent_path = "/".join(path.strip("/").split("/")[:-1])
        name = path.strip("/").split("/")[-1]
        parent = self._resolve(parent_path) if parent_path else self._wd
        if not parent.is_dir:
            raise NotADirectoryError(f"Not a directory: {parent.path()}")
        if name in parent.children:
            raise FileExistsError(f"File exists: {path}")
        file_node = VFSNode(name, is_dir=False, parent=parent)
        file_node.content = content
        file_node.size = len(content)
        file_node.modified = time.time()
        parent.children[name] = file_node
        self.used += len(content)
        return file_node

    def read(self, path):
        node = self._resolve(path)
        if node.is_dir:
            raise IsADirectoryError(f"Is a directory: {path}")
        return node.content

    def write(self, path, content):
        node = self._resolve(path)
        if node.is_dir:
            raise IsADirectoryError(f"Is a directory: {path}")
        delta = len(content) - len(node.content)
        if self.used + delta > self.disk_size:
            raise OSError("Disk full")
        self.used += delta
        node.content = content
        node.size = len(content)
        node.modified = time.time()
        return True

    def delete(self, path):
        node = self._resolve(path)
        parent = node.parent
        if parent is None:
            raise PermissionError("Cannot delete root")
        if node.is_dir and node.children:
            raise OSError("Directory not empty")
        del parent.children[node.name]
        if not node.is_dir:
            self.used -= len(node.content)
        return True

    def ls(self, path="."):
        node = self._resolve(path)
        if not node.is_dir:
            raise NotADirectoryError(f"Not a directory: {path}")
        return [(name, child.is_dir, child.size, child.modified)
                for name, child in node.children.items()]

    def cd(self, path):
        node = self._resolve(path)
        if not node.is_dir:
            raise NotADirectoryError(f"Not a directory: {path}")
        self._wd = node
        return node.path()

    def pwd(self):
        return self._wd.path()

    def stat(self, path):
        node = self._resolve(path)
        return {
            "name": node.name,
            "path": node.path(),
            "is_dir": node.is_dir,
            "size": node.size,
            "created": node.created,
            "modified": node.modified,
            "permissions": node.permissions,
        }
