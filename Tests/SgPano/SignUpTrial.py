from Lib.SgPano.HomePage import HomePage
from Lib.SgPano.SignUp import SignUp
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

sup = SignUp(driver)
sup.open_trial_panotour()

sup.sign_up_trial(cl.get("usernameTrial"), cl.get("passwordTrial"), cl.get("emailTrial"))
