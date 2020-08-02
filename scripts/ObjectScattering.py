from maya import cmds

def scatterOnCurve(curve, quality=5):
    rebuiltCurve = cmds.rebuildCurve(curve, degree=1, spans=quality, end=1, replaceOriginal=False, constructionHistory=False, name="BuildingPathRebuilt")[0]
    cvList = cmds.ls("{}.cv[*]".format(rebuiltCurve), flatten=True)

    for cv in cvList:
        cvPosition = cmds.pointPosition(cv, world=True)
        yield cvPosition

    cmds.delete(rebuiltCurve)
