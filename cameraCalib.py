import numpy as np
import cv2
import yaml
#from cv2 import aruco
from math import sqrt

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
# ARUCO Board used for finding Intrinstics
#aruco_board = cv2.aruco.GridBoard_create(5, 7, 2.3, 0.5, aruco_dict)


class CameraCalibration:

    def __init__(self):
        self.aruco_ids = []
        self.aruco_corners = [[]]
        self.arucoLength = 0.0  # in cm
        self.worldRatio = 0.0  # in cm
        self.topViewTransform = None
        self.calibrationDone = 0
        self.calibData = {}
        self.noOfFrames = 0
        self.prevArucoCorners = []
        self.arucoFixed = 1
        self.calibrationLEDStatus = 0

    def drawGroundPlane(self, img):
        if(self.topViewTransform is None):
            return None

        src_Points = np.array([[[300, 450], [650, 450], [650, 700], [300, 700]]], dtype=np.float32)
        invTransform = np.linalg.inv(self.topViewTransform)
        dst_points = cv2.perspectiveTransform(src_Points, invTransform)

        #dst_points_2 = np.array([[[dst_points[0][0][1], dst_points[0][0][0]], [dst_points[0][1][1], dst_points[0][1][0]], [dst_points[0][2][1], dst_points[0][2][0]], [dst_points[0][3][1], dst_points[0][3][0]]]])

        print(dst_points)

        overlay = np.copy(img)
        output = np.copy(img)
        cv2.fillConvexPoly(overlay, dst_points[0].astype('int32'), (255, 255, 255))

        cv2.addWeighted(overlay, 0.5, output, 0.5, 0, output)

        return output


    # function to detect aruco markers
    def detectMarkers(self, img):
        corners, ids, _ = cv2.aruco.detectMarkers(img, aruco_dict)
        return (corners, ids)

    # function to find top view transform using aruco corners
    def findTopViewTransform(self, img):
        sum_arr = []
        for i in range(0, 4):
            sum_arr.append(
                int(self.aruco_corners[0][0][i][0] + self.aruco_corners[0][0][i][1]))

        top_left_index = 0
        min_val = img.shape[0] + img.shape[1]

        for i, val in enumerate(sum_arr):
            if val < min_val:
                min_val = val
                top_left_index = i

        top_right_index = (
            top_left_index + 1) if ((top_left_index + 1) < 4) else (top_left_index + 1 - 4)
        bottom_right_index = (
            top_left_index + 2) if ((top_left_index + 2) < 4) else (top_left_index + 2 - 4)
        bottom_left_index = (
            top_left_index + 3) if ((top_left_index + 3) < 4) else (top_left_index + 3 - 4)

        pts_src = np.array((self.aruco_corners[0][0][top_left_index], self.aruco_corners[0][0][top_right_index], self.aruco_corners[0][0][bottom_right_index], self.aruco_corners[0][0][bottom_left_index]), dtype="float32")

        pts_dst = np.array(
            [[450, 550], [500, 550], [500, 600], [450, 600]],
            dtype="float32")

        trform = cv2.getPerspectiveTransform(pts_src, pts_dst)
        self.topViewTransform = trform

    # function to find top view of image
    def findTopView(self, img):
        if(self.topViewTransform is None):
            return None
        else:
            size = (1000, 1000)
            topView = np.zeros(size, dtype='uint8')
            topView = cv2.warpPerspective(img, self.topViewTransform, size)
            return topView

    # function to find worldRatio using topViewTransform matrix
    def findWorldRatio(self):
        self.worldRatio = (self.arucoLength ** 2) / (50 * 50)
        self.worldRatio = sqrt(self.worldRatio)

    def calibration(self, img):
        self.findTopViewTransform(img)
        self.findWorldRatio()

        if (self.worldRatio != 0):
            self.calibrationDone = 1
        else:
            self.calibrationDone = 0
            return 0
        return 1

    # function to calibrate camera
    def calibrate(self, img, arucoLength):
        self.arucoLength = arucoLength
        self.aruco_corners, self.aruco_ids = self.detectMarkers(img)
        if(not(self.aruco_ids is None)):
            if(len(self.aruco_ids) > 0):

                self.calibrationLEDStatus = 1

                if(self.noOfFrames == 0):
                    self.prevArucoCorners = []
                    self.prevArucoCorners.append(self.aruco_corners[0][0][0])
                    self.prevArucoCorners.append(self.aruco_corners[0][0][1])
                    self.prevArucoCorners.append(self.aruco_corners[0][0][2])
                    self.prevArucoCorners.append(self.aruco_corners[0][0][3])
                    self.prevArucoCorners = np.array(self.prevArucoCorners)
                else:
                    currentArucoCorners = []
                    currentArucoCorners.append(self.aruco_corners[0][0][0])
                    currentArucoCorners.append(self.aruco_corners[0][0][1])
                    currentArucoCorners.append(self.aruco_corners[0][0][2])
                    currentArucoCorners.append(self.aruco_corners[0][0][3])
                    currentArucoCorners = np.array(currentArucoCorners)

                    diffInPosition = currentArucoCorners - self.prevArucoCorners
                    # print(diffInPosition)

                    is_stable_1 = np.all((diffInPosition <= 5))
                    is_stable_2 = np.all((diffInPosition >= -5))
                    if(not (is_stable_1 and is_stable_2)):
                        self.noOfFrames = 0
                        self.arucoFixed = 0
                        self.calibrationLEDStatus = 0
                    else:
                        self.arucoFixed = 1
                        self.calibrationLEDStatus = 1

                    if(self.noOfFrames >= 5):
                        self.arucoFixed = 1
                        self.calibrationLEDStatus = 1
                        if(self.calibration(img)):
                            print("Calibration Done")
                            self.calibrationLEDStatus = 2
                            return 1
                        else:
                            self.calibrationLEDStatus = 0
                            return 0

                self.noOfFrames = self.noOfFrames + 1
            else:
                self.calibrationDone = 0
                self.calibrationLEDStatus = 0
                # print("ARUCO NOT DETECTED!")
                return 0
        else:
            self.calibrationDone = 0
            self.calibrationLEDStatus = 0
            # print("ARUCO NOT DETECTED!")
            return 0