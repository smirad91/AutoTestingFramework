cd ~/Desktop/SgPanoCleanGit/Tests/SgPano
python3 CreateTourSafariPrecondition.py
if [ "$?" -ne "0" ]; then
	exit 1
fi
python3 CreateTourSafari.py --browser=Safari --mobile=galaxyS9/S9+ --orientation=Landscape
if [ "$?" -ne "0" ]; then
	exit 1
fi
python3 ViewTour.py --browser=Safari --mobile=galaxyS9/S9+ --orientation=Landscape
if [ "$?" -ne "0" ]; then
	python3 RemoveTour.py --browser=Safari --mobile=galaxyS9/S9+ --orientation=Landscape
	exit 1
fi
python3 EditTourSafari.py --browser=Safari --mobile=galaxyS9/S9+ --orientation=Landscape
if [ "$?" -ne "0" ]; then
    python3 RemoveTour.py --browser=Safari --mobile=galaxyS9/S9+ --orientation=Landscape
	exit 1
fi
python3 RemoveTour.py --browser=Safari --mobile=galaxyS9/S9+ --orientation=Landscape