"""Object Scattering.

This module contains generators that create random position with some given parameters.
"""
from maya import cmds
import maya.api.OpenMaya as om
import random
import math

def scatterOnCurve(curve, objectCount=5, **kwargs):
    """This function creates random positions along a given curve.
    
    Attributes:
        curve (str): The curve to spawn objects on.
        objectCount (int): The number of copies to spawn.
        **kwargs: Arbitrary keyword arguments.

    Yields:
        list: x, y and z position on the curve.
    """

    # Rebuild the curve to have equal spacing
    rebuiltCurve = cmds.rebuildCurve(curve, degree=1, spans=objectCount-1, end=1, replaceOriginal=False, constructionHistory=False, name="BuildingPathRebuilt")[0]
    cvList = cmds.ls("{}.cv[*]".format(rebuiltCurve), flatten=True)

    # Get each cv's position
    for cv in cvList:
        cvPosition = cmds.pointPosition(cv, world=True)
        yield cvPosition

    # Delete the rebuilt curve
    cmds.delete(rebuiltCurve)

def scatterOnRange(objectCount, minX, minY, minZ, maxX, maxY, maxZ, **kwargs):
    """This function creates random positions along a given curve.
    
    Attributes:
        objectCount (int): The number of copies to spawn.
        minX (int): The minimum X coordicate.
        minY (int): The minimum Y coordicate.
        minZ (int): The minimum Z coordicate.
        maxX (int): The maximum X coordicate.
        maxY (int): The maximum Y coordicate.
        maxZ (int): The maximum Z coordicate.
        **kwargs: Arbitrary keyword arguments.

    Yields:
        list: A random x, y and z position
    """

    # Generate random positions for each object
    for index in xrange(objectCount):
        randomX = random.uniform(minX, maxX)
        randomY = random.uniform(minY, maxY)
        randomZ = random.uniform(minZ, maxZ)

        yield (randomX, randomY, randomZ)

def scatterOnMesh(objectCount, mesh, **kwargs):
    """This function creates random positions along a mesh' surface.
    
    Attributes:
        objectCount (int): The number of copies to spawn.
        mesh (str): The name of the mesh to spawn objects on.
        **kwargs: Arbitrary keyword arguments.

    Yields:
        list: A random location (x, y and z) on the surface of the mesh, and a rotation in Euler angles.
            list[0], list[1] and list[2] Are X, Y and Z coordinates.
            list[3] is x, y and z rotation as Euler angles to align object to normal
    """
    # Generate on each object
    for i in xrange(objectCount):
        position = get3DPosition(mesh)

        # Rotate upvector towards normal
        rotateQuat = om.MQuaternion(om.MVector(0, 1, 0), om.MVector(position[3]))

        # Get rotation in Euler
        rotateEuler = rotateQuat.asEulerRotation()
        rotation = [math.degrees(i) for i in rotateEuler]
        position[3] = rotation
        yield position

def get3DPosition(mesh):
    """This function gets a random 3D position on a mesh's surface.
    
    Attributes:
        mesh (str): The name of the mesh to get the point on.

    Returns:
        list: x, y, z, and Euler angles of the point.
    """
    # Generate random uv coordinate to use with getPointAtUV
    randomU = random.uniform(0,1)
    randomV = random.uniform(0,1)
    position = getPointAtUV(mesh, randomU, randomV)

    # If the position is None, generate another
    if not position:
        position = get3DPosition(mesh)
    return position

def getPointAtUV(mesh, U, V):
    """This function calculates the 3D coordinates based on UV coordinates.
    
    Attributes:
        mesh (str): The name of the mesh to get the point on.
        U (float): the u coordinate on uv
        V (float): the v coordinate on uv

    Returns:
        list: x, y, z, and Euler angles of the point.
    """
    # Create a Selection list (its like a wrapper class for a maya list)
    selList = om.MSelectionList()
    # Add the mesh to the list
    selList.add(mesh)
    # Get MDagPath object based on the mesh
    dagPath = selList.getDagPath(0)
    
    # Check if selected object is a mesh
    if dagPath.hasFn( om.MFn.kMesh ):

        # Get Maya Mesh object based on dagPath
        mesh  = om.MFnMesh(dagPath)
        # Get uv sets
        uvset = mesh.getUVSetNames()
        
        # Get each face
        for face in range(mesh.numPolygons):
            # Try to look for the uv point in the given face
            try:
                # Get uv points on kWorld space
                point = mesh.getPointAtUV(face,U,V,space=om.MSpace.kWorld,uvSet=uvset[0],tolerance=0.0)

                # Get face normal 
                normal = mesh.getPolygonNormal(face)

                # Return the position and the face normal
                result = list(point)[:3] + [list(normal)]
                return result
            
            # If the poiint was not found, there is an exception
            except:
                pass

    return None
