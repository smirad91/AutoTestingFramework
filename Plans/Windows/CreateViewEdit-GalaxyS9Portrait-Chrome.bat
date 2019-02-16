cd %~dp0
cd ..
cd ..
cd Tests

python CreateTour.py --browser=Chrome --mobile=galaxyS9/S9+ --orientation=Portrait
if ERRORLEVEL 1 pause
python ViewTour.py --browser=Chrome --mobile=galaxyS9/S9+ --orientation=Portrait
if ERRORLEVEL 1 pause
python EditTour.py --browser=Chrome --mobile=galaxyS9/S9+ --orientation=Portrait
if ERRORLEVEL 1 pause
python RemoveTour.py --browser=Chrome --mobile=galaxyS9/S9+ --orientation=Portrait
if ERRORLEVEL 1 pause




pause