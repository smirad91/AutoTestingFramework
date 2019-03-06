python3 ~/Desktop/SgPanoCleanGit/Tests/CreateTourSafariPrecondition.py
if [ "$?" -ne "0" ]; then
	exit 1
fi
python3 ~/Desktop/SgPanoCleanGit/Tests/CreateTourSafari.py --browser=Safari --mobile=galaxyS9/S9+ --orientation=Portrait
if [ "$?" -ne "0" ]; then
	exit 1
fi
python3 ~/Desktop/SgPanoCleanGit/Tests/ViewTour.py --browser=Safari --mobile=galaxyS9/S9+ --orientation=Portrait
if [ "$?" -ne "0" ]; then
	exit 1
fi
python3 ~/Desktop/SgPanoCleanGit/Tests/EditTour.py --browser=Safari --mobile=galaxyS9/S9+ --orientation=Portrait
if [ "$?" -ne "0" ]; then
	exit 1
fi
python3 ~/Desktop/SgPanoCleanGit/Tests/RemoveTour.py --browser=Safari --mobile=galaxyS9/S9+ --orientation=Portrait