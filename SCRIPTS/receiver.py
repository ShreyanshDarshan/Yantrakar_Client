import cv2

cap = cv2.VideoCapture('http://0.0.0.0:5000/video_feed')

while True:
    ret,frame= cap.read()
    if ret:
        cv2.imshow("w1",frame)
    cv2.waitKey(10)
