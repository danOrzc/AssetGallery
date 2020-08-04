""" Environment Creation.

This module contains functions to create environment details on the scene.

Attributes:
    physicalLight (str): Reference to the physical light node.
    envFog (str): Reference to the environment fog node.
"""
import mtoa.utils as mutils
import mtoa.core as core
from maya import cmds

physicalLight = None
envFog = None

class DomeLight(object):

    def __init__(self, elevation, azimuth, intensity):
        self.physicalLight = core.createArnoldNode("aiPhysicalSky")
        self.skyDome = mutils.createLocator("aiSkyDomeLight", asLight=True)

        self.setElevation(elevation)
        self.setAzimuth(azimuth)
        self.setIntensity(intensity)

        cmds.connectAttr("{}.outColor".format(self.physicalLight), "{}.color".format(self.skyDome[0]))
        transformDome = cmds.rename(self.skyDome[1], "SkyDome")

    def setElevation(self, elevation):
        cmds.setAttr("{}.elevation".format(self.physicalLight), elevation)

    def setAzimuth(self, azimuth):
        cmds.setAttr("{}.azimuth".format(self.physicalLight), azimuth)

    def setIntensity(self, intensity):
        cmds.setAttr("{}.intensity".format(self.physicalLight), intensity)

class EnvironmentFog(object):

    def __init__(self, color, distance, height):
        self.fogNode = core.createArnoldNode("aiFog")

        self.setColor(color)
        self.setDistance(distance)
        self.setHeight(height)
        self.setGroundNormal()
        
        cmds.connectAttr("{}.message".format(self.fogNode), "defaultArnoldRenderOptions.atmosphere", force=True)

    def setColor(self, color):
        cmds.setAttr("{}.color".format(self.fogNode), color[0], color[1], color[2], type="double3")

    def setDistance(self, distance):
        cmds.setAttr("{}.distance".format(self.fogNode), distance)

    def setHeight(self, height):
        cmds.setAttr("{}.height".format(self.fogNode), height)

    def setGroundNormal(self, normal=(0,1,0)):
        cmds.setAttr("{}.groundNormalX".format(self.fogNode), normal[0])
        cmds.setAttr("{}.groundNormalY".format(self.fogNode), normal[1])
        cmds.setAttr("{}.groundNormalZ".format(self.fogNode), normal[2])
        

def createSkyLight(elevationSlider, azimuthSlider, intensitySlider, *args):
    elevation = cmds.floatSliderGrp(elevationSlider, query=True, value=True)
    azimuth = cmds.floatSliderGrp(azimuthSlider, query=True, value=True)
    intensity = cmds.floatSliderGrp(intensitySlider, query=True, value=True)

    global physicalLight
    physicalLight = DomeLight(elevation, azimuth, intensity)

def elevationChange(elevation, *args):
    if physicalLight:
        physicalLight.setElevation(elevation)

def azimuthChange(azimuth, *args):
    if physicalLight:
        physicalLight.setAzimuth(azimuth)

def intensityChange(intensity, *args):
    if physicalLight:
        physicalLight.setIntensity(intensity)

def createAiFog(colorSlider, distanceSlider, heightSlider):
    color = cmds.colorSliderGrp(colorSlider, query=True, rgb=True)
    distance = cmds.floatSliderGrp(distanceSlider, query=True, value=True)
    height = cmds.floatSliderGrp(heightSlider, query=True, value=True)

    global envFog
    envFog = EnvironmentFog(color, distance, height)

def colorChange(colorSlider, *args):
    color = cmds.colorSliderGrp(colorSlider, query=True, rgb=True)
    if envFog:
        envFog.setColor(color)

def distanceChange(distance, *args):
    if envFog:
        envFog.setDistance(distance)

def heightChange(height, *args):
    if envFog:
        envFog.setHeight(height)