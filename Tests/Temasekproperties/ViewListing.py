import time
from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.temasekproperties.AddNewDownloads import AddNewDownloads
from Lib.temasekproperties.Downloads import Downloads
from Lib.temasekproperties.HomePage import HomePage
from Lib.temasekproperties.Listings import Listings
from Lib.temasekproperties.LogIn import LogIn

cl = ConfigLoader()
createDriver = DriverData(driver="Chrome")
driver = createDriver.get_driver()
driver.get("https://temasekproperties.com/wp-login.php")
log = Log(driver)

li = LogIn(driver)
li.log_in("testlist", "test123")

hp = HomePage(driver)
hp.go_to_listings_nfe()

l = Listings(driver)
l.open_listing_by_index(1)

l.play()
l.moveListing(8)
# time.sleep(10000)
# floor = 1
# while True:
#     if not l.choose_floor(floor):
#         break
#     l.moveListing(8)
#     floor += 1