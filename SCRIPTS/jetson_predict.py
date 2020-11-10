from mxnet import gluon
import requests
import mxnet as mx
from PIL import Image
import numpy as np
import json
import pickle
import base64
import time
# import mysql.connector as mysql
import _thread
import threading 
import gzip
# import transformation
from itertools import combinations
import os
from cryptography.fernet import Fernet
import ast
import pandas as pd
import datetime
import cv2
# passFile = open("pass.txt","r")
# mysql_pass = passFile.readline()
# passFile.close()

two_up = os.path.dirname(os.path.dirname(__file__)) #"C:/Users/Shreyansh Darshan/Documents/GitHub/Yantrakar_Client" #

class Predict():
    def __init__(self, isLocal):
        # self.db = mysql.connect(
        #     host="localhost", user="root", passwd=mysql_pass, database="test")
        # self.cursor = self.db.cursor()
        # self.databaseName = "cameraDatabaseFinal"
        if(isLocal):
            self.ctx = mx.gpu() if mx.context.num_gpus() else mx.cpu()
            self.net = self.get_model()
        self.image_extension=".png"
        self.getDataJson()
        
        self.encryptionKey = b'gkmrxai04WhOcWj3EGl-2Io58Q8biOWOytdQbPhNYGU='
        
        self.getSystemConfiguration()
        self.camera = cv2.VideoCapture(two_up + "/test_video/top.mp4")
        
    def getSystemConfiguration(self):
        with open(two_up + '/DATA/userSetting.txt','r') as file:
            data=file.read()
        cipher=Fernet(self.encryptionKey)
        userSetting=ast.literal_eval((cipher.decrypt(data.encode('utf-8'))).decode('utf-8'))
        self.activationKey=userSetting["activationKey"]
        self.apiURL=userSetting["apiURL"]
        self.numberOfLambda=userSetting["numberOfLambda"]

    # def getNames(self):
    #     self.db.reconnect()
    #     query = """SELECT frameID
    #             FROM """ + self.databaseName + """
    #             WHERE process_flag=0
    #             ORDER BY SUBSTRING(frameID, 7) 
    #             LIMIT 6"""
    #     self.cursor.execute(query)
    #     return self.cursor.fetchall()
    
    def read_pics_api(self, img_names):
        imgs = []

        for name in img_names:
            im = Image.open(two_up + "/FRAMES/" + name + self.image_extension)
            im = (np.array(im)).reshape(256, 256, 3)
            imgs.append(im)

        return imgs
    
    def predict_api(self, imageNames):
        # """file = open('/home/karan/conv/foo.b64', 'rb')

        # temp = file.read()

        # """
        imgs = self.read_pics_api(imageNames)

        l = []

        print(len(imgs))

        for i in range(len(imgs)):

            dictionary = {}
            dictionary['name'] = imageNames[i]

            dictionary['data'] = [imgs[i]]

            l.append(dictionary)

        temp = pickle.dumps(l)
        temp = base64.b64encode(temp)
        temp = gzip.compress(temp)

        # """with open("imgs.gz", "wb") as f:
        #     f.write(temp)"""

        start = time.time()

        api_endpoint = self.apiURL

        headers = {'content-encoding': 'gzip','x-api-key':self.activationKey}

        res = requests.post(url=api_endpoint, data=temp, headers=headers)

        print(time.time()-start)

        return ast.literal_eval(res.content.decode('utf-8'))

    def read_pics_local(self):
        imgs = []
        # # print (img_names)
        # for name in img_names:
        #     # if os.path.isfile('./FRAMES/'+name[0]+self.image_extension) :
        #     im = Image.open(
        #         two_up + '/FRAMES/'+name+self.image_extension)
        
        ret, im = self.camera.read()
        im = cv2.resize(im, (256, 256))
        cv2.imshow("lk", im) 
        im = (np.array(im)).reshape(256, 256, 3)
        imgs.append(im)
        cv2.waitKey(1)
        imgs = np.stack(imgs, axis=0)

        return mx.nd.array(imgs, self.ctx), im

    def get_model(self):
        net = gluon.nn.SymbolBlock.imports(two_up + "/DATA/new_ssd_512_mobilenet1.0_voc-symbol.json", [
                                           'data'], two_up + "/DATA/new_ssd_512_mobilenet1.0_voc-0000.params", ctx=self.ctx)
        return net

    def predict_local(self):

        x, im = self.read_pics_local()

        # net = self.get_model() 

        idx, prob, bbox = self.net(x)
        idx = idx.asnumpy()
        prob = prob.asnumpy()
        bbox = bbox.asnumpy()
        detection = idx.shape[1]
        # pred = {}

        # for i in range(len(img_names)):
        ctr = 0
        temp = []
        for k in range(detection):
            if idx[0][k][0] == 14.0 and ctr < 10 and prob[0][k][0] >= 0.4:
                ctr += 1
                cords = bbox[0][k].tolist()
                temp.append((int((cords[0]+cords[2])/2), int(cords[3])))

            # pred.update({im: temp})

        return im, temp

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
        
    def getDataJson(self):
        with open(two_up + '/DATA/cameraDatabase.json','r') as jsonFile:
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
        
    def processData(self, im, dbData):
        violatedPointsData={}
            
    
        points=combinations(dbData,2)
        violatedPoints=[]
        for point1,point2 in points:
                distance=self.findWorldDistance(self.cameraDataProcessed["000001"]["calibrationMatrix"],self.cameraDataProcessed["000001"]["worldRatio"], point1, point2)
                if(point1 == point2):
                    continue
                elif(distance == -1):
                    continue
                elif(distance  < 150):
                    violatedPoints.append((point1,point2))
        violatedPointsData.update({
            "000001": violatedPoints
        })

        # DELETE FILES
        for frameID,violatedPoints in violatedPointsData.items():
            if(len(violatedPoints)>0):
                for pointpair in violatedPoints:
                    im = cv2.line(im, pointpair[0], pointpair[1], (0, 0, 100))
                cv2.imwrite(two_up+ "/FRAMES/" + str(time.clock())+".jpg", im)                    
        
        return violatedPointsData

    # def getStringFromPoints(self, points):
    #     pointString = ''
    #     for point in points:
    #         mainString = str(point[0])+' '+str(point[1])
    #         if(len(pointString) != 0):
    #             pointString = pointString+','+mainString
    #         else:
    #             pointString = mainString
    #     return pointString

    # def editDatabase(self, data):
    #     for name, coords in data.items():
    #         pointsString = self.getStringFromPoints(coords)
    #         self.db.reconnect()
    #         query = """UPDATE """+self.databaseName + """
    #                 SET 
    #                     coordinates=%s,
    #                     process_flag=1
    #                 WHERE 
    #                     frameID=%s"""
    #         values = (pointsString, name)
    #         self.cursor.execute(query, values)
    #     self.db.commit()


