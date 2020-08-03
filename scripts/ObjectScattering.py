from maya import cmds
import random

def scatterOnCurve(curve, objectCount=5, **kwargs):

    rebuiltCurve = cmds.rebuildCurve(curve, degree=1, spans=objectCount-1, end=1, replaceOriginal=False, constructionHistory=False, name="BuildingPathRebuilt")[0]
    cvList = cmds.ls("{}.cv[*]".format(rebuiltCurve), flatten=True)

    for cv in cvList:
        cvPosition = cmds.pointPosition(cv, world=True)
        yield cvPosition

    cmds.delete(rebuiltCurve)

def scatterOnRange(objectCount, minX, minY, minZ, maxX, maxY, maxZ, **kwargs):

    for index in xrange(objectCount):
        randomX = random.uniform(minX, maxX)
        randomY = random.uniform(minY, maxY)
        randomZ = random.uniform(minZ, maxZ)

        yield (randomX, randomY, randomZ)
