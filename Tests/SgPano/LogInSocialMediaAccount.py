from Lib.SgPano.HomePage import HomePage
from Lib.SgPano.LogIn import LogIn
from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log

cl = ConfigLoader()
createDriver = DriverData()
driver = createDriver.get_driver()
log = Log(driver)

url = "https://sgpano.com/"
log.info("Go to {}".format(url))
driver.get(url)

hp = HomePage(driver)
hp.go_to_log_in()

ln = LogIn(driver)
ln.log_in_social_media(cl.get("facebookEmail"), cl.get("facebookPass"))

