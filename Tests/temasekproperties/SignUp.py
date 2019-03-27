from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.temasekproperties.LogIn import LogIn
from Lib.temasekproperties.RegistrationAgent import RegistrationAgent

cl = ConfigLoader()
createDriver = DriverData()
driver = createDriver.get_driver()
driver.get("https://temasekproperties.com/wp-login.php")
log = Log(driver)

li = LogIn(driver)
li.go_to_sign_up()

ra = RegistrationAgent(driver)
ra.sign_up("firstname", "lastname", "cea", "mobile")