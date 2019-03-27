import time

from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.temasekproperties.HomePage import HomePage
from Lib.temasekproperties.Listings import Listings
from Lib.temasekproperties.LogIn import LogIn

cl = ConfigLoader()
createDriver = DriverData(driver="Chrome")
driver = createDriver.get_driver()
driver.get("https://temasekproperties.com/wp-login.php")
log = Log(driver)

li = LogIn(driver)
li.log_in("testagent", "test123")

hp = HomePage(driver)
hp.go_to_listings()

l = Listings(driver)
l.open_listing_by_index(1)

l.purchase_listing("Monthly")



