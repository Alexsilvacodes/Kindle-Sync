#!/usr/env/bin python
# -*- coding: utf-8 -*-

from biplist import *
from os.path import expanduser

# Globals
debug = False

#def 

#
# Collect epub from iBooks Library to convert it to .mobi files
#
def collectiBooks():
	home = expanduser("~")

	books_library = readPlist(home + "/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books/Books.plist")

	books = []

	for elem in books_library['Books']:
		if "epub" in elem['path']:
			epub_file = elem['path'].split("/")[-1]
			epub_name = elem['itemName'].encode('utf-8')
			books.append({'book_name': epub_name, 'book_file': epub_file})
			if debug: print "EPUB: ", epub_name, " File: ", epub_file

	return books