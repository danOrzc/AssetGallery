""" Main Window module.

This module has the functions for UI creation and implementation.
"""
import os
import random
import ObjectLibrary as OL
import AssetConfig as AC
import EnvironmentCreation as EC
import RoadCreation as RC
import ObjectScattering as ObjScatter
from maya import cmds
import maya.api.OpenMaya as om
reload(ObjScatter)
reload(OL)
reload(AC)
reload(EC)
reload(RC)

objectScroll = ""
loadMethodRadio = ""
placingRadio = ""
viewportHeight = 0

class AssetIcon(object):
    """ A class representation of a checkbox containing the asset's screenshot.

    Attributes:
        name (str): The name in the folder hierarchy for this asset.
        icon (str): The path to the asset's screenshot.

    """

    def __init__(self, name, create=False):
        self.name = name
        self.icon = os.path.join(AC.ASSETS_PATH, name, "{}_SS.jpg".format(name))

        # If we want to create this icon on the UI
        if create:
            self.buildIcon()

    def buildIcon(self):
        """This function creates a iconTextCheckBox in the current layout with the set attributes."""

        cmds.iconTextCheckBox(image=self.icon, style="iconOnly", label=self.name, height=200, width=200, dragCallback=lambda *x: self.iconDrag(*x))

    def loadAsset(self, *args):
        """This function loads an Assembly Reference based on the name of this AssetIcon.
        
        Returns:
            str : The name of the root node of the Assembly Reference.
        """

        asset = OL.loadAssemblyReference(self.name)
        return asset

    def loadArnoldAsset(self, *args):
        """This function loads an Asset as an Arnold StandIn based on the name.

        Returns:
            str : The name of the Arnold StandIn node.
        """
        asset = OL.loadStandIn(self.name)
        return asset

    def iconDrag(self, dragControl, x, y, modifiers ): 
        pass


def createWindow():
    """This function initializes the window and displays it."""

    windowName = "ObjectSpawner"

    if cmds.window(windowName, query=True, exists=True):
        cmds.deleteUI(windowName)

    cmds.window(windowName)

    populateUI()
    enableEditorDrop()

    cmds.showWindow(windowName)

def enableEditorDrop():
    """ This function enables drag & drop functionality on the Model Editor."""

    perspPanel = cmds.getPanel( withLabel='Persp View')
    panelControl = cmds.panel( perspPanel, query=True, control=True)
    cmds.control(panelControl, edit=True, dropCallback=panelDropLoad)
    global viewportHeight
    viewportHeight = cmds.control(panelControl, query=True, h=True)


def populateUI():
    """This function manages everything inside the UI, the tabs, buttons, etc."""
    
    # Main form layout and it's attachment config
    form = cmds.formLayout()
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

    # Tab Layout
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

    # The different Tabs on the window
    spawnTab = SpawnObjectsTab()
    roadTab = RoadRiverTab()
    environmentTab = EnvironmentTab()

    # Tab creation
    cmds.tabLayout( tabs, edit=True, tabLabel=((spawnTab, 'Spawn Buildings'), (roadTab, 'Create Roads / Rivers'), (environmentTab, "Create Environment") ))

############################################# ASSET GALLERY SECTION #############################################################

