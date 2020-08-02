import os
import AssetConfig as AC
from maya import cmds
from maya import mel
from mtoa.core import createStandIn
reload(AC)


def addObjectToLibrary(name):
    """
    This function exports the object to the correct folders
    """

    os.mkdir(getAssetPath(name))
    saveScreenShot(name)
    saveObject(name)
    exportStandIn(name)
    createSceneAssembly(name)
    
def getAssetPath(name):
    return os.path.join(AC.ASSETS_PATH, name)

def saveObject(name):
    """
    This function saves the object as a source file (Maya Ascii)
    """

    selectedObject = cmds.ls(selection=True)[0]
    path = os.path.join(getAssetPath(name), "{}.ma".format(name))

    originalPos = prepareForExport(selectedObject)

    cmds.file(path, force=True, type='mayaAscii', exportSelected=True)
    removeStudent(path)

    exportAbc(name, selectedObject)

    resetAfterExport(selectedObject, originalPos)

def prepareForExport(dagPath):
    posX = cmds.getAttr(dagPath+".tx")
    posY = cmds.getAttr(dagPath+".ty")
    posZ = cmds.getAttr(dagPath+".tz")

    cmds.move(0,0,0, dagPath, absolute=True)

    return posX, posY, posZ

def resetAfterExport(dagPath, translate):

    cmds.move(translate[0], translate[1], translate[2], dagPath, absolute=True)

def exportAbc(name, dagPath):
    """
    This function saves an Alembic cache of the specified object
    """

    root = "-root {}".format(dagPath)
    save_name = "{}/{}.abc".format(getAssetPath(name), name)
    command = "-worldSpace " + root + " -file " + save_name
    cmds.AbcExport (j = command)

def saveScreenShot(name):
    """
    This function saves a screenshot of the selected object
    """

    path = os.path.join(getAssetPath(name), "{}_SS.jpg".format(name))

    cmds.viewFit()
    selectedObject = cmds.ls(selection=True)[0]
    
    # Set to JPEG
    cmds.setAttr("defaultRenderGlobals.imageFormat", 8)

    # Change view to perspective
    mel.eval('setNamedPanelLayout("Single Perspective View")')
    # Disable selection highlight
    perspPanel = cmds.getPanel( withLabel='Persp View')
    cmds.modelEditor(perspPanel, edit=True, selectionHiliteDisplay=False)

    # Isolate selected
    thePanel = cmds.paneLayout('viewPanes', q=True, pane1=True)
    cmds.isolateSelect(thePanel, state=1)
    cmds.isolateSelect(thePanel, addSelected=True)

    cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200, percent=100, showOrnaments=False, startTime=1, endTime=1, viewer=False)
    
    # Reset isolation
    cmds.isolateSelect(thePanel, removeSelected=True)
    cmds.isolateSelect(thePanel, state=False)

    # Enable hightlight
    cmds.modelEditor(perspPanel, edit=True, selectionHiliteDisplay=True)
    

def createSceneAssembly(name):
    """
    This function creates the Assembly Definition for the specified asset
    """

    # Create Assembly Definition node
    myAssembly = cmds.assembly(name="{}Assembly".format(name))

    # Create Locator representation
    cmds.assembly(myAssembly, edit=True, createRepresentation='Locator', repName="myLocator", input="Annotation: {}".format(myAssembly))

    # Build Scene and Cache Representations
    path = getAssetPath(name)
    path = path.replace('\\', '/')
    
    cmds.assembly(myAssembly, edit=True, createRepresentation='Scene', repName="myScene", input="{}/{}.ma".format(path, name))
    cmds.assembly(myAssembly, edit=True, createRepresentation='Cache', repName="myCache", input="{}/{}.abc".format(path, name))

    # Export Assembly definition and delete from this scene
    cmds.select(myAssembly)
    path = os.path.join(getAssetPath(name), "{}_AD.ma".format(name))
    cmds.file(path, force=True, type='mayaAscii', exportSelected=True)

    removeStudent(path)

    cmds.delete(myAssembly)

def exportStandIn(name):
    """
    This function creates an Arnold standIn for the specified asset
    """
    selectedObject = cmds.ls(selection=True)[0]
    originalPos = prepareForExport(selectedObject)

    path = getAssetPath(name)
    path = os.path.join(getAssetPath(name), "{}_SI.ass".format(name))
    path = path.replace('\\', '/')

    cmds.file(path, force=True, type="ASS Export", exportSelected=True, preserveReferences=True, options="-shadowLinks 1;-mask 6399;-lightLinks 1;-boundingBox;-fullPath")

    resetAfterExport(selectedObject, originalPos)

    #file -force -options "-shadowLinks 1;-mask 6399;-lightLinks 1;-boundingBox;-fullPath" -typ "ASS Export" -pr -es "C:/Users/dog_d/Documents/BCIT/AdvancedScripting/Props1/Props/scenes/StandInTest2.ass";
    #arnoldExportAss -f "C:/Users/dog_d/Documents/BCIT/AdvancedScripting/Props1/Props/scenes/StandInTest2.ass" -s -shadowLinks 1 -mask 6399 -lightLinks 1 -boundingBox -fullPath-cam perspShape;

def removeStudent(fileName):
    """
    This function removes the student tag on the file so it can be opened without the pop up
    """
    studentLine = -1

    with open(fileName) as fp:
        for i, line in enumerate(fp):
            
            if "student" in line:
                studentLine = i
                break
            
            if i > 29:
                break
    
    a_file = open(fileName, "r")
    lines = a_file.readlines()
    a_file.close()

    if studentLine > 0 :
        del lines[studentLine]

        new_file = open(fileName, "w+")

        for line in lines:
            new_file.write(line)

        new_file.close()

def loadAssemblyReference(name):
    """
    This function loads the scene assembly as a reference
    """

    assemblyReference = cmds.container(name=name, type="assemblyReference")
    cmds.setAttr("{}.definition".format(assemblyReference), os.path.join(getAssetPath(name), "{}_AD.ma".format(name)), type="string")
    cmds.setAttr("{}.repNamespace".format(assemblyReference), "{}_NS".format(name), type="string")

    # Set cache as default active representation
    cmds.assembly(assemblyReference, edit=True, active="myCache")
    
def loadCache(name):
    """
    This function loads the specified file as a GPU cache
    """

    assetNode = cmds.createNode("gpuCache", name="{}Geo".format(name))
    cmds.setAttr("{}.cacheFileName".format(assetNode), "{}/{}.abc".format(getAssetPath(name), name), type="string")
    cmds.setAttr("{}.cacheGeomPath".format(assetNode), "|", type="string")

    transform = cmds.listRelatives(assetNode, parent=True)
    transform = cmds.rename(transform, name)


def loadSource(name):
    """
    This function loads the specified file as a maya Ascii
    """

    directory = os.path.join(getAssetPath(name), '{}.ma'.format(name))
    cmds.file(directory, reference=True, type='mayaAscii', mergeNamespacesOnClash=True, namespace=':', options = "v=0;p=17;f=0")

def loadStandIn(name):
    """
    This function loads the specified asset as a Arnold StandIn
    """
    directory = os.path.join(getAssetPath(name), '{}_SI.ass'.format(name))
    standinNode = createStandIn(directory)

    # Change to shaded view
    cmds.setAttr("{}.mode".format(standinNode), 6)

    transform = cmds.listRelatives(standinNode, parent=True)
    transform = cmds.rename(transform, "{}_StandIn".format(name))
