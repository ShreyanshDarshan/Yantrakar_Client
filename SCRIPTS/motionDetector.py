import numpy as np
import cv2

class MotionDetector():

    def __init__(self):

        #self.sdThresh = 9.0
        self.sdThreshMax = 27
        self.k = 5
        self.framesList = []

    def distMap(self, frame1, frame2):
        """outputs pythagorean distance between two frames"""
        # frame1_32 = np.float32(frame1)
        # frame2_32 = np.float32(frame2)
        # diff32 = frame1_32 - frame2_32
        # norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
        # norm32 = np.sqrt(diff32[:, :] ** 2) / np.sqrt(255 ** 2)
        # dist = np.uint8(norm32 * 255) 
        dst = cv2.absdiff(frame1, frame2)
        # norm32 = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        # dist = np.uint8(norm32)
        return dst

    def detect(self, frame, sdThresh=0):

        new_width = int(480)
        new_height = int((frame.shape[0] / frame.shape[1]) * new_width)

        frame = cv2.resize(frame, (new_width, new_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        avg_dev = 0

        if(len(self.framesList)):


            thresh = None
            for i in range(0, self.k):
                dist = self.distMap(self.framesList[i], frame)

                mod = cv2.GaussianBlur(dist, (3, 3), 0)
                # apply thresholding
                _, thresh = cv2.threshold(mod, 100, 255, 0)
                #cv2.imshow('thresh', thresh)
                # calculate st dev test
                _, stDev = cv2.meanStdDev(mod)
                avg_dev = avg_dev + stDev
                if (i < self.k - 1):
                    self.framesList[i] = self.framesList[i + 1]

            self.framesList[self.k - 1] = frame
            avg_dev = avg_dev / self.k

            thresh = cv2.putText(thresh, "Deviation: " + str(avg_dev[0][0]), (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255), 2)

            if(avg_dev > sdThresh and avg_dev < self.sdThreshMax):
                thresh = cv2.putText(thresh, "Motion Detected", (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255), 2)
                return 1, thresh
            else:
                thresh = cv2.putText(thresh, "Motion not Detected", (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255), 2)
                return 0, thresh

        else:
            for i in range(0, self.k):
                self.framesList.append(frame)

        return 0, None

#detector = MotionDetector()

#cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

#cap = cv2.VideoCapture(0)

#import time

#count = 0
#start = time.time()

#while(True):
#    ret, frame = cap.read()
#    if (ret == False):
#        break
#    detector.detect(frame)
    # if detector.detect(frame):
            # print("Motion detected..")
#    count+=1
#    cv2.imshow('frame', frame)
#    if cv2.waitKey(1) & 0xFF == 27:
#        break

#print (count/(time.time() - start))
#cap.release()
#cv2.destroyAllWindows()