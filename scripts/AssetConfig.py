""" Asset Config.

This module contains the basic configuration for the paths used
by the tool.

Attributes:
    SCRIPTS_PATH (str): The folder where the scripts are located.
    BASE_PATH (str): The root folder of the tool.
    ASSETS_PATH (str): The folder inside the root where all the assets will be saved

"""
import os

SCRIPTS_PATH = os.path.split(__file__)[0]
BASE_PATH = os.path.split(SCRIPTS_PATH)[0]
ASSETS_PATH = os.path.join(BASE_PATH, 'Assets')

# Create Assets folder if it does not exist
if not os.path.exists(ASSETS_PATH):
    os.makedirs(ASSETS_PATH)