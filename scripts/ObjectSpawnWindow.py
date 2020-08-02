import os
import ObjectLibrary as OL
import AssetConfig as AC
import EnvironmentCreation as EC
import RoadCreation as RC
from maya import cmds
reload(OL)
reload(AC)
reload(EC)
reload(RC)

objectScroll = ""
loadMethodRadio = ""

def createWindow():
    windowName = "ObjectSpawner"

    if cmds.window(windowName, query=True, exists=True):
        cmds.deleteUI(windowName)

    cmds.window(windowName)

    populateUI()

    cmds.showWindow(windowName)

def populateUI():
    
    form = cmds.formLayout()

    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

    spawnTab = SpawnObjectsTab()
    roadTab = RoadRiverTab()
    environmentTab = EnvironmentTab()

    cmds.tabLayout( tabs, edit=True, tabLabel=((spawnTab, 'Spawn Buildings'), (roadTab, 'Create Roads / Rivers'), (environmentTab, "Create Environment") ))

def SpawnObjectsTab():
    mainTab = cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 20))

    cmds.separator(height=10, style="none")
    SpawnObjectsTab.UserField = cmds.textFieldButtonGrp(placeholderText="Write Asset's Name", buttonLabel="Save Asset", buttonCommand=lambda: saveAsset())
    cmds.separator(height=10, style="none")
    
    cmds.scrollLayout(childResizable=True, height=305, width=455, backgroundColor=(.2,.2,.2))

    global objectScroll
    objectScroll = cmds.gridLayout(cellWidthHeight=(150,150), autoGrow=True)
    
    populateGallery()

    #cmds.setParent('..') # Exit Grid Layout
    cmds.setParent(mainTab) # Exit scroll layout

    cmds.separator(height=10, style="none")

    global loadMethodRadio

    cmds.rowLayout(numberOfColumns=3, adjustableColumn=3)
    loadMethodRadio = cmds.radioCollection()
    cmds.radioButton("standin", label="Load as Arnold StandIn", select=True)
    cmds.separator(width=20, style="none")
    cmds.radioButton("assembly", label="Load as Assembly Reference")

    cmds.setParent(mainTab)
    cmds.separator(height=10, style="none")
    cmds.button(label='Load Selected Objects', command=lambda x: listObjects(x))

    cmds.setParent('..') # Exit column layout

    return mainTab

def populateGallery():
    global objectScroll
    cmds.setParent(objectScroll)

    #assetList =  os.listdir(AC.ASSETS_PATH)
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

def listObjects(*args):
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

def RoadRiverTab():
    mainTab = cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 20))
    
    cmds.separator(height=10, style="none")
    RoadRiverTab.roadWidth = cmds.floatSliderGrp(label="Road Width", field=True, value=1, min=.01, max=100)
    RoadRiverTab.roadQuality = cmds.intSliderGrp(label="Curve Quality", field=True, value=20, min=2, max=100)

    cmds.separator(height=5, style="none")
    cmds.button(label='Create road', command=buildRoad)

    cmds.setParent('..')

    return mainTab

def buildRoad(*args):
    width = cmds.floatSliderGrp(RoadRiverTab.roadWidth, query=True, value=True)
    quality = cmds.intSliderGrp(RoadRiverTab.roadQuality, query=True, value=True)

    RC.createRoad(width, quality)

def EnvironmentTab():
    mainTab = cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 20))
    
    cmds.separator(height=10, style="none")
    elevationSlider = cmds.floatSliderGrp(label="Elevation", field=True, value=45, min=0, max=90, dragCommand=lambda value:EC.elevationChange(value))
    azimuthSlider = cmds.floatSliderGrp(label="Azimuth", field=True, value=90, min=0, max=360, dragCommand=lambda value:EC.azimuthChange(value))
    intensitySlider = cmds.floatSliderGrp(label="Intensity", field=True, value=1, min=.1, max=10, dragCommand=lambda value:EC.intensityChange(value))

    cmds.separator(height=5, style="none")
    cmds.button(label='Create Sky Dome', command=lambda x: EC.createSkyLight(elevationSlider, azimuthSlider, intensitySlider))

    cmds.setParent('..')

    return mainTab

class AssetIcon(object):

    def __init__(self, name, create=False):
        self.name = name
        self.icon = os.path.join(AC.ASSETS_PATH, name, "{}_SS.jpg".format(name))

        if create:
            self.buildIcon()

    def buildIcon(self):
        cmds.iconTextCheckBox(image=self.icon, style="iconOnly", label=self.name, height=200, width=200)

    def loadAsset(self, *args):
        OL.loadAssemblyReference(self.name)

    def loadArnoldAsset(self, *args):
        OL.loadStandIn(self.name)
