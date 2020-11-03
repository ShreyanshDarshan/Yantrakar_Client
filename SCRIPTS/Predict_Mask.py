import cv2
import torch
import time
import argparse
import numpy as np
from PIL import Image
from utils import *


class Predict_Mask():
    def __init__(self, isLocal):
        if(isLocal):
            if torch.cuda.is_available():
                self.device = 'cuda:0'
            else:
                self.device = 'cpu'
            self.net = self.get_model()

        self.image_extension = ".png"

        self.feature_map_sizes = [[45, 45], [23, 23], [12, 12], [6, 6], [4, 4]]
        self.anchor_sizes = [[0.04, 0.056], [0.08, 0.11],
                             [0.16, 0.22], [0.32, 0.45], [0.64, 0.72]]
        self.anchor_ratios = [[1, 0.62, 0.42]] * 5
        self.anchors = generate_anchors(
            self.feature_map_sizes, self.anchor_sizes, self.anchor_ratios)

        self.anchors_exp = np.expand_dims(self.anchors, axis=0)

        # self.encryptionKey = b'gkmrxai04WhOcWj3EGl-2Io58Q8biOWOytdQbPhNYGU='
        # self.getSystemConfiguration()

    """
    def getSystemConfiguration(self):
        with open('userSetting.txt', 'r') as file:
            data = file.read()
        cipher = Fernet(self.encryptionKey)
        userSetting = ast.literal_eval(
            (cipher.decrypt(data.encode('utf-8'))).decode('utf-8'))
        self.activationKey = userSetting["activationKey"]
        self.apiURL = userSetting["apiURL"]
        self.numberOfLambda = userSetting["numberOfLambda"]
    """

    def read_pics_local(self, img_names):

        imgs = []
        fin_imgs = []
        # print (img_names)
        for name in img_names:
            im = cv2.imread('./FRAMES/'+name+self.image_extension)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            imgs.append(im)
            im = cv2.resize(im, (360, 360))
            im = im / 255.0
            im = im.transpose((2, 0, 1))
            fin_imgs.append(im)

        imgs_transformed = np.stack(fin_imgs, axis=0)
        imgs_transformed = torch.tensor(
            imgs_transformed).float().to(self.device)

        return imgs_transformed, imgs

    def get_model(self):
        model = torch.load('models/model360.pth')
        model.to(self.device)
        return model

    def predict_local(self, img_names):

        x, imgs = self.read_pics_local(img_names)

        y_bboxes, y_scores, = self.net.forward(x)

        y_bboxes_output = y_bboxes.detach().cpu().numpy()
        y_cls_output = y_scores.detach().cpu().numpy()

        pred = {}

        for i in range(x.shape[0]):

            height, width, _ = imgs[i].shape

            # remove the batch dimension, for batch is always 1 for inference.
            y_bboxes = decode_bbox(self.anchors_exp, y_bboxes_output)[i]
            y_cls = y_cls_output[i]

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

            pred.update({img_names[i]: temp})

        return pred


"""
pred = Predict_Mask(True)

print(pred.predict_local(["detection1",
                          "detection2",
                          "detection3"]))
"""
