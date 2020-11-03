import cv2
import time
from mxnet import gluon
from flask import Flask, render_template, Response, jsonify, request
import numpy as np
import mxnet as mx
from random import randint

app = Flask(__name__)
global_frame = None
ctx = mx.gpu() if mx.context.num_gpus() else mx.cpu()
net = gluon.nn.SymbolBlock.imports("new_ssd_512_mobilenet1.0_voc-symbol.json", [
                                           'data'], "new_ssd_512_mobilenet1.0_voc-0000.params", ctx=ctx)

def predict(frame):
    global net
    imgs = []
    im = (np.array(frame)).reshape(1200, 256, 3)
    imgs.append(im)
    imgs = np.stack(imgs, axis=0)
    x=mx.nd.array(imgs)
    # net = self.get_model() 

    idx, prob, bbox = net(x)
    idx = idx.asnumpy()
    prob = prob.asnumpy()
    bbox = bbox.asnumpy()
    detection = idx.shape[1]
    # pred = {}

    ctr = 0
    # temp = []
    for k in range(detection):
        if idx[0][k][0] == 14.0 and ctr < 10 and prob[0][k][0] >= 0.4:
            ctr += 1
            # cords = bbox[i][k].tolist()
            # temp.append((int((cords[0]+cords[2])/2), int(cords[3])))

    return ctr

def video_stream():
    global global_frame

    cap = cv2.VideoCapture(0)
    isFirst=True

    while True:
        ret, frame1 = cap.read()
            
        if ret:
            count=predict(frame1)
            count = randint(0, 10)
            if isFirst:
                isFirst=False
                ret, jpeg = cv2.imencode('.jpg', frame1)
                frame = jpeg.tobytes()
            if(count>7):
                print(count)
                ret, jpeg = cv2.imencode('.jpg', frame1)
                frame = jpeg.tobytes()
        else:
            frame = None

        # frame streaming part
        if frame != None:
            global_frame = frame
            # length=len(frame)
            yield (b'--frame\r\n'
                   b'Content-Type:image/jpeg\r\n'
                   b'Content-Length: ' + str(len(frame)).encode() + b'\r\n'
                   b'\r\n' + frame + b'\r\n')

        else:
            yield (b'--frame\r\n'
                   b'Content-Type:image/jpeg\r\n'
                   b'Content-Length: ' + str(len(global_frame)).encode() + b'\r\n'
                   b'\r\n' + global_frame + b'\r\n')
        cv2.waitKey(10)


@app.route('/video_feed')
# This is the video streaming Route. Used in src attribute of image tag in HTML
# To stream the video
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False, threaded=True, use_reloader=False)