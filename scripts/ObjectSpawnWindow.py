import os
import random
import ObjectLibrary as OL
import AssetConfig as AC
import EnvironmentCreation as EC
import RoadCreation as RC
import ObjectScattering as ObjScatter
from maya import cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui2
reload(ObjScatter)
reload(OL)
reload(AC)
reload(EC)
reload(RC)

objectScroll = ""
loadMethodRadio = ""
placingRadio = ""
viewportHeight = 0

def createWindow():
    """
    This function initializes the window and displays it.
    """

    windowName = "ObjectSpawner"

    if cmds.window(windowName, query=True, exists=True):
        cmds.deleteUI(windowName)

    cmds.window(windowName)

    populateUI()
    enableEditorDrop()

    cmds.showWindow(windowName)

def enableEditorDrop():
    perspPanel = cmds.getPanel( withLabel='Persp View')
    panelControl = cmds.panel( perspPanel, query=True, control=True)
    cmds.control(panelControl, edit=True, dropCallback=panelDropLoad)
    global viewportHeight
    viewportHeight = cmds.control(panelControl, query=True, h=True)


def populateUI():
    """
    This function manages everything inside the UI, the tabs, buttons, etc.
    """
    
    form = cmds.formLayout()

    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

    # The different Tabs on the window
    spawnTab = SpawnObjectsTab()
    roadTab = RoadRiverTab()
    environmentTab = EnvironmentTab()

    cmds.tabLayout( tabs, edit=True, tabLabel=((spawnTab, 'Spawn Buildings'), (roadTab, 'Create Roads / Rivers'), (environmentTab, "Create Environment") ))

def SpawnObjectsTab():
    mainTab = cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 20))

    cmds.separator(height=10, style="none")
    cmds.text(label="Asset Gallery:", align="left")

    cmds.separator(height=10, style="none")
    SpawnObjectsTab.UserField = cmds.textFieldButtonGrp(placeholderText="Write Asset's Name", buttonLabel="Save Asset", buttonCommand=lambda: saveAsset())
    cmds.separator(height=10, style="none")
    
    cmds.scrollLayout(childResizable=True, height=305, width=455, backgroundColor=(.2,.2,.2))

    global objectScroll
    objectScroll = cmds.gridLayout(cellWidthHeight=(150,150), autoGrow=True)
    
    populateGallery()

    cmds.setParent(mainTab) # Exit scroll layout

    cmds.separator(height=10, style="none")

    global loadMethodRadio

    cmds.rowLayout(numberOfColumns=3, adjustableColumn=3)
    loadMethodRadio = cmds.radioCollection()
    cmds.radioButton("standin", label="Load as Arnold StandIn", select=True)
    cmds.separator(width=20, style="none")
    cmds.radioButton("assembly", label="Load as Assembly Reference")
    cmds.setParent(mainTab)

    global placingRadio
    cmds.separator(height=10)
    cmds.text(label="Spawning method:", align="left")
    cmds.separator(height=5, style="none")
    cmds.rowLayout(numberOfColumns=4, adjustableColumn=4, columnAttach4=("both","both","both","both"), columnOffset4=(10,10,10,10))
    placingRadio = cmds.radioCollection()
    cmds.radioButton("single", label="Single Object", select=True, 
                    onCommand=lambda x: cmds.columnLayout(randomControlLayout, edit=True, enable=False),
                    offCommand=lambda x: cmds.columnLayout(randomControlLayout, edit=True, enable=True))
    cmds.radioButton("curve", label="Along Curve")
    cmds.radioButton("range", label="In Range",
                    onCommand=lambda x: cmds.columnLayout(rangeLayout, edit=True, visible=True),
                    offCommand=lambda x: cmds.columnLayout(rangeLayout, edit=True, visible=False))
    cmds.radioButton("mesh", label="On Mesh")
    #cmds.separator(style="none")
    cmds.setParent(mainTab)

    cmds.separator(height=10, style="none")

    randomControlLayout = cmds.columnLayout(enable=False)
    SpawnObjectsTab.BuildingAmount = cmds.intSliderGrp(label="Building Number", field=True, value=10, min=2, max=50)
    SpawnObjectsTab.RandomRotation = cmds.floatSliderGrp(label="Random Rotation", field=True, value=15, min=0, max=360)
    SpawnObjectsTab.RandomScale = cmds.floatSliderGrp(label="Random Scale", field=True, value=0, min=0, max=10)
    cmds.setParent(mainTab)

    rangeLayout = cmds.columnLayout(visible=False)
    SpawnObjectsTab.MinimumField = cmds.floatFieldGrp(label="Minimum Range: ", numberOfFields=3)
    SpawnObjectsTab.MaximumField = cmds.floatFieldGrp(label="Maximum Range: ", numberOfFields=3)
    cmds.setParent(mainTab)

    cmds.separator(height=10, style="none")
    cmds.button(label='Load Selected Objects', command=lambda x: choosePlacement(x))

    cmds.setParent('..') # Exit column layout

    return mainTab

