import cv2
import numpy as np
import datetime
# import mysql.connector as mysql
import json
import pandas as pd
# import rtsp

# passFile = open("pass.txt","r")
# mysql_pass = passFile.readline()
# passFile.close()

class Input():
    def __init__(self):
        # self.db=mysql.connect(host="localhost",user="root",passwd=mysql_pass, database="test")
        # self.cursor=self.db.cursor()
        # self.databaseName="cameraDatabaseFinal"
        self.image_extension=".png"
        self.cameraDataProcessed={
            # "000001":{
            #     "url": "rtsp://shrinivas:khiste@192.168.43.100:8080/h264_pcm.sdp",
            #     "isPaused": False,
            #     "counter": 0
            # },
            "000001":{
                "url": 0,
                "isPaused": False,
                "counter": 0
            }
        }
        # self.getDataJson()
        self.initialiseCameras()
        
    def getDataJson(self):
        with open('cameraDatabase.json','r') as jsonFile:
            cameraData=json.load(jsonFile)

        self.cameraDataProcessed= {}

        for cameraKey, cameraValue in cameraData.items():
            if(cameraValue["CalibrationData"]!=None):
                # cameraMatrix= np.array(cameraValue["CalibrationData"]["calibrationMatrix"])
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
            # self.cap[camerakey] = cv2.VideoCapture("rtsp://"+cameraData["username"]+":"+cameraData["password"]+"@"+cameraData["IP"])
            self.cap[camerakey] = cv2.VideoCapture("./test_video/top.mp4") # cv2.VideoCapture(cameraData["url"])
            self.cap[camerakey].set(cv2.CAP_PROP_FPS,1)
            self.cap[camerakey].set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
            self.cap[camerakey].set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
            
    def getFrames(self,updateIndex,sharedMem):
        time=datetime.datetime.now()
        timestamp=str(time.day).zfill(2)+str(time.hour).zfill(2)+str(time.minute).zfill(2)+str(time.second).zfill(2)+str(time.microsecond)[0:3]
        for key,camera in self.cap.items():
            if(not self.cameraDataProcessed[key]["isPaused"]):
                ret, frame=camera.read()
                if(ret):
                    frame=cv2.resize(frame,(256,256))
                    cv2.imwrite("./FRAMES/"+key+timestamp+self.image_extension,frame)
                    # cv2.imshow("img",frame)
                    self.cameraDataProcessed[key]["counter"]=0
                    self.editSheredMemory(key+timestamp,sharedMem)
                else:
                    self.cameraDataProcessed[key]["counter"]=self.cameraDataProcessed[key]["counter"]+1
                if(self.cameraDataProcessed[key]["counter"]>5):
                    self.cameraDataProcessed[key]["isPaused"]=True
                    # print("yo")
                    self.editJson(key,updateIndex)
    
    # def editDatabase(self,frameID,cameraID):
    #     self.db.reconnect()
    #     query= """INSERT INTO """ +self.databaseName +"""
    #             (cameraId, 
    #             frameID, 
    #             process_flag,
    #             coordinates, 
    #             violations) 
    #             VALUES (%s,%s,%s,%s,%s)"""
    #     values=(cameraID,frameID,0,None,None)
    #     self.cursor.execute(query,values)
    #     self.db.commit()

    def editSheredMemory (self, frameID, sharedMem):
        sharedMem.append(frameID)

    def editJson(self,key,updateIndex):
        with open('cameraDatabase.json','r') as jsonFile:
            cameraData=json.load(jsonFile)
        
        cameraData[key]["cameraStatus"]["feedAvailable"]=False
        cameraData[key]["cameraStatus"]["isPaused"]=True
        
        with open('cameraDatabase.json','w') as jsonFile:
            json.dump(cameraData,jsonFile)
            self.sendUpdate(updateIndex)

    def sendUpdate(self, updateIndex):
        updateIndex.value += 1
        print("sending update from input.py")
        # updateFile = open("Update.txt","r")
        # UpdateIndex = (updateFile.read())
        # updateFile.close()
        # updateFile = open("Update.txt","w")
        # updateFile.write(str(UpdateIndex + 1))
        # updateFile.close()


images_upper_limit=10
images_lower_limit=5
waitDuration=500
targetDuration=500
upperDurationCounter=None
fpsChangeFactor=2

# if __name__ == "__main__":
def beginInput(updateIndex, shared_images):
    global images_upper_limit,images_lower_limit,waitDuration,targetDuration,upperDurationCounter
    global fpsChangeFactor
    input=Input()
    print (input.cameraDataProcessed)
    oldUpdateIndex = updateIndex.value
    while(True):
        if updateIndex.value != oldUpdateIndex:
            print("getting json data in input.py")
            # input.getDataJson()
        
        #FPS MANAGEMENT
        if(len(shared_images)>images_upper_limit):
            if(upperDurationCounter==None):
                upperDurationCounter=0
                targetDuration=targetDuration*fpsChangeFactor
                waitDuration=targetDuration
            upperDurationCounter=upperDurationCounter+1
            print("fps decreased")
            if(upperDurationCounter>5):
                upperDurationCounter=0
                targetDuration=targetDuration*fpsChangeFactor
                waitDuration=targetDuration
        elif(len(shared_images)<images_lower_limit):
            print("fps increased")
            upperDurationCounter=0
            if(waitDuration-targetDuration<10):
                targetDuration=targetDuration/fpsChangeFactor
            waitDuration=updateWaitDuration(0.5,waitDuration,targetDuration)
            
        oldUpdateIndex = updateIndex.value
        input.getFrames(updateIndex, shared_images)
        
        # if(len(shared_images)>10):
        cv2.waitKey(int(waitDuration))
        
def updateWaitDuration(updateRate,currentDuration,targetDuration):
    return (1-updateRate)*currentDuration+updateRate*targetDuration
        
# up = 0
# beginInput(up)
#'rtsp://shrinivas:khiste@192.168.43.69'