Backup utility tools
====================
Usage example::

	>>> from filetool.backup import backup_dir
	>>> backup_dir("wallpaper", r"C:\downloads\wallpapers")
	Perform backup 'C:\downloads\wallpapers'...
	1. Calculate files...
	    Done, got 20 files, total size is 4.50 MB.
	2. Backup files...
	    Write to 'wallpaper 2016-01-01 8h-54m-23s.zip'...
	Complete!

There are three keywords ``ignore``, ``ignore_ext`` and ``ignore_pattern`` is available for filtering out files you don't want to backup. The API is similar to :meth:`~filetool.files.FileCollection.from_path_except`.
