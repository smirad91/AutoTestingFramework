cd %~dp0
cd ..
cd ..
cd ..
cd Tests/SgPano


python CreateTour.py --browser=Firefox --mobile=galaxyS9/S9+ --orientation=Portrait
if ERRORLEVEL 1 pause
python ViewTour.py --browser=Firefox --mobile=galaxyS9/S9+ --orientation=Portrait
if ERRORLEVEL 1 (python RemoveTour.py --browser=Firefox --mobile=galaxyS9/S9+ --orientation=Portrait
pause)
python EditTour.py --browser=Firefox --mobile=galaxyS9/S9+ --orientation=Portrait
if ERRORLEVEL 1 (python RemoveTour.py --browser=Firefox --mobile=galaxyS9/S9+ --orientation=Portrait
pause)
python RemoveTour.py --browser=Firefox --mobile=galaxyS9/S9+ --orientation=Portrait




pause