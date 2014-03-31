#!/bin/bash
#
# 2014 Alex Silva <alexsilvaf28 at gmail.com>

if [ -f $(pwd)/kindlegen ]: then
	if [ -d $(pwd)/dist/ ]; then
		sudo rm -R $(pwd)/dist
		sudo rm -R $(pwd)/build
	fi

	sudo python setup.py py2app;

	if [ -d $(pwd)/dist/Kindle\ Sync.app/Contents/Frameworks ]; then
		sudo cp $(pwd)/kindlegen $(pwd)/dist/Kindle\ Sync.app/Contents/Resources;
		sudo chmod -R 755 $(pwd)/dist $(pwd)/dist/Kindle\ Sync.app/Contents/
		echo ""
		echo $'\E[1;32m >> Deployed correctly << \E[0m';
		echo ""
	else
		echo ""
		echo $'\E[1;31m >> Deploy failed << \E[0m';
		echo ""
	fi
else
	echo "";
	echo $'\E[1;31m >> Download kindlegen from: (http://www.amazon.com/gp/feature.html?docId=1000765211) and put it on this folder << \E[0m';
	echo "";
fi