cd %~dp0
cd ..
cd ..
cd ..
cd Tests/Temasekproperties

python ViewListing.py --browser=Firefox --mobile=galaxyS9/S9+ --orientation=Landscape
if ERRORLEVEL 1 pause
python PurchaseListing.py --browser=Firefox --mobile=galaxyS9/S9+ --orientation=Landscape
if ERRORLEVEL 1 pause
python CreateListing.py --browser=Firefox --mobile=galaxyS9/S9+ --orientation=Landscape
if ERRORLEVEL 1 pause
python BookResource.py --browser=Firefox --mobile=galaxyS9/S9+ --orientation=Landscape
if ERRORLEVEL 1 pause




pause