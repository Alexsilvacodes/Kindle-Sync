#!/usr/env/bin python
# -*- coding: utf-8 -*-

from biplist import *
from os.path import *
from os import mkdir

# Globals
debug = False
home = expanduser("~")
# if MacOS X
ks_folder = home + "/Library/Application Support/Kindle Sync"
ibooks_folder = home + "/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books/"
# if Linux
# ks_folder = home + ".Kindle Sync"

#
# Definition of folder an config files
#
def initFolderConf():
	try:
		mkdir(ks_folder)
		mkdir(ks_folder + "/ConvertedKindle")
	except Exception, e:
		print e

#
# Collect epub from iBooks Library to convert it to .mobi files
#
def collectiBooks():
	books_library = readPlist(ibooks_folder + "Books.plist")

	books = []

	for elem in books_library['Books']:
		if "epub" in elem['path']:
			epub_file = elem['path'].split("/")[-1]
			epub_name = elem['itemName'].encode('utf-8')
			# {book_name: "blabla", book_file: "blabla.epub", converted: True}
			books.append({'book_name': epub_name, 'book_file': epub_file, 'converted': isfile(ks_folder + "/ConvertedKindle/" + epub_file.split(".")[0] + ".mobi")})
			if debug: print "EPUB: ", epub_name, " File: ", epub_file

	return books

#
# Creates Library.plist file
#
def createLibrary(books):
	try:
		writePlist(books, ks_folder + "/Library.plist")
	except Exception, e:
		print e

if debug: collectiBooks()