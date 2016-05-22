#!/usr/bin/env python
# -*- coding: utf-8 -*-

from filetool.backup import backup_dir

def test():
    root_dir = "testdir"
    ignore_ext = [".txt",]
    backup_filename = "testdir-backup"
    backup_dir(backup_filename, root_dir, ignore_ext=ignore_ext)

if __name__ == "__main__":
    test()