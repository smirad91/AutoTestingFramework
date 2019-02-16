cd %~dp0
cd ..
cd ..
cd Tests


python CreateTour.py --browser=Chrome
if ERRORLEVEL 1 pause
python ViewTour.py --browser=Chrome
if ERRORLEVEL 1 pause
python EditTour.py --browser=Chrome
if ERRORLEVEL 1 pause
python RemoveTour.py --browser=Chrome
if ERRORLEVEL 1 pause


pause