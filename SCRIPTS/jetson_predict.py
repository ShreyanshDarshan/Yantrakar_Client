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
import torch
import argparse
from utils import *
# passFile = open("pass.txt","r")
# mysql_pass = passFile.readline()
# passFile.close()

two_up = os.path.dirname(os.path.dirname(__file__))

class Predict():
    def __init__(self, isLocal):
        # self.db = mysql.connect(
        #     host="localhost", user="root", passwd=mysql_pass, database="test")
        # self.cursor = self.db.cursor()
        # self.databaseName = "cameraDatabaseFinal"
        if(isLocal):
            self.ctx = mx.gpu() if mx.context.num_gpus() else mx.cpu()
            self.net_human = self.get_model_human()
            if torch.cuda.is_available():
                self.device = 'cuda:0'
            else:
                self.device = 'cpu'
            self.net_mask = self.get_model_mask()
        self.image_extension=".png"
        self.getDataJson()
        
        self.feature_map_sizes = [[45, 45], [23, 23], [12, 12], [6, 6], [4, 4]]
        self.anchor_sizes = [[0.04, 0.056], [0.08, 0.11],
                             [0.16, 0.22], [0.32, 0.45], [0.64, 0.72]]
        self.anchor_ratios = [[1, 0.62, 0.42]] * 5
        self.anchors = generate_anchors(
            self.feature_map_sizes, self.anchor_sizes, self.anchor_ratios)

        self.anchors_exp = np.expand_dims(self.anchors, axis=0)
        
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

    def read_pics_human(self,im):
        imgs = []
        # # print (img_names)
        # for name in img_names:
        #     # if os.path.isfile('./FRAMES/'+name[0]+self.image_extension) :
        #     im = Image.open(
        #         two_up + '/FRAMES/'+name+self.image_extension)
        
        # ret, im = self.camera.read()
        im = cv2.resize(im, (256, 256))
        cv2.imshow("lk", im) 
        im = (np.array(im)).reshape(256, 256, 3)
        imgs.append(im)
        imgs = np.stack(imgs, axis=0)

        return mx.nd.array(imgs)
    
    def read_pics_mask(self,im):

        imgs = []
        fin_imgs = []
        # print (img_names)
        # for name in img_names:
        #     im = cv2.imread('./FRAMES/'+name+self.image_extension)
        #     im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        #     imgs.append(im)
        #     im = cv2.resize(im, (360, 360))
        #     im = im / 255.0
        #     im = im.transpose((2, 0, 1))
        #     fin_imgs.append(im)

        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        # imgs.append(im)
        im = cv2.resize(im, (360, 360))
        im = im / 255.0
        im = im.transpose((2, 0, 1))
        fin_imgs.append(im)
        
        imgs_transformed = np.stack(fin_imgs, axis=0)
        imgs_transformed = torch.tensor(
            imgs_transformed).float().to(self.device)

        return imgs_transformed

    def get_model_human(self):
        net = gluon.nn.SymbolBlock.imports(two_up + "/DATA/new_ssd_512_mobilenet1.0_voc-symbol.json", [
                                           'data'], two_up + "/DATA/new_ssd_512_mobilenet1.0_voc-0000.params", ctx=self.ctx)
        return net
    
    def get_model_mask(self):
        model = torch.load('models/model360.pth')
        model.to(self.device)
        return model

    def predict_mask(im):
        x = self.read_pics_mask(im)
        y_bboxes, y_scores, = self.net_mask.forward(x)

        y_bboxes_output = y_bboxes.detach().cpu().numpy()
        y_cls_output = y_scores.detach().cpu().numpy()

        pred = {}

        # for i in range(x.shape[0]):

        height, width, _ = im.shape

        # remove the batch dimension, for batch is always 1 for inference.
        y_bboxes = decode_bbox(self.anchors_exp, y_bboxes_output)[0]
        y_cls = y_cls_output[0]

        # To speed up, do single class NMS, not multiple classes NMS.
        bbox_max_scores = np.max(y_cls, axis=1)
        bbox_max_score_classes = np.argmax(y_cls, axis=1)

        # keep_idx is the alive bounding box after nms.
        keep_idxs = single_class_non_max_suppression(y_bboxes,
                                                        bbox_max_scores,
                                                        conf_thresh=0.5,
                                                        iou_thresh=0.4,
                                                        )

        output_info_class_id = []
        output_info_conf = []
        output_info_cords = []

        for idx in keep_idxs:
            conf = float(bbox_max_scores[idx])
            class_id = bbox_max_score_classes[idx]
            bbox = y_bboxes[idx]
            # clip the coordinate, avoid the value exceed the image boundary.
            xmin = max(0, int(bbox[0] * width))
            ymin = max(0, int(bbox[1] * height))
            xmax = min(int(bbox[2] * width), width)
            ymax = min(int(bbox[3] * height), height)

            output_info_class_id.append(class_id)
            output_info_conf.append(conf)
            output_info_cords.append([xmin, ymin, xmax, ymax])

        temp = {'id': output_info_class_id,
                'prob': output_info_conf, 'bbox': output_info_cords}
            
        print(output_info_conf)
            # pred.update({img_names[i]: temp})

        return temp
    
    def predict_human(im):
        x = self.read_pics_human(im)
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
        violatedPoints=processData(im,temp)
        return violatedPoints

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

        for frameID,violatedPoints in violatedPointsData.items():
            if(len(violatedPoints)>0):
                for pointpair in violatedPoints:
                    im = cv2.line(im, pointpair[0], pointpair[1], (0, 0, 100))
                cv2.imwrite(two_up+ "/FRAMES/" + str(time.clock())+".jpg", im)                    
        
        return violatedPointsData

