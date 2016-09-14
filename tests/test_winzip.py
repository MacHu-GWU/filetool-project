#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
from filetool import winzip


def test_winzip():
    winzip.zip_a_folder(os.getcwd(), "1.zip")
    winzip.zip_everything_in_a_folder(os.getcwd(), "2.zip")
    winzip.zip_many_files([__file__,], "3.zip")


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
