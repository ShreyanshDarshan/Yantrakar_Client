import os
import json
import cv2
import numpy as np

two_up = os.path.dirname(os.path.dirname(__file__))

def findWorldDistance(matrix, worldRatio, point1, point2):
    point1 = np.asarray(point1).reshape((2, 1))
    point2 = np.asarray(point2).reshape((2, 1))

    if(worldRatio==None):
        return -1

    temp = np.zeros((3, 1))
    temp[0][0] = point1[0][0]
    temp[1][0] = point1[1][0]
    temp[2][0] = 1

    cornerInTopView = matrix.dot(temp)
    corner1 = np.zeros((2, 1))
    corner1[0][0] = cornerInTopView[0][0] / cornerInTopView[2][0]
    corner1[1][0] = cornerInTopView[1][0] / cornerInTopView[2][0]

    temp = np.zeros((3, 1))
    temp[0][0] = point2[0][0]
    temp[1][0] = point2[1][0]
    temp[2][0] = 1

    cornerInTopView = matrix.dot(temp)
    corner2 = np.zeros((2, 1))
    corner2[0][0] = cornerInTopView[0][0] / cornerInTopView[2][0]
    corner2[1][0] = cornerInTopView[1][0] / cornerInTopView[2][0]

    if (worldRatio!=None):
        pixelDistance = np.sqrt(
            ((corner1[0][0] - corner2[0][0]) ** 2) + ((corner1[1][0] - corner2[1][0]) ** 2))
        worldDistance = worldRatio * pixelDistance
        return worldDistance
    else:
        return -1

##########################################################

with open(two_up + '/DATA/cameraDatabase.json','r') as jsonFile:
    cameraData=json.load(jsonFile)

cameraDataProcessed= {}

for cameraKey, cameraValue in cameraData.items():
            if(cameraValue["CalibrationData"]!=None):
                cameraMatrix= np.array(cameraValue["CalibrationData"]["calibrationMatrix"])
                cameraDataProcessed.update({
                    cameraKey:{
                        "calibrationMatrix": cameraMatrix,
                        "worldRatio": cameraValue["CalibrationData"]["worldRatio"]
                    } 
                })
            else:
                cameraDataProcessed.update({
                    cameraKey:{
                        "calibrationMatrix": None,
                        "worldRatio": None
                        }
                })

camera = cv2.VideoCapture(two_up + "/test_video/top.mp4")
while True:
    _, orig = camera.read()
    
    point1 = (962, 291)
    point2 = (665, 335)
    
    cv2.circle(orig, point1, radius=5, color=(0, 0, 200), thickness=-1)
    cv2.circle(orig, point2, radius=5, color=(0, 0, 200), thickness=-1)

    M = cameraDataProcessed["000001"]["calibrationMatrix"] 
    distance = findWorldDistance(
                        cameraDataProcessed["000001"]["calibrationMatrix"],
                        cameraDataProcessed["000001"]["worldRatio"],
                        point1, point2)
    print(distance)
    dst = cv2.warpPerspective(orig, M, (1280, 720))
    cv2.imshow("orig", orig)
    cv2.imshow("top", dst)

    cv2.waitKey(1)