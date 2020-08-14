To use the tool:

Using Maya's modules to recognize scripts location
Drag "dragToMaya.py" folder to Maya's viewport.
When prompted, please restart Maya
When opening Maya again, the tool will be available to import.

Import the tool by running this command:

import ObjectSpawnWindow as OSW
reload(OSW)
OSW.createWindow()

	
To delete the tool:
	Go to Maya's forlder in documents
	Look for modules folder
	.mod file
	You can now safely delete the project folder
