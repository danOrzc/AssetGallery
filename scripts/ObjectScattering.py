from maya import cmds
import maya.api.OpenMaya as om
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

def scatterOnMesh(objectCount, mesh, **kwargs):
    for i in xrange(objectCount):
        position = get3DPosition(mesh)

        yield position


def get3DPosition(mesh):
    randomU = random.uniform(0,1)
    randomV = random.uniform(0,1)
    position = getPointAtUV(mesh, randomU, randomV)

    if not position:
        position = get3DPosition(mesh)
    return position


def getPointAtUV(mesh, U, V):
    
    selList = om.MSelectionList()
    selList.add(mesh)
    dagPath = selList.getDagPath(0)
    
    # Check if selected object is a mesh
    if dagPath.hasFn( om.MFn.kMesh ):
        mesh  = om.MFnMesh(dagPath)
        uvset = mesh.getUVSetNames()
        
        for face in range(mesh.numPolygons):
            try:
                point = mesh.getPointAtUV(face,U,V,space=om.MSpace.kWorld,uvSet=uvset[0],tolerance=0.0)
                return list(point)[:3]
            except:
                pass

    return None
