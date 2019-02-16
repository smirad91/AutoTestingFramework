from Lib.CreateEditTourBasicInformation import BasicInformationTour
from Lib.CreateEditTourConnectScenes import ConnectScenesTour
from Lib.CreateEditTourUploadScenes import UploadScenesTour
from Lib.CreateEditTourUploadedScenes import UploadedScenesTour
from Lib.Dashboard import Dashboard
from Lib.EditScenes import EditScenes
from Lib.HomePage import HomePage
from Lib.LogIn import LogIn
from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.common.ScenesGetData import parse_to_scenes

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
es.edit_tour(cl.get("tourName"))

cvt = BasicInformationTour(driver)
cvt.set_basic_info(cl.get("tourName")+" edited", "edited", "edited", mode="update")

pictures = parse_to_scenes(cl.get("picturesData"))

pictureForDelete = pictures[1]
uss = UploadedScenesTour(driver)
uss.delete_uploaded_scene(pictureForDelete.title)


us = UploadScenesTour(driver)
scenes = parse_to_scenes(cl.get("picturesDataToAdd"))

us.upload_scenes(scenes)
uss.insert_scenes_title(scenes)

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
cs.insert_hotSpots(scenes)

#uncomment when bug is resolved
#cs.delete_hotSpot(pictures[0], pictures[0].hotSpots[0].location)

cs.publish()