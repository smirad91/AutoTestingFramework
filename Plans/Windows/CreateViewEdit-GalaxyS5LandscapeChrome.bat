cd %~dp0
cd ..
cd ..
cd Tests

::python CreateTour.py --browser=Chrome --mobile="Galaxy S5" --orientation=Landscape
::python ViewTour.py --browser=Chrome --mobile="Galaxy S5" --orientation=Landscape
python EditTour.py --browser=Chrome --mobile="Galaxy S5" --orientation=Landscape
::python RemoveTour.py --browser=Chrome --mobile="Galaxy S5" --orientation=Landscape



pause