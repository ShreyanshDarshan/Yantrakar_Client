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

# passFile = open("pass.txt","r")
# mysql_pass = passFile.readline()
# passFile.close()

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
            im = Image.open("./FRAMES/" + name + self.image_extension)
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

        api_endpoint = "https://edh5g0f8h3.execute-api.ap-south-1.amazonaws.com/default/mxnet4"

        headers = {'content-encoding': 'gzip'}

        res = requests.post(url=api_endpoint, data=temp, headers=headers)

        print(time.time()-start)

        return res.content

    def read_pics_local(self, img_names):
        imgs = []
        # print (img_names)
        for name in img_names:
            # if os.path.isfile('./FRAMES/'+name[0]+self.image_extension) :
            im = Image.open(
                './FRAMES/'+name+self.image_extension)
            im = (np.array(im)).reshape(256, 256, 3)
            imgs.append(im)

        imgs = np.stack(imgs, axis=0)

        return mx.nd.array(imgs)

    def get_model(self):
        net = gluon.nn.SymbolBlock.imports("new_ssd_512_mobilenet1.0_voc-symbol.json", [
                                           'data'], "new_ssd_512_mobilenet1.0_voc-0000.params", ctx=self.ctx)
        return net

    def predict_local(self, img_names):

        x = self.read_pics_local(img_names)

        # net = self.get_model() 

        idx, prob, bbox = self.net(x)
        idx = idx.asnumpy()
        prob = prob.asnumpy()
        bbox = bbox.asnumpy()
        detection = idx.shape[1]
        pred = {}

        for i in range(len(img_names)):
            ctr = 0
            temp = []
            for k in range(detection):
                if idx[i][k][0] == 14.0 and ctr < 10 and prob[i][k][0] >= 0.4:
                    ctr += 1
                    cords = bbox[i][k].tolist()
                    temp.append((int((cords[0]+cords[2])/2), int(cords[3])))

            pred.update({img_names[i]: temp})

        return pred

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
        
    def processData(self,coordinates):
        violatedPointsData={}
            
        for frameID, dbData in coordinates.items():
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
            violatedPointsData.update({
                frameID: violatedPoints
            })

        # DELETE FILES
        for frameID,violatedPoints in violatedPointsData.items():
            if(len(violatedPoints)==0):
                deleteFile=frameID+self.image_extension
                os.remove('./FRAMES/'+deleteFile) 
        
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


locks = []

def startOnePrediction(imageNamesBuffer, lambda_number):
    # print("LAMBDA NUMBER")
    # print (lambda_number)
    # print("A")
    while True:
        num_img = len(imageNamesBuffer)
        if (num_img > min_batch_size):
            imageNames = imageNamesBuffer[0:min(batch_size, num_img)]
            del imageNamesBuffer[0:min(batch_size, num_img)]
            print(imageNames)
            model=Predict(True)
            prediction=model.predict_local(imageNames)
            # model.editDatabase(prediction)
            print("LAMBDA "+str(lambda_number)+" PREDICTION")
            if('message' in prediction and 'Internal server error' in prediction['message']):
                print("Error")
            print(prediction)
            violatedPoints=model.processData(prediction)
            print(violatedPoints)
    # transformation.beginTransformation(updateIndex)
    # lockobject.release()

def create_thread(img_names, lambda_number):
    # Create a lock and acquire it
    # a_lock = _thread.allocate_lock()
    # a_lock.acquire()

    # Store it in the global locks list
    # locks.append(a_lock)

    # Pass it to the newly created thread which can release the lock once done
    _thread.start_new_thread(startOnePrediction, (img_names, lambda_number))

num_lambda = 2
batch_size = 2
min_batch_size = 1
def beginPrediction(shared_images):
    global locks
    model=Predict(True)
    thread_buffers = [[]]*num_lambda
    for i in range(num_lambda):
        create_thread(thread_buffers[i], i)

    while True:
        len_img = len(shared_images)
        # print("IMAGE NAMES")
        # print(shared_images)
        for i in range(num_lambda):
            thread_buffers[i].extend(shared_images[int(i*(len_img/num_lambda)):int((i+1)*(len_img/num_lambda))])
        # imageNames=model.getNames()
        del shared_images[0:int(num_lambda*(len_img/num_lambda))]
        
        # if(len(imageNames)>=batch_size*num_lambda and imageNames):
            # locks=[]
            # print (imageNames)

            # Acquire all the locks, which means all the threads have released the locks
            # all(lock.acquire() for lock in locks)
            
if __name__ == "__main__":
    beginPrediction()
        

