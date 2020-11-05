from mxnet import gluon
import mysql.connector as mysql
import mxnet as mx
from PIL import Image
# import boto3
import numpy as np
import json
import os
import time

passFile = open("pass.txt","r")
mysql_pass = passFile.readline()
passFile.close()

class Predict():
    def __init__(self):
        self.db=mysql.connect(host="localhost",user="root",passwd=mysql_pass, database="test")
        self.cursor=self.db.cursor()
        self.databaseName="cameraDatabaseFinal"
        self.ctx = mx.gpu() if mx.context.num_gpus() else mx.cpu()
        self.net=self.get_model()   
        
        self.image_extension=".png"
        
    def getNames(self):
        self.db.reconnect()
        query="""SELECT frameID
                FROM """ +self.databaseName +"""
                WHERE process_flag=0
                ORDER BY SUBSTRING(frameID, 7) 
                LIMIT 5"""
        self.cursor.execute(query)
        imageNames = self.cursor.fetchall()
        for nm in imageNames:
            if (os.path.isfile("./FRAMES/" + nm[0] + self.image_extension) == False):
                imageNames.remove(nm)
        return imageNames


    def read_pics(self,img_names):
        imgs = []

        for name in img_names:
            im = Image.open("./FRAMES/"+name[0]+self.image_extension)
            im = (np.array(im)).reshape(256, 256, 3)
            imgs.append(im)

        imgs = np.stack(imgs, axis=0)

        return mx.nd.array(imgs)


    def get_model(self):
        net = gluon.nn.SymbolBlock.imports("new_ssd_512_mobilenet1.0_voc-symbol.json", ['data'], "new_ssd_512_mobilenet1.0_voc-0000.params", ctx=self.ctx)
        return net

    def predict(self,img_names):

        x = self.read_pics(img_names)

        # net = get_model()

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

            pred.update({img_names[i][0]: temp})

        return pred
    
    def getStringFromPoints(self,points):
        pointString=''
        for point in points:
            mainString=str(point[0])+' '+str(point[1])
            if(len(pointString)!=0):
                pointString=pointString+','+mainString
            else:
                pointString=mainString
        return pointString

    def editDatabase(self,data):
        for name,coords in data.items():
            pointsString=self.getStringFromPoints(coords)
            self.db.reconnect()
            query = """UPDATE """+self.databaseName +"""
                    SET 
                        coordinates=%s,
                        process_flag=1
                    WHERE 
                        frameID=%s"""
            values=(pointsString,name)
            self.cursor.execute(query,values)
        self.db.commit()

# if __name__ == "__main__":
def beginPrediction():
    model=Predict()
    while True:
        imageNames=model.getNames()
        print (imageNames)
        if(len(imageNames)>0):
            prediction=model.predict(imageNames)
            model.editDatabase(prediction)
            print(prediction)
        # time.sleep(1)

# beginPrediction()