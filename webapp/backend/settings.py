# Settings handler
# To make changes to settings, please use the file settings.json

import json
import os
import sys

# Example taken from here: https://gist.github.com/nadya-p/b25519cf3a74d1bed86ed9b1d8c71692
# Handler for loading the settings.json file
# Initialized class can be used with:
#   from backend.settings import settings
#   settings.app["name"]

class Settings:
    _config_location = 'settings.json'
    adminToken = ""

    def __init__(self):
      if os.path.exists(self._config_location):
        self.__dict__ = json.load(open(self._config_location))
      else:
        sys.exit("COULD NOT LOAD THE SETTINGS.JSON FILE")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        json.dump(self.__dict__, open(self._config_location, 'w'))

settings = Settings()