cd %~dp0
cd ..
cd ..
cd ..
cd Tests/SgPano

python CreateTour.py --browser=Chrome --mobile=galaxyS9/S9+ --orientation=Landscape
if ERRORLEVEL 1 pause
python ViewTour.py --browser=Chrome --mobile=galaxyS9/S9+ --orientation=Landscape
if ERRORLEVEL 1 (python RemoveTour.py --browser=Chrome --mobile=galaxyS9/S9+ --orientation=Landscape
pause)
python EditTour.py --browser=Chrome --mobile=galaxyS9/S9+ --orientation=Landscape
if ERRORLEVEL 1 (python RemoveTour.py --browser=Chrome --mobile=galaxyS9/S9+ --orientation=Landscape
pause)
python RemoveTour.py --browser=Chrome --mobile=galaxyS9/S9+ --orientation=Landscape



pause