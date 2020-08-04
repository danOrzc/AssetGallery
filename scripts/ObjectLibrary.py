""" Object Library.

This module contain functions that deal with the importing and exporting of
Assets to their respective directories as different file formats.
"""
import os
import AssetConfig as AC
from maya import cmds
from maya import mel
from mtoa.core import createStandIn


def addObjectToLibrary(name):
    """This function is in charge of exporting the given object to the Asset folder.
    
    Attributes:
        name (str): The name that this asset will be given.
    """

    # Create the directory for this asset
    os.mkdir(getAssetPath(name))
    # Create screenshot
    saveScreenShot(name)
    # Save as .ma
    saveObject(name)
    # Save as .ass
    exportStandIn(name)
    # Generate assembly reference
    createSceneAssembly(name)
    
def getAssetPath(name):
    """This function returns the path to the given asset.
    
    Attributes:
        name (str): The asset name that we are looking in the Assets directory
    """

    return os.path.join(AC.ASSETS_PATH, name)

def saveObject(name):
    """This function saves the object as a source file (Maya Ascii).

    Attributes:
        name (str): The name that will be assigned to the asset
    """

    # Get the selected object(s)
    selectedObject = cmds.ls(selection=True)[0]
    # Create the path to the file
    path = os.path.join(getAssetPath(name), "{}.ma".format(name))

    # Save the original position of the scene's object
    originalPos = prepareForExport(selectedObject)

    # Export selection as .ma
    cmds.file(path, force=True, type='mayaAscii', exportSelected=True)
    # Remove student license text on .ma file
    removeStudent(path)

    # Export selection as .abc
    exportAbc(name, selectedObject)

    # Return the object to it's original position
    resetAfterExport(selectedObject, originalPos)

def prepareForExport(dagPath):
    """This function gets the original position attributes of the given object.
    
    Attributes:
        dagPath (str): The object's path on the scene.

    Return:
        list : A list containing the X, Y and Z values for the object's location.
    """
    # Get Attributes
    posX = cmds.getAttr(dagPath+".tx")
    posY = cmds.getAttr(dagPath+".ty")
    posZ = cmds.getAttr(dagPath+".tz")

    # Move to origin
    cmds.move(0,0,0, dagPath, absolute=True)

    return posX, posY, posZ

def resetAfterExport(dagPath, translate):
    """This function moves a given object to a specified location.
    
    Attributes:
        dagPath (str): The path to the object to move.
        translate (list): A list with x, y and z coordinates.
    """
    cmds.move(translate[0], translate[1], translate[2], dagPath, absolute=True)

def exportAbc(name, dagPath):
    """This function saves an Alembic cache of the specified object.

    Attributes:
        name (str): The name that will be given to the file.
        dagPath (str): The object's path on the scene.
    """

    # Build the command for AbcExport
    root = "-root {}".format(dagPath)
    save_name = "{}/{}.abc".format(getAssetPath(name), name)
    command = "-worldSpace " + root + " -file " + save_name
    # Export with given info
    cmds.AbcExport (j = command)

def saveScreenShot(name):
    """This function saves a screenshot of the selected object.

    Attributes:
        name (str): The name that will be given to the file.
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
    """This function creates the Assembly Definition for the specified asset.

    Attributes:
        name (str):  The name that will be given to the file.
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
    """This function creates an Arnold standIn for the specified asset.

    Attributes:
        name (str):  The name that will be given to the file.
    """

    selectedObject = cmds.ls(selection=True)[0]
    originalPos = prepareForExport(selectedObject)

    path = getAssetPath(name)
    path = os.path.join(getAssetPath(name), "{}_SI.ass".format(name))
    path = path.replace('\\', '/')

    # Export as .ass file
    cmds.file(path, force=True, type="ASS Export", exportSelected=True, preserveReferences=True, options="-shadowLinks 1;-mask 6399;-lightLinks 1;-boundingBox;-fullPath")

    resetAfterExport(selectedObject, originalPos)

def removeStudent(fileName):
    """This function removes the student tag on the file so it can be opened without the pop-up.

    Attributes:
        fileName (str): The name of the .ma file to remove the line from.
    """
    studentLine = -1

    with open(fileName) as fp:
        for i, line in enumerate(fp):
            
            # Look for the word "student" line by line
            if "student" in line:
                studentLine = i
                break
            
            if i > 29:
                break
    
    a_file = open(fileName, "r")
    lines = a_file.readlines()
    a_file.close()

    if studentLine > 0 :
        # Delete the student line if it was found
        del lines[studentLine]

        new_file = open(fileName, "w+")

        # Write the rest of the lines back
        for line in lines:
            new_file.write(line)

        new_file.close()

def loadAssemblyReference(name):
    """This function loads the scene assembly as a reference.

    Attributes:
        name (str): The name of the Asset that we are looking for.

    Returns:
        str: The name of the Assembly Reference Node.
    """

    assemblyReference = cmds.container(name=name, type="assemblyReference")
    cmds.setAttr("{}.definition".format(assemblyReference), os.path.join(getAssetPath(name), "{}_AD.ma".format(name)), type="string")
    cmds.setAttr("{}.repNamespace".format(assemblyReference), "{}_NS".format(name), type="string")

    # Set cache as default active representation
    cmds.assembly(assemblyReference, edit=True, active="myCache")

    return assemblyReference
    
def loadCache(name):
    """This function loads the specified file as a GPU cache.

    Attributes:
        name (str): The name of the Asset that we are looking for.
    """

    # Create gpu cache node
    assetNode = cmds.createNode("gpuCache", name="{}Geo".format(name))
    cmds.setAttr("{}.cacheFileName".format(assetNode), "{}/{}.abc".format(getAssetPath(name), name), type="string")
    cmds.setAttr("{}.cacheGeomPath".format(assetNode), "|", type="string")

    # Get and rename the transform node
    transform = cmds.listRelatives(assetNode, parent=True)
    transform = cmds.rename(transform, name)


def loadSource(name):
    """This function loads the specified file as a maya Ascii.

    Attributes:
        name (str): The name of the Asset that we are looking for.
    """

    # Build the path to the file based on the naame
    directory = os.path.join(getAssetPath(name), '{}.ma'.format(name))
    cmds.file(directory, reference=True, type='mayaAscii', mergeNamespacesOnClash=True, namespace=':', options = "v=0;p=17;f=0")

def loadStandIn(name):
    """This function loads the specified asset as a Arnold StandIn.

    Attributes:
        name (str): The name of the Asset that we are looking for.

    Returns:
        str: The name of the transform node of the StandIn node.
    """
    
    # Get path to .ass file
    directory = os.path.join(getAssetPath(name), '{}_SI.ass'.format(name))
    standinNode = createStandIn(directory)

    # Change to shaded view
    cmds.setAttr("{}.mode".format(standinNode), 6)

    # Get and rename transform node
    transform = cmds.listRelatives(standinNode, parent=True)
    transform = cmds.rename(transform, "{}_StandIn".format(name))

    return transform
