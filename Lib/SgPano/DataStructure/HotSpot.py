"""
Class for holding data for hotSpot.
"""

class HotSpot:

    def __init__(self, location, goingToScene, up=False, down=False):
        """
        Sets hotSpot location in pixels where hotSpot will be added and goingToScenes as title of scene
        that this hotSpot is showing to.

        :param location: In perspective of width of scene, this is pixel number where hotSpot should be put.
        (This info can be found in Paint application)
        :type location: int
        :param goingToScene: Title of scene that this hotSpot is showing to
        :type goingToScene: str
        """
        self.location = location
        self.goingToScene = goingToScene
        self.up = up
        self.down = down

    def __str__(self):
        return "Hotspot with location in px={} and showing to scene={}".format(self.location, self.goingToScene)

