cd %~dp0
cd ..
cd ..
cd ..
cd Tests/SgPano


python CreateTour.py --browser=Chrome
if ERRORLEVEL 1 pause
python ViewTour.py --browser=Chrome
if ERRORLEVEL 1 (python RemoveTour.py --browser=Chrome
pause)
python EditTour.py --browser=Chrome
if ERRORLEVEL 1 (python RemoveTour.py --browser=Chrome
pause)
python RemoveTour.py --browser=Chrome


pause