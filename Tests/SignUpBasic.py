from Lib.HomePage import HomePage
from Lib.SignUp import SignUp
from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log

cl = ConfigLoader()
createDriver = DriverData()
driver = createDriver.get_driver()
log = Log(driver)
driver.get("https://sgpano.com/")

hp = HomePage(driver)
hp.go_to_sign_up()

su = SignUp(driver)
su.open_basic_panotour()

su.sign_up_paid(cl.get("usernameBasic"), cl.get("passwordBasic"), cl.get("emailBasic"),
                cl.get("payPalEmail"), cl.get("payPalPassword"))