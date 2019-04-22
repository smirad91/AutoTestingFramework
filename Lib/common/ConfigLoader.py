"""
Class for getting values from json files from Configuration folder
"""

import json
import os
from Lib.common.NonAppSpecific import is_forwarded


class ConfigLoader:

    def getConfigurationPath(self):
        return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           os.pardir, os.pardir, "Configuration"))

    def __init__(self, file="Case1.json", lookArgs=True):
        """
        Mechanism for getting parameters from json file. File should be in Configuration folder and
        it should look like this: {"configuration": {
                                    "key1": "value1",
                                    "key2: "Value2", ...
                                    }

        :param file: File name from Configuration folder with extension .json
        :type file: str
        """
        file = os.path.join(os.path.basename(os.getcwd()), file)
        if lookArgs:
            if is_forwarded("config") is not None:
                file = os.path.join(os.path.basename(os.getcwd()), is_forwarded("config"))
        config_file = os.path.join(self.getConfigurationPath(), file)
        with open(config_file) as f:
            self.data = json.load(f)['configuration']

    def get(self, keyword):
        """
        Return key from file specified at __init__

        :param keyword: Keyword from file
        :type keyword: str
        :return: Object for keyword
        :rtype: str or object
        """
        try:
            return self.data[keyword]
        except Exception as ex:
            return None
