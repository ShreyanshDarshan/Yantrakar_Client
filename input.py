import cv2
import numpy as np
import datetime
import mysql.connector as mysql
import json

class Input():
    def __init__(self):
        self.db=mysql.connect(host="localhost",user="root",passwd="Shrinivas#100", database="test")
        self.cursor=self.db.cursor()
        self.databaseName="cameraDatabaseFinal"
        self.cameraDataProcessed={
            "000001":{
                "url": "rtsp://shrinivas:khiste@192.168.43.100:8080/h264_pcm.sdp",
                "isPaused": False,
                "counter": 0
            },
            "000002":{
                "url": 0,
                "isPaused": False,
                "counter": 0
            }
        }
        self.initialiseCameras()
        
    def getDataJson(self):
        with open('e:/SHRINIVAS/KGP/SocialDistancingUIDesktop/cameraDatabase.json','r') as jsonFile:
            cameraData=json.load(jsonFile)

        self.cameraDataProcessed= {}

        for cameraKey, cameraValue in cameraData.items():
            if(cameraValue["CalibrationData"]!=None):
                cameraMatrix= np.array(cameraValue["CalibrationData"]["calibrationMatrix"])
                self.cameraDataProcessed.update({
                    cameraKey:{
                        "username": cameraValue["cameraID"],
                        "password": cameraValue["cameraPassword"],
                        "IP": cameraValue["cameraIP"],
                        "isPaused": cameraValue["cameraStatus"]["isPaused"],
                        "counter": 0,
                    } 
                })
                
    def initialiseCameras(self):
        self.cap={}
        for camerakey,cameraData in self.cameraDataProcessed.items():
            self.cap[camerakey] = cv2.VideoCapture(cameraData["url"])
            self.cap[camerakey].set(cv2.CAP_PROP_FPS,1)
            self.cap[camerakey].set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
            self.cap[camerakey].set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
            
    def getFrames(self):
        time=datetime.datetime.now()
        timestamp=str(time.day).zfill(2)+str(time.hour).zfill(2)+str(time.minute).zfill(2)+str(time.second).zfill(2)+str(time.microsecond)[0:3]
        for key,camera in self.cap.items():
            if(not self.cameraDataProcessed[key]["isPaused"]):
                ret, frame=camera.read()
                if(ret):
                    frame=cv2.resize(frame,(256,256))
                    cv2.imwrite("e:/SHRINIVAS/KGP/SocialDistancingUIDesktop/"+key+timestamp+".png",frame)
                    cv2.imshow("img",frame)
                    self.cameraDataProcessed[key]["counter"]=0
                    self.editDatabase(key+timestamp,key)
                else:
                    self.cameraDataProcessed[key]["counter"]=self.cameraDataProcessed[key]["counter"]+1
                if(self.cameraDataProcessed[key]["counter"]>5):
                    self.cameraDataProcessed[key]["isPaused"]=True
                    print("yo")
                    self.editJson(key)
    
    def editDatabase(self,frameID,cameraID):
        query= """INSERT INTO """ +self.databaseName +"""
                (cameraId, 
                frameID, 
                process_flag,
                coordinates, 
                violations) 
                VALUES (%s,%s,%s,%s,%s)"""
        values=(cameraID,frameID,0,None,None)
        self.cursor.execute(query,values)
        self.db.commit()

    def editJson(self,key):
        with open('e:/SHRINIVAS/KGP/SocialDistancingUIDesktop/cameraDatabase.json','r') as jsonFile:
            cameraData=json.load(jsonFile)
        
        cameraData[key]["cameraStatus"]["feedAvailable"]=False
        
        with open('e:/SHRINIVAS/KGP/SocialDistancingUIDesktop/cameraDatabase.json','w') as jsonFile:
            json.dump(cameraData,jsonFile)


if __name__ == "__main__":
    input=Input()
    while(True):
        input.getFrames()   
        cv2.waitKey(1000)
        

#'rtsp://shrinivas:khiste@192.168.43.69'