#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from filetool.backup import backup_dir


def test_backup_dir():
    root_dir = "testdir"
    ignore_ext = [".txt", ]
    backup_filename = "testdir-backup"
    backup_dir(backup_filename, root_dir, ignore_ext=ignore_ext)


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
