import requests
import calibrateWithoutGUI as calib
from PIL import Image
import numpy as np
import json
import pickle
import base64
import time
# import mysql.connector as mysql
# import _thread
# import threading 
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
from pygame import mixer

# import RPi.GPIO as GPIO

but_pin = 18

from vision.ssd.mobilenet import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor

two_up = os.path.dirname(os.path.dirname(__file__))

mixer.init()
soundMask= mixer.Sound(two_up + "/DATA/maskAudio.ogg")
soundDist=mixer.Sound(two_up + "/DATA/distancingAudio.ogg")

model_path = two_up + "/models/mobilenet-v1-ssd-mp-0_675.pth"
label_path = two_up + "/models/voc-model-labels.txt"
class_names = [name.strip() for name in open(label_path).readlines()]

image_area_threshold = 0.25
mask_frame_threshold = 4
mask_frame_buffer = 6 
mask_radius_thresh = 100

# two_up = '/home/yantrakaar/Yantrakar_Client'

class Predict():
    def __init__(self, isLocal):
        if(isLocal):
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
        self.camera = cv2.VideoCapture(two_up + "/test_video/mask.mp4")
        self.calibrate=calib.CalibrateWithoutGUI()
        self.calibDone=False

    def getSystemConfiguration(self):
        with open(two_up + '/DATA/userSetting.txt','r') as file:
            data=file.read()
        cipher=Fernet(self.encryptionKey)
        userSetting=ast.literal_eval((cipher.decrypt(data.encode('utf-8'))).decode('utf-8'))
        self.activationKey=userSetting["activationKey"]
        self.apiURL=userSetting["apiURL"]
        self.numberOfLambda=userSetting["numberOfLambda"]

    def read_pics_mask(self,im):

        imgs = []
        fin_imgs = []

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

        net = create_mobilenetv1_ssd(len(class_names), is_test=True)
        net.load(model_path)
        predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)
        
        return predictor
    
    def get_model_mask(self):
        model = torch.load(two_up + '/models/model360.pth')
        model.to(self.device)
        return model

    def predict_mask(self, im):
        x = self.read_pics_mask(im)
        y_bboxes, y_scores, = self.net_mask.forward(x)

        y_bboxes_output = y_bboxes.detach().cpu().numpy()
        y_cls_output = y_scores.detach().cpu().numpy()

        pred = {}
        #print(y_bboxes_output)
        #print(y_cls_output)

        # for i in range(x.shape[0]):

        height, width, _ = im.shape

        # remove the batch dimension, for batch is always 1 for inference.
        y_bboxes = decode_bbox(self.anchors_exp, y_bboxes_output)[0]
        y_cls = y_cls_output[0]

        # To speed up, do single class NMS, not multiple classes NMS.
        bbox_max_scores = np.max(y_cls, axis=1)
        bbox_max_score_classes = np.argmax(y_cls, axis=1)

        # keep_idx is the alive bounding box after nms.
        keep_idxs = single_class_non_max_suppression(   y_bboxes,
                                                        bbox_max_scores,
                                                        conf_thresh=0.5,
                                                        iou_thresh=0.5,
                                                        )

        output_info_class_id = []
        output_info_conf = []
        output_info_cords = []
        # print(keep_idxs)

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
            
        # print(output_info_conf)
        # pred.update({img_names[i]: temp})

        return temp
    
    def predict_human(self, im):
        # x = self.read_pics_human(im)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        boxes, labels, probs = self.net_human.predict(im, 10, 0.4)
        new_boxes = []
        new_labels = []
        new_probs = []

        for i in range(len(labels)):
            if labels[i] == 15:
                new_boxes.append(boxes[i, :])
                new_labels.append(15)
                new_probs.append(probs[i])
        boxes = new_boxes
        labels = new_labels
        probs = new_probs
        ctr = 0
        temp = []
        for i in range(len(boxes)):
            if ctr<10:
                ctr+=1
                box = boxes[i]
                temp.append(box) #.append((int((box[0]+box[2])/2), int(box[3])))
            # pred.update({im: temp})
        return temp

    def findWorldDistance(self, matrix, worldRatio, point1, point2):
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
        
    def processData(self, im, human_boxes, mask_points, masks_list, iter):
        violatedPointsData = {}
        dbData = []
        for box in human_boxes:
            dbData.append((int((box[0]+box[2])/2), int(box[3]), int(abs(box[2] - box[0])*abs(box[3]-box[1]))))
            cv2.rectangle(im, (box[0], box[1]), (box[2], box[3]), color=(0, 0, 0))
        
        height, width, _ = im.shape

        points = combinations(dbData, 2)
        violatedPoints = []
        distancingViolated = False
        for point1, point2 in points:
            if (point1[2]<width*height*image_area_threshold and point2[2]<width*height*image_area_threshold):
                point1_scaled = (int(point1[0] * width / 256),
                                int(point1[1] * height / 256))
                point2_scaled = (int(point2[0] * width / 256),
                                int(point2[1] * height / 256))
                distance = self.findWorldDistance(
                    self.cameraDataProcessed["000001"]["calibrationMatrix"],
                    self.cameraDataProcessed["000001"]["worldRatio"],
                    point1_scaled, point2_scaled)
                if (point1 == point2):
                    continue
                elif (distance == -1):
                    continue
                elif (distance < 150):
                    violatedPoints.append((point1_scaled, point2_scaled))
        violatedPointsData.update({"000001": violatedPoints})

        for _, violatedPoints in violatedPointsData.items():
            if (len(violatedPoints) > 0):
                distancingViolated = True
                for pointpair in violatedPoints:
                    im = cv2.line(im, pointpair[0], pointpair[1], (0, 0, 100))


        maskViolated = False
        # print(masks_list)
        if (iter != 0):
            for i, box in enumerate(mask_points['bbox']):
                id = mask_points['id']
                if (id[i] == 1):
                    for mask in masks_list:
                        if (box[0]+box[2])/2 - (mask[0]+mask[2])/2 < mask_radius_thresh and (box[1]+box[3])/2 - (mask[1]+mask[3])/2 < mask_radius_thresh:
                            for human in human_boxes:
                                if (box[0]+box[2])/2 > human[0] and (box[0]+box[2])/2 < human[2] and (box[1]+box[3])/2 > human[1] and (box[1]+box[3])/2 < human[3]:
                                    mask[0] = box[0]
                                    mask[1] = box[1]
                                    mask[2] = box[2]
                                    mask[3] = box[3]
                                    mask[4] += 1
                    cv2.rectangle(im, (box[0], box[1]), (box[2], box[3]), color=(0, 0, 255))
                else:
                    cv2.rectangle(im, (box[0], box[1]), (box[2], box[3]), color=(0, 255, 0))

        else :
            for mask in masks_list:
                if mask[4] >= mask_frame_threshold:
                    maskViolated = True
            
            masks_list.clear()
            for i, box in enumerate(mask_points['bbox']):
                id = mask_points['id']
                if (id[i] == 1):
                    for human in human_boxes:
                        if (box[0]+box[2])/2 > human[0] and (box[0]+box[2])/2 < human[2] and (box[1]+box[3])/2 > human[1] and (box[1]+box[3])/2 < human[3]:
                            masks_list.append([box[0], box[1], box[2], box[3], 0])

        # cv2.imwrite(two_up + "/FRAMES/" + str(time.process_time()) + ".jpg", im)
        cv2.imshow("out", im)
        cv2.waitKey(1)
        return maskViolated, distancingViolated, masks_list