def SpawnObjectsTab():
    """This function creates a layout containing the object spawning functionality.

    Returns:
        str : The reference to the layout.
    """

    ### Create main Layout for the tab
    mainTab = cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 20))

    cmds.separator(height=10, style="none")
    cmds.text(label="Asset Gallery:", align="left")

    ### Asset Name Text Field
    cmds.separator(height=10, style="none")
    SpawnObjectsTab.UserField = cmds.textFieldButtonGrp(placeholderText="Write Asset's Name", buttonLabel="Save Asset", buttonCommand=lambda: saveAsset())
    
    ### Asset Gallery Layout
    cmds.separator(height=10, style="none")
    cmds.scrollLayout(childResizable=True, height=305, width=455, backgroundColor=(.2,.2,.2))
    global objectScroll
    objectScroll = cmds.gridLayout(cellWidthHeight=(150,150), autoGrow=True)
    populateGallery()   # Creates Icons
    cmds.setParent(mainTab) # Exit scroll layout

    ### Choose between Arnold StandIn and Assembly Reference
    cmds.separator(height=10, style="none")
    global loadMethodRadio
    cmds.rowLayout(numberOfColumns=3, adjustableColumn=3)
    loadMethodRadio = cmds.radioCollection()
    cmds.radioButton("standin", label="Load as Arnold StandIn", select=True)    # Radio button for StandIn
    cmds.separator(width=20, style="none")
    cmds.radioButton("assembly", label="Load as Assembly Reference")    # Radio button for Assembly
    cmds.setParent(mainTab)

    ### Choose how to set the location of the object
    cmds.separator(height=10)
    cmds.text(label="Spawning method:", align="left")
    cmds.separator(height=5, style="none")
    cmds.rowLayout(numberOfColumns=4, adjustableColumn=4, columnAttach4=("both","both","both","both"), columnOffset4=(10,10,10,10))
    global placingRadio
    placingRadio = cmds.radioCollection()
    # Create only one copy
    cmds.radioButton("single", label="Single Object", select=True, 
                    onCommand=lambda x: cmds.columnLayout(randomControlLayout, edit=True, enable=False),
                    offCommand=lambda x: cmds.columnLayout(randomControlLayout, edit=True, enable=True))
    # Create copies along a curve
    cmds.radioButton("curve", label="Along Curve")
    # Create copies between a range in world space
    cmds.radioButton("range", label="In Range",
                    onCommand=lambda x: cmds.columnLayout(rangeLayout, edit=True, visible=True),
                    offCommand=lambda x: cmds.columnLayout(rangeLayout, edit=True, visible=False))
    # Create copies on a mesh's surface
    cmds.radioButton("mesh", label="On Mesh")
    cmds.setParent(mainTab)

    ### Randomization parameters
    cmds.separator(height=10, style="none")
    randomControlLayout = cmds.columnLayout(enable=False)
    # How many copies
    SpawnObjectsTab.BuildingAmount = cmds.intSliderGrp(label="Building Number", field=True, value=10, min=2, max=50, fieldMaxValue=200)
    # Deviation from original rotation
    SpawnObjectsTab.RandomRotation = cmds.floatSliderGrp(label="Random Rotation", field=True, value=15, min=0, max=360)
    # Deviation from orignal scale
    SpawnObjectsTab.RandomScale = cmds.floatSliderGrp(label="Random Scale", field=True, value=0, min=0, max=10)
    cmds.setParent(mainTab)

    ### Range spawning parameters
    rangeLayout = cmds.columnLayout(visible=False)
    # Min x, y and z coordinates
    SpawnObjectsTab.MinimumField = cmds.floatFieldGrp(label="Minimum Range: ", numberOfFields=3)
    # Max x, y and z coordinates
    SpawnObjectsTab.MaximumField = cmds.floatFieldGrp(label="Maximum Range: ", numberOfFields=3)
    cmds.setParent(mainTab)

    ### Finalize
    cmds.separator(height=10, style="none")
    cmds.button(label='Load Selected Objects', command=lambda x: choosePlacement(x))
    cmds.setParent('..') # Exit column layout
    return mainTab

def populateGallery():
    """This function creates an icon for each folder created in the Assets directory."""

    # Set the UI parent to be the scroll layout
    global objectScroll
    cmds.setParent(objectScroll)

    # List all assets in the direcoty
    assetList = [directory for directory in os.listdir(AC.ASSETS_PATH) if os.path.isdir(os.path.join(AC.ASSETS_PATH, directory))]

    # Create a ButtonIcon for each asset
    for asset in assetList:
        addButtonIcon(asset)

def addButtonIcon(name):
    """This function adds a ButtonIcon with given name to the scroll layout."""

    # Set parent to be the scroll layout
    global objectScroll
    cmds.setParent(objectScroll)

    # Instance object, with create flag set to True
    AssetIcon(name, True)

def saveAsset(*args):
    """This function saves an Asset to the asset directory."""

    # Get user assigned name
    userName = cmds.textFieldButtonGrp(SpawnObjectsTab.UserField, query=True, text=True)

    # Use user's name if there is one or object's if there isn't
    if userName:
        name = userName
    else:
        name = cmds.ls(selection=True)[0]

    # Add to Library
    OL.addObjectToLibrary(name)
    # Create icon
    addButtonIcon(name)

def choosePlacement(*args):
    """This function selects the correct placement method based on the user's selection on the Radio Buttons."""

    # Query radio buttons
    placingMethod = cmds.radioCollection(placingRadio, query=True, select=True)

    # Choose placement function
    if "single" in placingMethod:
        loadSingleObject()
    if "curve" in placingMethod:
        loadMultiple("curve")
    if "range" in placingMethod:
        loadMultiple("range")
    if "mesh" in placingMethod:
        loadMultiple("mesh")

