from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.temasekproperties.HomePage import HomePage
from Lib.temasekproperties.LogIn import LogIn
from Lib.temasekproperties.UserProfile import UserProfile

cl = ConfigLoader()
createDriver = DriverData()
driver = createDriver.get_driver()
driver.get("https://temasekproperties.com/wp-login.php")
log = Log(driver)

li = LogIn(driver)
li.log_in("testagent", "test123")

hp = HomePage(driver)
hp.go_to_user_profile()

up = UserProfile(driver)
up.edit_info(cl.get("updateProfileFirstName"), cl.get("updateProfileLastName"),
             cl.get("updateProfileEmail"), cl.get("updateProfileMobile"))