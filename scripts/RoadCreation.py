"""Road Creation.

This module contains functions that create a road or river on top of a curve.
"""
from maya import cmds

def createRoad(roadWidth=1, quality=50, *args):

    HighResQuality = 200

    selectedCurve = cmds.ls(selection=True)[0]

    widthCurve = cmds.curve(name="widthCurve", degree=1, point=((0,0,0), (0,0,roadWidth)), k=(0,1))
    cmds.CenterPivot()

    cmds.currentTime(1)
    cmds.select(selectedCurve, add=True)
    pathAnim = cmds.pathAnimation(fractionMode=True, follow=True, followAxis="x", upAxis="y", worldUpType="vector", 
                                  worldUpVector=(0,1,0), startTimeU=1, endTimeU=2)

    roadPart = cmds.polyPlane(name="RoadGeo", height=roadWidth, subdivisionsX=1, subdivisionsY=1, constructionHistory=False)[0]
    pConstraint = cmds.pointConstraint(widthCurve, roadPart)
    oConstraint = cmds.orientConstraint(widthCurve,roadPart)

    cmds.delete(pConstraint, oConstraint)
    cmds.polyExtrudeEdge("{}.e[2]".format(roadPart), divisions=quality, constructionHistory=False, inputCurve=selectedCurve)

    cmds.select(roadPart)
    cmds.delete(widthCurve)

def createRiver(riverWidth=1, quality=50, *args):

    HighResQuality = 200

    selectedCurve = cmds.ls(selection=True)[0]
    rebuiltCurve = cmds.rebuildCurve(selectedCurve, spans=HighResQuality, end=1, replaceOriginal=False, constructionHistory=False, name="RoadPathRebuilt")

    widthCurve = cmds.curve(name="widthCurve", degree=1, point=((0,0,0), (0,0,riverWidth)), k=(0,1))
    cmds.CenterPivot()

    cmds.select(rebuiltCurve, add=True)
    pathAnim = cmds.pathAnimation(fractionMode=True, follow=True, followAxis="x", upAxis="y", worldUpType="vector", 
                                  worldUpVector=(0,1,0), startTimeU=1, endTimeU=HighResQuality)
    cmds.selectKey("{}_uValue".format(pathAnim), add=True, keyframe=True, time=(1,HighResQuality))
    cmds.keyTangent(inTangentType="linear", outTangentType="linear")

    cmds.select(widthCurve)

    snapGroup = cmds.snapshot(increment=1, constructionHistory=False, startTime=1, endTime=HighResQuality)[0]
    cmds.select(snapGroup)

    loftSurface = cmds.loft(constructionHistory=False, uniform=True, reverseSurfaceNormals=True)
    loftSurface =  cmds.rebuildSurface(constructionHistory=False, replaceOriginal=True, end=1, keepRange=False, 
                                       keepCorners=False, spansU=1, degreeU=1, spansV=quality, degreeV=3)

    roadGeo = cmds.nurbsToPoly(loftSurface, name="RoadPathGeo", constructionHistory=False, mnd=True, f=3, pt=1, pc=200, chr=.1, ft=.01, mel=.001, d=.1, ut=1, un=3, vt=1, vn=3, uch=0, ucr=0, cht=.2, es=0, ntr=0, mrt=0, uss=1)
    cmds.CenterPivot()

    cmds.delete(loftSurface, snapGroup, widthCurve, rebuiltCurve)