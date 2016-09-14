#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
filetool.files.py unittest
"""

import os
import pytest
from filetool.files import WinFile, WinDir, FileCollection


#--- WinFile ---
def test_initialize():
    """测试WinFile多种初始化方式的实现。
    """
    winfile = WinFile("test.txt")

    level3_attributes = set([
        "abspath", "dirname", "basename", "fname", "ext",
        "atime", "ctime", "mtime", "size_on_disk", "md5",
    ])
    WinFile.set_initialize_mode(complexity=3)
    winfile = WinFile("test_files.py")
    attributes = set(winfile.to_dict())
    assert attributes == level3_attributes

    level2_attributes = set([
        "abspath", "dirname", "basename", "fname", "ext",
        "atime", "ctime", "mtime", "size_on_disk",
    ])
    WinFile.set_initialize_mode(complexity=2)
    winfile = WinFile("test_files.py")
    attributes = set(winfile.to_dict())
    assert attributes == level2_attributes

    level1_attributes = set([
        "abspath", "dirname", "basename", "fname", "ext",
    ])
    WinFile.set_initialize_mode(complexity=1)
    winfile = WinFile("test_files.py")
    attributes = set(winfile.to_dict())
    assert attributes == level1_attributes

    # 测试完毕, 恢复初始化模式为默认值
    WinFile.set_initialize_mode(complexity=2)


def test_str_and_repr():
    winfile = WinFile("test_files.py")
    print(repr(winfile))


def test_rename():
    """测试文件重命名功能。
    """
    winfile = WinFile("test.txt")

    # 修改文件名为test1
    winfile.rename(new_fname="test1")
    d = winfile.to_dict()
    assert d["fname"] == "test1"

    # 将文件名修改回test
    winfile.rename(new_fname="test")
    d = winfile.to_dict()
    assert d["fname"] == "test"


def test_copy():
    winfile1 = WinFile("test.txt")
    winfile2 = winfile1.copy()
    assert id(winfile1) != id(winfile2)


def test_copy_to_and_remove():
    winfile1 = WinFile("test.txt")
    winfile2 = winfile1.copy()  # create a copy
    winfile2.update(new_fname="test-copy")  # change file name

    assert winfile2.exists() is False  # not exists
    winfile1.copy_to(winfile2.abspath)  # copy to new file
    assert winfile2.exists() is True  # now exists
    assert winfile2.isfile() is True  # now exists
    winfile2.delete()  # delete the new file
    assert winfile2.exists() is False  # not exists

#--- WinDir ---


def test_detail():
    windir = WinDir("testdir")
    # print(repr(windir))


def test_rename():
    windir = WinDir("testdir")

    # 修改文件夹名为testdir1
    windir.rename(new_basename="testdir1")
    d = windir.to_dict()
    assert d["basename"] == "testdir1"

    # 将文件夹名修改回testdir
    windir.rename(new_basename="testdir")
    d = windir.to_dict()
    assert d["basename"] == "testdir"


#--- FileCollection ---
dir_path = "testdir"


def test_yield_file():
    print("{:=^100}".format("yield_all_file_path"))
    for abspath in FileCollection.yield_all_file_path(dir_path):
        print(abspath)

    print("{:=^100}".format("yield_all_winfile"))
    for winfile in FileCollection.yield_all_winfile(dir_path):
        print(repr(winfile))

    print("{:=^100}".format("yield_all_top_file_path"))
    for abspath in FileCollection.yield_all_top_file_path(dir_path):
        print(abspath)

    print("{:=^100}".format("yield_all_top_winfile"))
    for winfile in FileCollection.yield_all_top_winfile(dir_path):
        print(repr(winfile))


def test_from_path():
    fc = FileCollection.from_path(dir_path)
    basename_list = [winfile.basename for winfile in fc.iterfiles()]
    basename_list.sort()
    expect = ["root_file.txt", "root_image.jpg",
              "sub_file.txt", "sub_image.jpg"]
    expect.sort()
    assert basename_list == expect


def test_from_path_by_criterion():
    def image_filter(winfile):
        if winfile.ext in [".jpg", ".png"]:
            return True
        else:
            return False

    fc_yes, fc_no = FileCollection.from_path_by_criterion(
        dir_path, image_filter, keepboth=True)

    basename_list = [winfile.basename for winfile in fc_yes.iterfiles()]
    basename_list.sort()
    expect_yes = ["root_image.jpg", "sub_image.jpg"]
    expect_yes.sort()
    assert basename_list == expect_yes

    basename_list = [winfile.basename for winfile in fc_no.iterfiles()]
    basename_list.sort()
    expect_no = ["root_file.txt", "sub_file.txt"]
    expect_no.sort()


def test_from_path_except():
    """测试from_path_except方法是否能正常工作。
    """
    fc = FileCollection.from_path_except(
        "testdir", ignore=["subfolder", ])
    basename_list = [winfile.basename for winfile in fc.iterfiles()]
    basename_list.sort()
    expect = ["root_file.txt", "root_image.jpg"]
    expect.sort()
    assert basename_list == expect

    fc = FileCollection.from_path_except(
        "testdir", ignore_ext=[".jpg"])
    basename_list = [winfile.basename for winfile in fc.iterfiles()]
    basename_list.sort()
    expect = ["root_file.txt", "sub_file.txt"]
    expect.sort()
    assert basename_list == expect

    fc = FileCollection.from_path_except(
        "testdir", ignore_pattern=["image"])
    basename_list = [winfile.basename for winfile in fc.iterfiles()]
    basename_list.sort()
    expect = ["root_file.txt", "sub_file.txt"]
    expect.sort()
    assert basename_list == expect


def test_from_path_by_pattern():
    """测试from_path_by_pattern方法是否能正常工作。
    """
    fc = FileCollection.from_path_by_pattern(
        "testdir", pattern=["sub"])
    basename_list = [winfile.basename for winfile in fc.iterfiles()]
    basename_list.sort()
    expect = ["sub_file.txt", "sub_image.jpg"]
    expect.sort()
    assert basename_list == expect


def test_from_path_by_size():
    """测试from_from_path_by_size方法是否能正常工作。
    """
    fc = FileCollection.from_path_by_size("testdir", min_size=1024)
    basename_list = [winfile.basename for winfile in fc.iterfiles()]
    basename_list.sort()
    expect = ["root_image.jpg", "sub_image.jpg"]
    expect.sort()
    assert basename_list == expect

    fc = FileCollection.from_path_by_size("testdir", max_size=1024)
    basename_list = [winfile.basename for winfile in fc.iterfiles()]
    basename_list.sort()
    expect = ["root_file.txt", "sub_file.txt"]
    expect.sort()
    assert basename_list == expect


def test_from_path_by_ext():
    """测试from_path_by_ext方法是否能正常工作。
    """
    fc = FileCollection.from_path_by_ext("testdir", ext=".jpg")
    basename_list = [winfile.basename for winfile in fc.iterfiles()]
    basename_list.sort()
    expect = ["root_image.jpg", "sub_image.jpg"]
    expect.sort()
    assert basename_list == expect

    fc = FileCollection.from_path_by_ext("testdir", ext=[".txt"])
    basename_list = [winfile.basename for winfile in fc.iterfiles()]
    basename_list.sort()
    expect = ["root_file.txt", "sub_file.txt"]
    expect.sort()
    assert basename_list == expect


def test_from_path_by_md5():
    WinFile.set_initialize_mode(complexity=3)
    winfile = WinFile("test_files.py")
    WinFile.set_initialize_mode(complexity=2)

    res = FileCollection.from_path_by_md5(os.getcwd(), winfile.md5)
    assert res[0].basename == "test_files.py"


def test_add_and_remove():
    """测试添加WinFile和删除WinFile的方法是否正常工作。
    """
    fc = FileCollection()
    fc.add("test_files.py")
    assert fc.howmany == 1
    fc.remove("test_files.py")
    assert fc.howmany == 0


def test_sort():
    """测试排序功能是否正常工作。
    """
    fc = FileCollection.from_path(dir_path)
    fc.sort_by_abspath()
    fc.sort_by_dirname()
    fc.sort_by_fname()
    fc.sort_by_ext()
    fc.sort_by_atime()
    fc.sort_by_ctime()
    fc.sort_by_mtime()
    fc.sort_by_size()


def test_add():
    """测试两个集合相加是否正常工作。
    """
    fc1 = FileCollection.from_path(dir_path)
    fc2 = FileCollection.from_path(dir_path)
    fc3 = FileCollection()
    fc3.add("test_files.py")

    fc = fc1 + fc2 + fc3
    assert fc.howmany == 5

    fc = FileCollection.sum([fc1, fc2, fc3])
    assert fc.howmany == 5


def test_sub():
    """测试两个集合相减是否正常工作。
    """
    fc1 = FileCollection.from_path(dir_path)
    fc2 = FileCollection.from_path(dir_path)
    fc = fc1 - fc2
    assert fc.howmany == 0


def test_create_fake_mirror():
    src = "testdir"
    dst = "testdir_mirror"
    FileCollection.create_fake_mirror(src, dst)


def test_show_big_file():
    FileCollection.show_big_file(dir_path, 1000)


def test_show_patterned_file():
    FileCollection.show_patterned_file(dir_path, ["image", ])


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
