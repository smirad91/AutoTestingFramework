from Lib.Dashboard import Dashboard
from Lib.EditScenes import EditScenes
from Lib.HomePage import HomePage
from Lib.LogIn import LogIn
from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log

cl = ConfigLoader()
createDriver = DriverData()
driver = createDriver.get_driver()

log = Log(driver)

driver.get("https://sgpano.com/")

hp = HomePage(driver)
hp.go_to_log_in()

lp = LogIn(driver)
lp.log_in(cl.get("usernameTrial"), cl.get("passwordTrial"))

db = Dashboard(driver)
db.view_edit_tour()

es = EditScenes(driver)
es.remove_tour_by_name(cl.get("tourName")+" edited")
