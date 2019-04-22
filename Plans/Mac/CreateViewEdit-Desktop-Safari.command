cd ~/Desktop/TemasekGit/Tests/SgPano
python3 CreateTourSafariPrecondition.py
if [ "$?" -ne "0" ]; then
	exit 1
fi
python3 CreateTourSafari.py --browser=Safari
if [ "$?" -ne "0" ]; then
	exit 1
fi
python3 ViewTour.py --browser=Safari
if [ "$?" -ne "0" ]; then
	exit 1
fi
python3 EditTour.py --browser=Safari
if [ "$?" -ne "0" ]; then
	exit 1
fi
python3 RemoveTour.py --browser=Safari