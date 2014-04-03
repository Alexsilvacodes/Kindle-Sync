# -*- coding: utf-8 -*-
#
# 2014 Alex Silva <alexsilvaf28 at gmail.com>

"""
Usage:
    python setup.py py2app
"""

from setuptools import setup

setup(
	name="Kindle Sync",
	app=["KindleSyncMain.py"],
	version="1.0a",
	author="Alejandro Silva",
	url="https://github.com/Alexsays/Kindle-Sync",
	license="GNU General Public License (GPLv2)",
	options={
		"py2app": {
			"iconfile": "icon.icns",
			"argv_emulation": True,
			"includes": ['sip', 'PyQt4.QtCore', 'PyQt4.QtGui'],
			'excludes': ['PyQt4.QtDesigner', 'PyQt4.QtNetwork', 'PyQt4.QtOpenGL', 'PyQt4.QtScript', 
					'PyQt4.QtSql', 'PyQt4.QtTest', 'PyQt4.QtWebKit', 'PyQt4.QtXml', 'PyQt4.phonon',
					'PyQt4.QtXmlPatterns', 'PyQt4.QtSvg', 'PyQt4.QtScriptTools', 'PyQt4.QtNetwork',
					'PyQt4.QtMultimedia', 'PyQt4.QtDeclarative']
		}
	},
	setup_requires=["py2app"],
	data_files=[('', ['images'])]
)