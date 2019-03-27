from Lib.SgPano.CreateEditTourConnectScenes import ConnectScenesTour
from Lib.SgPano.CreateEditTourBasicInformation import BasicInformationTour
from Lib.SgPano.CreateEditTourUploadScenes import UploadScenesTour
from Lib.SgPano.CreateEditTourUploadedScenes import UploadedScenesTour
from Lib.SgPano.Dashboard import Dashboard
from Lib.SgPano.HomePage import HomePage
from Lib.SgPano.LogIn import LogIn
from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.common.ScenesGetData import parse_to_scenes

cl = ConfigLoader()
createDriver = DriverData()
driver = createDriver.get_driver()
driver.get("https://sgpano.com/")
log = Log(driver)

hp = HomePage(driver)

hp.go_to_log_in()

lp = LogIn(driver)
lp.log_in(cl.get("usernameTrial"), cl.get("passwordTrial"))

db = Dashboard(driver)
db.create_new_tour()

bit = BasicInformationTour(driver)
bit.set_basic_info(title=cl.get("tourName"), address=cl.get("tourAddress"),
                   description=cl.get("tourDescription"), publicAccess=False)

pictures_info2 = cl.get("picturesData")
scenes = parse_to_scenes(pictures_info2)

us = UploadScenesTour(driver)
us.upload_scenes(scenes)

uss = UploadedScenesTour(driver)
uss.insert_scenes_title(scenes)

csp = ConnectScenesTour(driver)
csp.choose_theme(3)
csp.insert_hotSpots(scenes)
csp.publish()
