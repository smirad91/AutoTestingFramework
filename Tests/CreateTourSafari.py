import time
from Lib.CreateEditTourConnectScenes import ConnectScenesTour
from Lib.CreateEditTourBasicInformation import BasicInformationTour
from Lib.CreateEditTourUploadedScenes import UploadedScenesTour
from Lib.Dashboard import Dashboard
from Lib.EditScenes import EditScenes
from Lib.HomePage import HomePage
from Lib.LogIn import LogIn
from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import check_if_elem_exist, close_driver
from Lib.common.ScenesGetData import parse_to_scenes
from Lib.common.WaitAction import wait_until

cl = ConfigLoader()

pictures_info2 = cl.get("picturesData")
scenes = parse_to_scenes(pictures_info2)

createDriver = DriverData()
driver = createDriver.get_driver()

driver.get("https://sgpano.com/")

hp = HomePage(driver)
time.sleep(2)
hp.go_to_log_in()
time.sleep(2)
lp = LogIn(driver)
lp.log_in(cl.get("usernameTrial"), cl.get("passwordTrial"))

db = Dashboard(driver)
time.sleep(5)
db.view_edit_tour()

es = EditScenes(driver)
es.edit_tour(cl.get("tourName"))
bi = BasicInformationTour(driver)
wait_until(lambda: check_if_elem_exist(bi.btnSubmit), timeout=10)
bi.btnSubmit().click()

uss = UploadedScenesTour(driver)
wait_until(lambda: check_if_elem_exist(uss.btnNext), timeout=10)
uss.btnNext().click()


csp = ConnectScenesTour(driver)
csp.choose_theme(3)
csp.insert_hotSpots(scenes)
csp.publish()
