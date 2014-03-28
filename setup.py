from setuptools import setup

setup(
	name="Kindle Sync",
	app=["KindleSyncMain.py"],
	author="Alejandro Silva",
	url="https://github.com/Alexsays/Kindle-Sync",
	license="GNU General Public License (GPLv2)",
	options={"py2app":
		{"argv_emulation": True, "includes": ["sip", "PyQt4._qt"]}
	},
	setup_requires=["py2app"],
	data_files=[('', ['images'])]
)