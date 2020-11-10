import cameraCalib
import cv2
import numpy as np
import json
import os
from pygame import mixer
import time 


class CalibrateWithoutGUI():

    def __init__(self):
        self.calibrater = cameraCalib.CameraCalibration()
        self.instructionStatus = -1 # -1: Not calibration, 0: Aruco not detected, 1: calibrating, 2: calibration complete
        self.isCalibrating = False
        self.cameraDatabase = None
        self.markerSide = 14.0
        self.cameraID = "000001"
        self.two_up=os.path.dirname(os.path.dirname(__file__))
        mixer.init()
        self.soundNoMarker=mixer.Sound(self.two_up + "/DATA/marker.ogg")
        self.soundDone=mixer.Sound(self.two_up + "/DATA/calibComplete.ogg")
        self.soundDoing=mixer.Sound(self.two_up + "/DATA/calibrating.ogg")

        self.soundDoneDuration=2

        self.openCameraDatabase()

    def saveCalibration(self):
        self.isCalibrating = False
        self.instructionStatus = -1

        calibrationData = {
            'calibrationMatrix': self.calibrater.topViewTransform.tolist(),
            'worldRatio': self.calibrater.worldRatio
        }
        self.cameraDatabase[self.cameraID]['cameraStatus']['calibAvailable'] = True
        self.cameraDatabase[self.cameraID]['CalibrationData'] = calibrationData

        with open(self.two_up + "/DATA/cameraDatabase.json", 'w') as jsonFile:
            json.dump(self.cameraDatabase,jsonFile,sort_keys=True, indent=4)

    def openCameraDatabase(self):
        try:
            with open(self.two_up + "/DATA/cameraDatabase.json", 'r') as jsonFile:
                self.cameraDatabase = json.load(jsonFile)
        except:
            print('Error opening camera database')
        pass


    def calibrate(self, frame):
        if(self.isCalibrating):
            if (not self.calibrater.calibrationDone):
                self.calibrater.calibrate(frame, float(self.markerSide))
                self.instructionStatus = self.calibrater.calibrationLEDStatus
            else:
                self.saveCalibration()

    def startCalibration(self):
        self.isCalibrating = True
        self.calibrater.calibrationDone = 0
        self.instructionStatus = -1

    def runCalibration(self,cap):
        self.startCalibration()
        while True:
            _,frame=cap.read()
            self.calibrate(frame)
            if(self.instructionStatus == 0 and not mixer.Channel(0).get_busy()):
                self.soundNoMarker.play()
            elif(self.instructionStatus == 1 and not mixer.Channel(0).get_busy()):
                self.soundDoing.play()
            elif(not mixer.Channel(0).get_busy()):
                self.soundDone.play()
                time.sleep(self.soundDoneDuration)
                break

calib=CalibrateWithoutGUI()