def loadSingleObject(*args):
    """This function loads a single copy of the selected asset."""

    # Query selected assets
    objectIconsList = cmds.layout(objectScroll, query=True, childArray=True)
    # Query selection between Arnold StandIN / Assembly reference
    selectedRadio = cmds.radioCollection(loadMethodRadio, query=True, select=True)

    for obj in objectIconsList:
        isSelected = cmds.iconTextCheckBox(obj, query=True, value=True)

        if isSelected:
            # If this icon is selected, instance an icon object
            asset = AssetIcon(cmds.iconTextCheckBox(obj, query=True, label=True))

            # Choose how to load it
            if "standin" in selectedRadio:
                asset.loadArnoldAsset()
            else: 
                asset.loadAsset()

def loadMultiple(method, *args):
    """This function loads multiple copies of the selected assets.
    
    Attributes:
        method (str): A string representing the method that will be used to place the assets.
            'curve' : Spawns copies along a NURBS curve.  
            'range' : Spawns copies on a range in the spcae. 
            'mesh' : Spawns copies on a mesh's surface.
    """

    ### Declaring attributes
    selectedCurve = selectedMesh = None
    minRangeX = minRangeY = minRangeZ = maxRangeX = maxRangeY = maxRangeZ = 0
    selectedObjects = []

    ### Query UI values
    # Choise between standin / assembly
    selectedRadio = cmds.radioCollection(loadMethodRadio, query=True, select=True)
    # List of all asset icons on UI
    objectIconsList = cmds.layout(objectScroll, query=True, childArray=True)
    # Amount of copies
    buildingAmount = cmds.intSliderGrp(SpawnObjectsTab.BuildingAmount, query=True, value=True)
    # Deviation from original rotation
    rotationVariation = cmds.floatSliderGrp(SpawnObjectsTab.RandomRotation, query=True, value=True)
    # Deviation from original scale
    scaleVariation = cmds.floatSliderGrp(SpawnObjectsTab.RandomScale, query=True, value=True)

    ### Iterate over each asset icon
    for obj in objectIconsList:

        # Append to list if the asset is selected
        isSelected = cmds.iconTextCheckBox(obj, query=True, value=True)

        if isSelected:
            selectedObjects.append(cmds.iconTextCheckBox(obj, query=True, label=True))

    # Exit the function if no asset is selected
    if not selectedObjects:
        return
        
    # Reference to the function that will scatter the copies
    scatteringFunction = None

    ### The user chose "curve"
    if method == "curve":
        
        # Set function from ObjectScattering.py
        scatteringFunction = ObjScatter.scatterOnCurve

        # Get curve reference
        selectedCurve = cmds.ls(selection=True)
        if not selectedCurve:
            return
        selectedCurve = selectedCurve[0]

    ### The user chose "range"
    if method == "range":

        # Set function from ObjectScattering.py
        scatteringFunction = ObjScatter.scatterOnRange

        # Query minimum values from floatField
        minValues = cmds.floatFieldGrp(SpawnObjectsTab.MinimumField, query=True, value=True)
        minRangeX, minRangeY, minRangeZ = minValues[0], minValues[1], minValues[2]
        # Query maximum values from floatField
        maxValues = cmds.floatFieldGrp(SpawnObjectsTab.MaximumField, query=True, value=True)
        maxRangeX, maxRangeY, maxRangeZ = maxValues[0], maxValues[1], maxValues[2]

    ### The user chose "mesh"
    if method == "mesh":
        scatteringFunction = ObjScatter.scatterOnMesh
        selectedMesh = cmds.ls(selection=True)

        if not selectedMesh:
            return

        selectedMesh = selectedMesh[0]
        
    finalGroup = cmds.group(name="CurveAssetGroup", empty=True)
    cmds.select(clear=True)

    for position in scatteringFunction(objectCount=buildingAmount, curve=selectedCurve,
                                       minX=minRangeX, minY=minRangeY, minZ=minRangeZ, maxX=maxRangeX, maxY=maxRangeY, maxZ=maxRangeZ,
                                       mesh=selectedMesh):
        
        asset = AssetIcon(random.choice(selectedObjects))
        loadedAssetNode = None

        if "standin" in selectedRadio:
            loadedAssetNode = asset.loadArnoldAsset()
        else: 
            loadedAssetNode = asset.loadAsset()

        cmds.move(position[0], position[1], position[2], loadedAssetNode, absolute=True)

        if len(position) == 4:
            cmds.rotate(position[3][0], position[3][1], position[3][2], loadedAssetNode, absolute=True)
        
        angle = random.uniform(-rotationVariation, rotationVariation)
        cmds.rotate(angle, loadedAssetNode, y=True, relative=True, objectSpace=True)

        newScale = random.uniform(1, 1+scaleVariation)
        cmds.scale(newScale, newScale, newScale, loadedAssetNode, absolute=True)

        #cmds.FreezeTransformations(loadedAssetNode)

        cmds.parent(loadedAssetNode, finalGroup)

