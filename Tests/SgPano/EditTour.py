from Lib.SgPano.CreateEditTourBasicInformation import BasicInformationTour
from Lib.SgPano.CreateEditTourConnectScenes import ConnectScenesTour
from Lib.SgPano.CreateEditTourUploadScenes import UploadScenesTour
from Lib.SgPano.CreateEditTourUploadedScenes import UploadedScenesTour
from Lib.SgPano.Dashboard import Dashboard
from Lib.SgPano.EditScenes import EditScenes
from Lib.SgPano.HomePage import HomePage
from Lib.SgPano.LogIn import LogIn
from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.common.ScenesGetData import parse_to_scenes

cl = ConfigLoader()
createDriver = DriverData()
driver = createDriver.get_driver()
log = Log(createDriver)

driver.get("https://sgpano.com/")

hp = HomePage(driver)
hp.go_to_log_in()

lp = LogIn(driver)
lp.log_in(cl.get("usernameTrial"), cl.get("passwordTrial"))

db = Dashboard(driver)
db.view_edit_tour()

es = EditScenes(driver)
es.edit_tour(cl.get("tourName"))

cvt = BasicInformationTour(driver)
cvt.set_basic_info(cl.get("tourName")+" edited", "edited", "edited", mode="update")

pictures = parse_to_scenes(cl.get("picturesData"))

pictureForDelete = pictures[1]
uss = UploadedScenesTour(driver)
if not createDriver.driverName == "Safari":
    uss.delete_uploaded_scene(pictureForDelete.title)


us = UploadScenesTour(driver)
scenes = parse_to_scenes(cl.get("picturesDataToAdd"))

if not createDriver.driverName == "Safari":
    us.upload_scenes(scenes)
    uss.insert_scenes_title(scenes)
else:
    uss.btnNext().click()

cs = ConnectScenesTour(driver)
log.info("Add, edit and delete info button")
#when bug is resolved, uncomment
# cs.add_info_button_center("title", "name", "https://sgpano.com/")
# cs.edit_info_button_center("edited title", "edited name", "edited url")
# cs.delete_hotSpotOrInfo_center()

log.info("Add, edit going to, go to and delete hotSpot button")
cs.add_button_to_center()
cs.choose_arrow(1)
cs.save_hotSpot()

cs.edit_hotSpot_center()
cs.edit_hotSpot_goingTo("Third picture")

cs.save_edited_hotSpot()
cs.goTo_hotSpot_center()

cs.change_current_scene("First picture")
#uncomment when bug is resolved
#cs.delete_hotSpotOrInfo_center()

log.info("Insert defined hotSpots")
if not createDriver.driverName == "Safari":
    cs.insert_hotSpots(scenes)

cs.choose_theme(4)

#uncomment when bug is resolved
#cs.delete_hotSpot(pictures[0], pictures[0].hotSpots[0].location)

cs.publish()