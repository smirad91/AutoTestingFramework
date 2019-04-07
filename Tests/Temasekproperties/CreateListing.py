from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.temasekproperties.AddNewDownloads import AddNewDownloads
from Lib.temasekproperties.Downloads import Downloads
from Lib.temasekproperties.HomePage import HomePage
from Lib.temasekproperties.LogIn import LogIn

cl = ConfigLoader()
createDriver = DriverData(driver="Chrome")
driver = createDriver.get_driver()
driver.get("https://temasekproperties.com/wp-login.php")
log = Log(driver)

li = LogIn(driver)
li.log_in("testlist", "test123")

hp = HomePage(driver)
hp.go_to_downloads()

d = Downloads(driver)
d.go_to_add_new()

ad = AddNewDownloads(driver)
ad.set_name("AutoTest download")
ad.set_advertisement_status("Onhold")
ad.set_advertisement_type("Rental")

ad.change_to_text()

ad.set_description("description")
ad.set_model_url("http://modelurl")

ad.locate_download_category()
ad.locate_download_tags()

ad.set_download_category(2,2,2,2)
ad.add_tag("autotestTag")

ad.enable_variable_pricing()

ad.set_excerpt("excerpt description")
ad.choose_author("bmuser (bmuser)")

ad.choose_author("testlist (testlist)")

ad.save_draft()