def panelDropLoad( dragControl, dropControl, messages, x, y, dragType ): 
    loadedObject = cmds.iconTextCheckBox(dragControl, query=True, label=True)
    selectedRadio = cmds.radioCollection(loadMethodRadio, query=True, select=True)
    asset = AssetIcon(loadedObject)
   
    loadedAssetNode = None

    if "standin" in selectedRadio:
        loadedAssetNode = asset.loadArnoldAsset()
    else: 
        loadedAssetNode = asset.loadAsset()
        
    loadedLocation = cmds.autoPlace(useMouse=True)
    cmds.move(loadedLocation[0], loadedLocation[1], loadedLocation[2], loadedAssetNode, absolute=True)

############################################# ROAD / RIVER SECTION #############################################################

def RoadRiverTab():
    mainTab = cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 20))
    
    cmds.separator(height=10, style="none")
    cmds.text(label="Generate road and rivers:", align="left")
    RoadRiverTab.roadWidth = cmds.floatSliderGrp(label="Road Width", field=True, value=1, min=.01, max=100)
    RoadRiverTab.roadQuality = cmds.intSliderGrp(label="Curve Quality", field=True, value=20, min=2, max=100)

    cmds.separator(height=5, style="none")
    cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
    cmds.button(label='Create Road', width=200, command=buildRoad)
    cmds.separator(style="none")
    cmds.button(label="Create River", width=200, command=buildRiver)

    cmds.setParent('..')
    cmds.setParent('..')

    return mainTab

def buildRoad(*args):
    width = cmds.floatSliderGrp(RoadRiverTab.roadWidth, query=True, value=True)
    quality = cmds.intSliderGrp(RoadRiverTab.roadQuality, query=True, value=True)

    RC.createRoad(width, quality)

def buildRiver(*args):
    width = cmds.floatSliderGrp(RoadRiverTab.roadWidth, query=True, value=True)
    quality = cmds.intSliderGrp(RoadRiverTab.roadQuality, query=True, value=True)

    RC.createRiver(width, quality)

############################################# ENVIRONMENT #############################################################

def EnvironmentTab():
    mainTab = cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 20))
    
    cmds.separator(height=10, style="none")
    cmds.text(label="Physical Light:", align="left")
    elevationSlider = cmds.floatSliderGrp(label="Elevation", field=True, value=45, min=0, max=90, 
                                          dragCommand=lambda value:EC.elevationChange(value),
                                          changeCommand=lambda value:EC.elevationChange(value))
    azimuthSlider = cmds.floatSliderGrp(label="Azimuth", field=True, value=90, min=0, max=360, 
                                        dragCommand=lambda value:EC.azimuthChange(value),
                                        changeCommand=lambda value:EC.azimuthChange(value))
    intensitySlider = cmds.floatSliderGrp(label="Intensity", field=True, value=1, min=.1, max=10, 
                                          dragCommand=lambda value:EC.intensityChange(value),
                                          changeCommand=lambda value:EC.intensityChange(value))

    cmds.separator(height=5, style="none")
    cmds.button(label='Create Sky Dome', command=lambda x: EC.createSkyLight(elevationSlider, azimuthSlider, intensitySlider))

    cmds.separator(height=20)
    cmds.text(label="Environment Fog:", align="left")
    colorSlider = cmds.colorSliderGrp(label="Color", rgb=(1,1,1), 
                                      dragCommand=lambda value:EC.colorChange(colorSlider),
                                      changeCommand=lambda value:EC.colorChange(colorSlider))
    distanceSlider = cmds.floatSliderGrp(label="Distance", field=True, value=.02, min=0, max=1000, step=.01, 
                                         dragCommand=lambda value:EC.distanceChange(value), 
                                         changeCommand=lambda value:EC.distanceChange(value))
    heightSlider = cmds.floatSliderGrp(label="Height", field=True, value=5, min=0, max=1000, step=.1, 
                                        dragCommand=lambda value:EC.heightChange(value),
                                        changeCommand=lambda value:EC.heightChange(value))

    cmds.separator(height=5, style="none")
    cmds.button(label='Create Environment Fog', command=lambda x: EC.createAiFog(colorSlider, distanceSlider, heightSlider))

    cmds.setParent('..')

    return mainTab