csv_didnt_open={}

def edit_csv(violatedPoints):
    global csv_didnt_open
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

# locks = []
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
        ret, im = model.camera.read()
        mask_points=model.predict_mask(im)
        # violatedPoints_human=model.predict_human(im)
        # model.editDatabase(prediction)
        # print("PREDICTION HUMAN")
        # print(violatedPoints_human)
        print("PREDICTION MASK")
        print(mask_points)
        # edit_csv(violatedPoints_human)
        print(time.clock() - starttime)
    # transformation.beginTransformation(updateIndex)
    # lockobject.release()

# num_lambda = 3
batch_size = 2
min_batch_size = 1
startOnePrediction()

# def create_thread(img_names, lambda_number):
#     _thread.start_new_thread(startOnePrediction, (img_names, lambda_number))

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

        # for i in range(num_lambda):
            # thread_buffers[i].extend(shared_images[int(i*(len_img/num_lambda)):int((i+1)*(len_img/num_lambda))])
        # def getNames(self):
    #     self.db.reconnect()
    #     query = """SELECT frameID
    #             FROM """ + self.databaseName + """
    #             WHERE process_flag=0
    #             ORDER BY SUBSTRING(frameID, 7) 
    #             LIMIT 6"""
    #     self.cursor.execute(query)
    #     return self.cursor.fetchall()
    
    # def read_pics_api(self, img_names):
    #     imgs = []

    #     for name in img_names:
    #         im = Image.open(two_up + "/FRAMES/" + name + self.image_extension)
    #         im = (np.array(im)).reshape(256, 256, 3)
    #         imgs.append(im)

    #     return imgs
    
    # def predict_api(self, imageNames):
    #     # """file = open('/home/karan/conv/foo.b64', 'rb')

    #     # temp = file.read()

    #     # """
    #     imgs = self.read_pics_api(imageNames)

    #     l = []

    #     print(len(imgs))

    #     for i in range(len(imgs)):

    #         dictionary = {}
    #         dictionary['name'] = imageNames[i]

    #         dictionary['data'] = [imgs[i]]

    #         l.append(dictionary)

    #     temp = pickle.dumps(l)
    #     temp = base64.b64encode(temp)
    #     temp = gzip.compress(temp)

    #     # """with open("imgs.gz", "wb") as f:
    #     #     f.write(temp)"""

    #     start = time.time()

    #     api_endpoint = self.apiURL

    #     headers = {'content-encoding': 'gzip','x-api-key':self.activationKey}

    #     res = requests.post(url=api_endpoint, data=temp, headers=headers)

    #     print(time.time()-start)

    #     return ast.literal_eval(res.content.decode('utf-8'))
    

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


