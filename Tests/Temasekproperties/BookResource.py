from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.temasekproperties.HomePage import HomePage
from Lib.temasekproperties.Listings import Listings
from Lib.temasekproperties.LogIn import LogIn
from Lib.temasekproperties.Resources import Resources

cl = ConfigLoader()
createDriver = DriverData()
driver = createDriver.get_driver()
driver.get("https://temasekproperties.com/wp-login.php")
log = Log(driver)

li = LogIn(driver)
li.log_in("TestBS", "test123")

hp = HomePage(driver)
hp.go_to_resources_booking()

#hp.go_to_listings()
rb = Resources(driver)

#l.search_for("Derbyshire")

rb.book("Central - Newton", "Derbyshire #22-01")
bookedFor = rb.booking_steps()

hp.go_to_resources_booked()

rb.check_if_exist("6 Derbyshire #22-01",bookedFor)