# uncomment this for GPIO
# def checkButton():
#     value = GPIO.input(but_pin)
#     return value == GPIO.LOW

csv_didnt_open={}

def startOnePrediction():
    global soundMask, soundDist
    maskAudioDuration = 2
    distAudioDuration = 2
    isPlayingMask = False
    isPlayingDist = False
    isAudioPlaying = False
    audioTime = time.time()
    model = Predict(True)
    avg = 0
    num_imgs = 0
    masks_list = []
    iter = 0
    while True:
        # uncomment this for GPIO
        # if checkButton():
        #     placeholder_code_delete_this = 0
            # model.calibrate.runCalibration(model.camera)
        if not model.calibDone:
            model.calibrate.runCalibration(model.camera)
            model.calibDone=True
        if (iter > mask_frame_buffer):
            iter = 0
        num_imgs += 1
        starttime = time.clock()
        _, im = model.camera.read()
        mask_points={}
        mask_points = model.predict_mask(im)
        human_boxes = model.predict_human(im)
        # print("PREDICTION MASK")
        # print(mask_points)
        # print("PREDICTION HUMAN")
        # print(human_boxes)
        isMask, isDist, masks_list = model.processData(im, human_boxes,
                                           mask_points, masks_list, iter)
        if isMask and not isAudioPlaying:
            audioTime = time.time()
            isPlayingMask = True
            soundMask.play()
            isAudioPlaying = True
        if isDist and not isAudioPlaying:
            audioTime = time.time()
            isPlayingDist = True
            soundDist.play()
            isAudioPlaying = True

        if isPlayingMask and time.time()-audioTime > maskAudioDuration:
            isPlayingMask = False
            isAudioPlaying = False

        if isPlayingDist and time.time()-audioTime > distAudioDuration:
            isAudioPlaying = False
            isPlayingDist = False

        avg = avg * (num_imgs - 1) / num_imgs + 1 / (time.clock() -
                                                     starttime) / num_imgs
        # print(avg)
        iter += 1


if __name__ == "__main__":
    # uncomment this for GPIO
    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setup(but_pin, GPIO.IN)
    # try:
        # startOnePrediction()
    model=Predict(True)
    # finally:
        # GPIO.cleanup()