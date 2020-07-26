import mysql.connector as mysql
import json
import numpy as np
from itertools import combinations
import os

#get the data from the database and json file
#process it for violations
#delete unneccessary files and data
#make changes in database

passFile = open("pass.txt","r")
mysql_pass = passFile.readline()
passFile.close()

class Transformation():
    def __init__(self):
        self.db=mysql.connect(host="localhost",user="root",passwd=mysql_pass, database="test")
        self.cursor=self.db.cursor()
        self.databaseName="cameraDatabaseFinal"
        # self.createDatabase()
        # self.addValues()
        # self.printAllData()
        # self.getDataDatabase()
        # self.getDataJson()
        # self.processData()
        # self.deleteFiles()
        # self.editDatabse()
        # self.printAllData()
        
        self.image_extension=".png"
    
    def createDatabase(self):
        query="""CREATE TABLE """ +self.databaseName +""" 
                (cameraID CHAR(6), 
                frameID CHAR(17)  PRIMARY KEY, 
                process_flag TINYINT, 
                coordinates VARCHAR(160), 
                violations VARCHAR(180) )"""
        self.cursor.execute(query)
        
    def addValues(self):
        query= """INSERT INTO """ +self.databaseName +"""
                (cameraId, 
                frameID, 
                process_flag,
                coordinates, 
                violations) 
            VALUES
                ('000001', '00000124125406421', 1,'10 20,200 20,30 30',NULL),
                ('000001', '00000124125506421', 0, NULL,NULL),
                ('000002', '00000224125406421', 1,'10 20,200 200,300 30',NULL),
                ('000001', '00000124124406421', 2,'10 20,30 40,100 100','10 20|30 40,30 40|100 100')"""
        self.cursor.execute(query)
        self.db.commit()
        
    def printAllData(self):
        query="""SELECT *
                FROM """+self.databaseName+""" 
                LIMIT 40"""
        self.cursor.execute(query)
        
        print(self.cursor.fetchall())
    
    def getDataDatabase(self):
        query="""SELECT *
                FROM """ +self.databaseName +"""
                WHERE process_flag=1"""
        self.cursor.execute(query)
        self.dbData=self.cursor.fetchall()
        
        self.dbDataProcessed={}
        
        for dbDataItem in self.dbData:
            pointsStringList= dbDataItem[3].split(",")
            
            points =[]

            for pointsString in pointsStringList:
                pointStringList=pointsString.split()
                if(len(pointStringList)>0):
                    points.append((int(pointStringList[0]),int(pointStringList[1])))
                
            self.dbDataProcessed.update({
                dbDataItem[1]: points
            })
    
    def getDataJson(self):
        with open('cameraDatabase.json','r') as jsonFile:
            cameraData=json.load(jsonFile)

        self.cameraDataProcessed= {}

        for cameraKey, cameraValue in cameraData.items():
            if(cameraValue["CalibrationData"]!=None):
                cameraMatrix= np.array(cameraValue["CalibrationData"]["calibrationMatrix"])
                self.cameraDataProcessed.update({
                    cameraKey:{
                        "calibrationMatrix": cameraMatrix,
                        "worldRatio": cameraValue["CalibrationData"]["worldRatio"]
                    } 
                })
            else:
                self.cameraDataProcessed.update({
                    cameraKey:{
                        "calibrationMatrix": None,
                        "worldRatio": None
                        }
                })
                
    def findWorldDistance(self,matrix, worldRatio, point1, point2):
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
        
    def processData(self):
        self.violatedPointsData={}
            
        for frameID, dbData in self.dbDataProcessed.items():
            points=combinations(dbData,2)
            violatedPoints=[]
            for point1,point2 in points:
                    distance=self.findWorldDistance(self.cameraDataProcessed[frameID[0:6]]["calibrationMatrix"],self.cameraDataProcessed[frameID[0:6]]["worldRatio"], point1, point2)
                    if(point1 == point2):
                        continue
                    elif(distance == -1):
                        continue
                    elif(distance  < 150):
                        violatedPoints.append((point1,point2))
            self.violatedPointsData.update({
                frameID: violatedPoints
            })

    def deleteFiles(self):
        for frameID,violatedPoints in self.violatedPointsData.items():
            if(len(violatedPoints)==0):
                deleteFile=frameID+self.image_extension
            
                os.remove('./FRAME/'+deleteFile)
    
    def editDatabse(self):
        for frameID in self.dbDataProcessed.keys():
            if(len(self.violatedPointsData[frameID])!=0):
                violationString=self.getStringFromViolatedPoints(self.violatedPointsData[frameID])
                query = """UPDATE """+self.databaseName +"""
                    SET 
                        violations=%s,
                        process_flag=2
                    WHERE 
                        frameID=%s"""
                values=(violationString,frameID)
                self.cursor.execute(query,values)
            else:
                query="DELETE FROM "+self.databaseName +" WHERE frameID=%s"
                values=(frameID,)
            
                self.cursor.execute(query,values)
        
        self.db.commit()

    def getStringFromViolatedPoints(self,violatedPoints):
        if(len(violatedPoints)>10):
            violatedPoints=violatedPoints[0:10]
        violationString=''
        for pointSet in violatedPoints:
            mainString=str(pointSet[0][0])+' '+str(pointSet[0][1])+'|'+str(pointSet[1][0])+' '+str(pointSet[1][1])
            if(len(violationString)!=0):
                violationString=violationString+','+mainString
            else:
                violationString=mainString
        return violationString

if __name__ == "__main__":
    transformation = Transformation()
    transformation.getDataJson()
    oldUpdateIndex = 0
    newUpdateIndex = 0
    while(True):
        transformation.getDataDatabase()
        transformation.processData()
        transformation.deleteFiles()
        transformation.editDatabse()
        updateFile = open("Update.txt","r")
        newUpdateIndex = (updateFile.read())
        updateFile.close()
        if newUpdateIndex != oldUpdateIndex:
            transform.getDataJson()
