"""
Class used specially for Scenes and HotSpot class from DataStructure folder.
"""
from PIL import Image

from Lib.SgPano.DataStructure.HotSpot import HotSpot
from Lib.SgPano.DataStructure.Scene import Scene
from Lib.common.NonAppSpecific import get_images_path


def get_pictures_string(scenes):
    """
    Return all pictures file name in string (example: "first.jpg", "second.jpg", "third.jpg")

    :param scenes: Scenes to upload
    :type scenes: Scene (from DataStructure folder)
    :return: str
    """
    picturesStr = ""
    for scene in scenes:
        picturesStr += '"' + scene.fileName + '" '
    return picturesStr

def parse_to_scenes(scenes_info):
    """
    Scenes_info should be in Configuration in json file and can be read with ConfigLoader class.
    Example of scenes info:

    "path":"Tour1",
                "scenes": [
                {"fileName":"first.jpg", "title":"First picture", "hotSpots":["Second picture":2717]},
                {"fileName":"second.jpg", "title":"Second picture","hotSpots":["Third picture": 501]},
                {"fileName":"Foto.jpg", "title":"Third picture", "hotSpots":["First picture": 397]}
                ]

    In example above we have:
    path (folder name from Images folder),
    fileName (file name of picture that is located in given path),
    title (title that is going to added when file is going to be loaded in Sgpano create tour),
    hotSpots - Contains title of picture that we want hotSpot to show and location in pixels where should it be (width).
            This info can be also found in Paint, after you move cursor in to location, width can be read in
            down-left corner.

    :param scenes_info: Scenes info explained above
    :type scenes_info: object
    :return: Scenes
    :rtype: Scene (from DataStructure folder)
    """
    scenes = []
    for pic in scenes_info["scenes"]:
        hotSpots = []
        for hotSpot in pic["hotSpots"]:
            hotSpotInfo = hotSpot.split(":")
            up = False
            down = False
            if len(hotSpotInfo) == 3:
                if "up" in hotSpotInfo[2]:
                    up = True
                else:
                    down = True
            goingToScene = hotSpotInfo[0]
            location = int(hotSpotInfo[1])
            hotSpots.append(HotSpot(location, goingToScene, up, down))

        pictureWidth = Image.open(get_images_path(scenes_info["path"] + "/"+ pic["fileName"])).size[0]
        picturePath = scenes_info["path"] + "\\" + pic["fileName"]
        scene = Scene(picturePath, pic["title"], pictureWidth, hotSpots)
        scenes.append(scene)
    return scenes
