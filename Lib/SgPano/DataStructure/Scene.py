"""
Class for holding data for scene.
"""

class Scene:

    def __init__(self, picturePath, title, width, hotSpots):
        """
        Sets scene path (folder name in Images folder), fileName, title that will be added on site,
         full width in pixels (can be found in Paint application) and hotSpots.

        :param picturePath: Folder name with picture name in Images folder. Example: "Tour1/first.jpg"
        :type picturePath: str
        :param title: Title that will be added in SgPano site
        :type title: str
        :param width: Full width of picture
        :type width: int
        :param hotSpots: HotSpots for this scene
        :type hotSpots: HotSpot
        """
        self.folder = picturePath.split("\\")[0]
        self.fileName = picturePath.split("\\")[1]
        self.title = title
        self.width = width
        self.hotSpots = hotSpots


    def __repr__(self):
        sceneString = "Scene in path={}, title={}, full width in px={} and hotSpots=".format(
            self.folder + "\\" + self.fileName, self.title, self.width)
        for hotSpot in self.hotSpots:
            sceneString += str(hotSpot) + ","
        return sceneString