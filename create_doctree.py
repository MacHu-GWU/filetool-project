#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from docfly import Docfly
import shutil
 
try:
    shutil.rmtree(r"source\filetool")
except Exception as e:
    print(e)
     
docfly = Docfly("filetool", dst="source", 
    ignore=[
        "filetool.zzz_manual_install.py",
        "filetool.tests",
    ]
)
docfly.fly()