def populateGallery():
    global objectScroll
    cmds.setParent(objectScroll)

    assetList = [directory for directory in os.listdir(AC.ASSETS_PATH) if os.path.isdir(os.path.join(AC.ASSETS_PATH, directory))]

    for asset in assetList:
        addButtonIcon(asset)

def addButtonIcon(name):
    global objectScroll
    cmds.setParent(objectScroll)

    AssetIcon(name, True)

def loadAsset(name, *args):
    OL.loadAssemblyReference(name)

def saveAsset(*args):
    userName = cmds.textFieldButtonGrp(SpawnObjectsTab.UserField, query=True, text=True)
    if userName:
        name = userName
    else:
        name = cmds.ls(selection=True)[0]

    OL.addObjectToLibrary(name)
    addButtonIcon(name)

def choosePlacement(*args):
    placingMethod = cmds.radioCollection(placingRadio, query=True, select=True)

    if "single" in placingMethod:
        loadSingleObject()
    if "curve" in placingMethod:
        loadMultiple("curve")
    if "range" in placingMethod:
        loadMultiple("range")
    if "mesh" in placingMethod:
        loadMultiple("mesh")

def loadSingleObject(*args):
    selectedRadio = cmds.radioCollection(loadMethodRadio, query=True, select=True)
    objectIconsList = cmds.layout(objectScroll, query=True, childArray=True)

    for obj in objectIconsList:
        isSelected = cmds.iconTextCheckBox(obj, query=True, value=True)

        if isSelected:
            asset = AssetIcon(cmds.iconTextCheckBox(obj, query=True, label=True))

            if "standin" in selectedRadio:
                asset.loadArnoldAsset()
            else: 
                asset.loadAsset()

def loadMultiple(method, *args):

    selectedCurve = selectedMesh = None
    minRangeX = minRangeY = minRangeZ = maxRangeX = maxRangeY = maxRangeZ = 0

    selectedObjects = []

    selectedRadio = cmds.radioCollection(loadMethodRadio, query=True, select=True)
    objectIconsList = cmds.layout(objectScroll, query=True, childArray=True)
    buildingAmount = cmds.intSliderGrp(SpawnObjectsTab.BuildingAmount, query=True, value=True)
    rotationVariation = cmds.floatSliderGrp(SpawnObjectsTab.RandomRotation, query=True, value=True)
    scaleVariation = cmds.floatSliderGrp(SpawnObjectsTab.RandomScale, query=True, value=True)

    for obj in objectIconsList:
        isSelected = cmds.iconTextCheckBox(obj, query=True, value=True)

        if isSelected:
            selectedObjects.append(cmds.iconTextCheckBox(obj, query=True, label=True))

    if not selectedObjects:
        return
        
    scatteringFunction = None

    if method == "curve":
        scatteringFunction = ObjScatter.scatterOnCurve
        selectedCurve = cmds.ls(selection=True)

        if not selectedCurve:
            return

        selectedCurve = selectedCurve[0]

    if method == "range":
        scatteringFunction = ObjScatter.scatterOnRange
        minValues = cmds.floatFieldGrp(SpawnObjectsTab.MinimumField, query=True, value=True)
        minRangeX, minRangeY, minRangeZ = minValues[0], minValues[1], minValues[2]

        maxValues = cmds.floatFieldGrp(SpawnObjectsTab.MaximumField, query=True, value=True)
        maxRangeX, maxRangeY, maxRangeZ = maxValues[0], maxValues[1], maxValues[2]

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

        angle = random.uniform(-rotationVariation, rotationVariation)
        cmds.rotate(angle, loadedAssetNode, y=True, absolute=True)

        newScale = random.uniform(1, 1+scaleVariation)
        cmds.scale(newScale, newScale, newScale, loadedAssetNode, absolute=True)

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

#######################################33

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

##########################

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

class AssetIcon(object):

    def __init__(self, name, create=False):
        self.name = name
        self.icon = os.path.join(AC.ASSETS_PATH, name, "{}_SS.jpg".format(name))

        if create:
            self.buildIcon()

    def buildIcon(self):
        cmds.iconTextCheckBox(image=self.icon, style="iconOnly", label=self.name, height=200, width=200, dragCallback=lambda *x: self.iconDrag(*x))

    def loadAsset(self, *args):
        asset = OL.loadAssemblyReference(self.name)
        return asset

    def loadArnoldAsset(self, *args):
        asset = OL.loadStandIn(self.name)
        return asset

    def iconDrag(self, dragControl, x, y, modifiers ): 
        pass
