Zip Archive Tools
=================
Let's say we have some files::

	/folder
	/folder/001.jpg
	/folder/002.jpg

:func:`~filetool.winzip.zip_a_folder`::

	>>> from filetool.winzip import *
	>>> zip_a_folder("folder", "folder.zip")

Then you get these in your zip archive::

	/folder
	/folder/001.jpg
	/folder/002.jpg

:func:`filetool.winzip.zip_everything_in_a_folder`::

	>>> zip_everything_in_a_folder("folder", "folder.zip")

Then you get these in your zip archive::

	001.jpg
	002.jpg

:func:`filetool.winzip.zip_many_files`::

	>>> zip_many_files(["folder/001.jpg", "folder/002.jpg"], "folder.zip")

Then you get these in your zip archive::

	001.jpg
	002.jpg