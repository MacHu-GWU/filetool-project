File Directory Manipulation
===========================
In our model, we define three concept :class:`~filetool.files.WinFile`, :class:`~filetool.files.WinDir`, :class:`~filetool.files.FileCollection`. First two are self explained, :class:`~filetool.files.FileCollection` is collection of files.

Bascially, filetool provides object oriented interface to simplify your work with file and directory.

First, import::

	>>> from filetool.files import WinFile, WinDir, FileCollection


:class:`~filetool.files.WinFile`
---------------------------------
- WinFile.abspath: absolute path
- WinFile.dirname: directory path
- WinFile.basename: file full name
- WinFile.fname: file name without extension
- WinFile.ext: file extension
- WinFile.size_on_disk: file size in bytes
- WinFile.atime: last access time
- WinFile.ctime: create time
- WinFile.mtime: last modify time
- WinFile.md5: file md5 value, check sum

For example::

	>>> abspath = r"C:\downloads\python-logo.png"
	>>> winfile = WinFile(abspath)
	>>> winfile.fname
	'python-logo'

	>>> winfile.ext
	'.png'

	>>> winfile.basename
	'python-logo.png'

	>>> winfile.dirname
	'C:\downloads'

	...

:meth:`Initialize Mode <filetool.files.WinFile.set_initialize_mode>` defines how WinFile instance is being initialized. Because getting more information takes longer, sometime we just want properties we need. By default, we use regular initiation (md5 is not available). You can call :meth:`WinFile.use_fast_init <filetool.files.WinFile.use_fast_init>`, :meth:`WinFile.use_regular_init <filetool.files.WinFile.use_regular_init>`, :meth:`WinFile.use_slow_init <filetool.files.WinFile.use_slow_init>` to customize it.

:meth:`Copy file <filetool.files.WinFile.copy>`, copy file to another place::

	>>> winfile.copy_to(r"C:\downloads\python-logo-copy.png")

:meth:`Rename <filetool.files.WinFile.rename>`, rename/cut file to another place::

	>>> winfile.rename(new_fname="python-logo-copy")

:meth:`Delete <filetool.files.WinFile.delete>`, delete file::

	>>> winfile.delete()

:meth:`Deep copy <filetool.files.WinFile.copy>` :class:`~filetool.files.WinFile` instance::

	>>> winfile1 = winfile.copy()

:meth:`Update <filetool.files.WinFile.update>`, update dirname, fname, extension::

	>>> winfile.update(new_ext=".jpg")
	>>> winfile.ext
	'.jpg'

	# basename also been updated
	>>> winfile.basename
	'python-logo.jpg'


:class:`~filetool.files.WinDir`
--------------------------------
- WinDir.size_total: total size of all files
- WinDir.size_current_total: total size of all files, not include file in 
  subfolder

- WinDir.num_folder_total: number of all directory
- WinDir.num_folder_current: number of all directory, not include subfolder

- WinDir.num_file_total: number of all file
- WinDir.num_file_current: number of all file, not include file in subfolder

::

	>>> dir_path = r"C:\downloads"
	>>> windir = WinDir(dir_path)
	>>> repr(windir)
	...


:class:`~filetool.files.FileCollection`
----------------------------------------
Create a file collection from a directory - select all files::

	>>> dir_path = r"C:\downloads"
	>>> fc = FileCollection.from_path(dir_path)
	>>> print(fc)
	C:\downloads\movie.avi
	C:\downloads\music.mp3
	C:\downloads\image.jpg
	...

Filter files::

	>>> def image_filter(winfile):
	...     if winfile.ext in [".jpg". ".png"]:
	...         return True
	...     else:
	...         return False
	>>> fc = FileCollection.from_path_by_criterion(dir_path, image_filter)
	>>> print(fc)
	C:\downloads\image.jpg

Since it is a collection-like object, of course it **support plus, minus operator**::

	>>> fc1 = FileCollection(["C:\downloads\movie.avi", "C:\downloads\music.mp3"])
	>>> fc2 = FileCollection(["C:\downloads\music.mp3", "C:\downloads\image.jpg"])
	>>> print(fc1 + fc2)
	C:\downloads\movie.avi
	C:\downloads\music.mp3
	C:\downloads\image.jpg

	>>> print(fc1 - fc2)
	C:\downloads\movie.avi

:class:`~filetool.files.FileCollection` is also **iterable, in natural order**::

	>>> for abspath in fc: # yield string
	...      print(abspath)

	>>> for winfile in fc.iterfiles(): # yield winfile instance
	...      print(repr(winfile))

Some time, you only want files or dir but not subfolder, then you can do :meth:`~filetool.files.FileCollection.yield_all_top_winfile` or :meth:`~filetool.files.FileCollection.yield_all_top_windir`.

Here's an example::

	>>> for winfile in FileCollection.yield_all_top_winfile():
	...     print(repr(winfile))

Plus, you can easily **sort files** by it's name, extension, size, ctime... Here's the list of available methods:

- :meth:`~filetool.files.FileCollection.sort_by_abspath`
- :meth:`~filetool.files.FileCollection.sort_by_dirname`
- :meth:`~filetool.files.FileCollection.sort_by_fname`
- :meth:`~filetool.files.FileCollection.sort_by_ext`
- :meth:`~filetool.files.FileCollection.sort_by_atime`
- :meth:`~filetool.files.FileCollection.sort_by_ctime`
- :meth:`~filetool.files.FileCollection.sort_by_mtime`
- :meth:`~filetool.files.FileCollection.sort_by_size`

Here's how::

	>>> fc
	C:\downloads\movie.avi
	C:\downloads\music.mp3
	C:\downloads\image.jpg

	>>> fc.sort_by_abspath()
	>>> fc
	C:\downloads\movie.avi
	C:\downloads\image.jpg
	C:\downloads\music.mp3
	
FileCollection provide many built-in file selection function:

- :meth:`~filetool.files.FileCollection.from_path_except`: select files except falling some rules we defined. For example: by prefix, by extension, by keyword.
- :meth:`~filetool.files.FileCollection.from_path_by_pattern`: select files matching specified patterns.
- :meth:`~filetool.files.FileCollection.from_path_by_size`: select files by size range.
- :meth:`~filetool.files.FileCollection.from_path_by_ext`: select files by extension.
- :meth:`~filetool.files.FileCollection.from_path_by_md5`: select files by md5 checksum.


:class:`~filetool.files.FileFilter`
----------------------------------
This class serves for :meth:`~filetool.files.FileCollection.from_path_by_criterion`. Check out what includes :class:`~filetool.files.FileFilter`.

OK, I know you want example::

	>>> for winfile in FileCollection.from_path_by_criterion(dir_path, FileFilter.image).iterfiles():
	...     # do what ever you want