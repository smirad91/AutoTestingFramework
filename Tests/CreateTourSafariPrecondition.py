from Lib.CreateEditTourBasicInformation import BasicInformationTour
from Lib.CreateEditTourUploadScenes import UploadScenesTour
from Lib.CreateEditTourUploadedScenes import UploadedScenesTour
from Lib.Dashboard import Dashboard
from Lib.HomePage import HomePage
from Lib.LogIn import LogIn
from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import close_driver
from Lib.common.ScenesGetData import parse_to_scenes

cl = ConfigLoader()
##upload scenes
createDriver1 = DriverData(driver="Firefox")
driverTemp = createDriver1.get_driver()
driverTemp.get("https://sgpano.com/")
#log = Log(createDriver1)

hp1 = HomePage(driverTemp)

hp1.go_to_log_in()

lp1 = LogIn(driverTemp)
lp1.log_in(cl.get("usernameTrial"), cl.get("passwordTrial"))

db1 = Dashboard(driverTemp)
db1.create_new_tour()

bit1 = BasicInformationTour(driverTemp)
bit1.set_basic_info(title=cl.get("tourName"), address=cl.get("tourAddress"),
                   description=cl.get("tourDescription"), publicAccess=False)

pictures_info2 = cl.get("picturesData")
scenes = parse_to_scenes(pictures_info2)

us1 = UploadScenesTour(driverTemp)
us1.upload_scenes(scenes)

uss1 = UploadedScenesTour(driverTemp)
uss1.insert_scenes_title(scenes)

### scenes uploaded