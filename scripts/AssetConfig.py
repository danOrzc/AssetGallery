import os

SCRIPTS_PATH = os.path.split(__file__)[0]
BASE_PATH = os.path.split(SCRIPTS_PATH)[0]
ASSETS_PATH = os.path.join(BASE_PATH, 'Assets')

if not os.path.exists(ASSETS_PATH):
    os.makedirs(ASSETS_PATH)