# if __name__ == "__main__":
#     # local
#     # model=Predict(True)
#     # imageNames=model.getNames()
#     # if(len(imageNames)>10):
#     #     prediction=model.predict_local(imageNames)
#     #     model.editDatabase(prediction)

#     # api
#     model = Predict(False)
#     imageNames = model.getNames()
#     prediction = model.predict_api(imageNames)
#     # model.editDatabase(prediction)
#     print(prediction)


# locks = []
csv_didnt_open={}
def startOnePrediction():
    global csv_didnt_open
    # print("LAMBDA NUMBER")
    # print (lambda_number)
    # print("A")
    model=Predict(True)
    while True:
        starttime = time.clock()
        # num_img = len(imageNamesBuffer)
        # if (num_img > min_batch_size):
            # imageNames = imageNamesBuffer[0:min(batch_size, num_img)]
            # del imageNamesBuffer[0:min(batch_size, num_img)]
            # print(imageNames)
        im, prediction=model.predict_local()
        # model.editDatabase(prediction)
        print("LAMBDA "+" PREDICTION")
        if('message' in prediction and 'Internal server error' in prediction['message']):
            print("Error")
        else: 
            # print(prediction)
            violatedPoints=model.processData(im, prediction)
            print(violatedPoints)
            csv_name=str(datetime.datetime.now().day).zfill(2)+str(datetime.datetime.now().month).zfill(2)+str(datetime.datetime.now().year).zfill(2)
            csv_name = two_up + "/DATA/"+csv_name
            if(os.path.exists(csv_name+'.csv')):
                try:
                    data=pd.read_csv(csv_name+'.csv')
                    for frameID,points in violatedPoints.items():
                        if(len(points)!=0):
                            new_row = pd.Series(data={'cameraID': 'A'+frameID[0:6],'frameID': 'A'+frameID,'points': points})
                            data = data.append(new_row, ignore_index=True)
                    if(len(csv_didnt_open)!=0):
                        for frameID,points in csv_didnt_open.items():
                            if(len(points)!=0):
                                new_row = pd.Series(data={'cameraID': 'A'+frameID[0:6],'frameID': 'A'+frameID,'points': points})
                                data = data.append(new_row, ignore_index=True)
                        csv_didnt_open={}
                    if(len(data)!=0):
                        data.to_csv( csv_name+'.csv',index=False)
                except:
                    print("Couldn't open csv "+str(len(csv_didnt_open)))
                    csv_didnt_open.update(violatedPoints)
            else:
                emptyData={
                    'cameraID': [],
                    'frameID': [],
                    'points': []
                }
                data = pd.DataFrame(emptyData, index=[])
                # data.to_csv( csv_name+'.csv',index=False)
                for frameID,points in violatedPoints.items():
                    if(len(points)!=0):
                        new_row = pd.Series(data={'cameraID': 'A'+frameID[0:6],'frameID': 'A'+frameID,'points': points})
                        data = data.append(new_row, ignore_index=True)
                if(len(data)!=0):
                    data.to_csv( csv_name+'.csv',index=False)
        
        print(time.clock() - starttime)
    # transformation.beginTransformation(updateIndex)
    # lockobject.release()

# def create_thread(img_names, lambda_number):
#     _thread.start_new_thread(startOnePrediction, (img_names, lambda_number))

# num_lambda = 3
batch_size = 2
min_batch_size = 1
# def beginPrediction(shared_images):
    # global locks
    # model=Predict(True)
    # num_lambda=model.numberOfLambda
    # thread_buffers = [[]]*num_lambda
    # for i in range(num_lambda):
        # create_thread(thread_buffers[i], i)

    # while True:
        # len_img = len(shared_images)
        # print("IMAGE NAMES")
        # print(shared_images)
startOnePrediction()
        # for i in range(num_lambda):
            # thread_buffers[i].extend(shared_images[int(i*(len_img/num_lambda)):int((i+1)*(len_img/num_lambda))])

