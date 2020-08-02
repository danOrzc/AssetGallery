import mtoa.utils as mutils
import mtoa.core as core
from maya import cmds

physicalLight = None

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

