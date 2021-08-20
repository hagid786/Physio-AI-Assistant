import cv2
import mediapipe as mp
import time
import math
import numpy as np

class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
                                     self.detectionCon, self.trackCon)



    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def get_distance_by_names(self, p1, p2):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]

        res = np.sqrt((x2-x1)^2 + (y1-y2)^2)
        return res

    # def get_distance(self, lmk_from, lmk_to):
    #     return int(lmk_to) - int(lmk_from)


    def findAngle(self, img, p1, p2, p3, draw=True):

        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        # x4, y4 = self.lmList[p4][1:]
        # x5, y5 = self.lmList[p5][1:]
        # x6, y6 = self.lmList[p6][1:]
        # x7, y7 = self.lmList[p7][1:]
        # x8, y8 = self.lmList[p8][1:]
        # x9, y9 = self.lmList[p9][1:]
        # x10, y10 = self.lmList[p10][1:]
        # x11, y11 = self.lmList[p11][1:]
        # x12, y12 = self.lmList[p12][1:]


        # Calculate the Angle
        '''right elbow'''
        angle1 = math.degrees(math.atan2(y1 - y2, x1 - x2) -
                             math.atan2(y3 - y2,x3 - x2))
        # '''left elbow'''
        # angle2 = math.degrees(math.atan2(y6 - y5, x6 - x5) -
        #                      math.atan2(y4 - y5, x4 - x5))
        # '''right shoulder'''
        # angle3 = math.degrees(math.atan2(y2 - y1, x2 - x1) -
        #                      math.atan2(y7 - y1, x7 - x1))
        # '''left shoulder'''
        # angle4 = math.degrees(math.atan2(y8 - y4, x8 - x4) -
        #                        math.atan2(y5 - y4, x5 - x4))
        # '''right hip'''
        # angle5 = math.degrees(math.atan2(y9 - y7, x9 - x7))-90
        # '''left hip'''
        # angle6 = math.degrees(math.atan2(y4 - y8, x4 - x8) +
        #                      math.atan2(y10 - y8, x10 - x8))
        # '''right knee'''
        # angle7 = math.degrees(math.atan2(y3 - y2, x3 - x2) -
        #                      math.atan2(y1 - y2, x1 - x2))
        # '''left knee'''
        # angle8 = math.degrees(math.atan2(y3 - y2, x3 - x2) -
        #                      math.atan2(y1 - y2, x1 - x2))

        if angle1 > 180:
            angle1 = 360 - angle1
        # if angle2 > 180:
        #     angle2 = 360 - angle2
        # if angle3 > 180:
        #     angle3 = 360 - angle3
        # if angle4 > 180:
        #     angle4 = 360 - angle4
        # if angle5 > 180:
        #     angle5 = 360 - angle5
        # if angle6 > 180:
        #     angle6 = 360 - angle6
        # if angle7 > 180:
        #     angle7 = 360 - angle7
        # if angle8 > 180:
        #     angle8 = 360 - angle8

        # print(math.degrees((math.atan2(y7 - y9, x7 - x9))))

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(abs(int(angle1))), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            # cv2.line(img, (x4, y4), (x5, y5), (255, 255, 255), 3)
            # cv2.line(img, (x6, y6), (x5, y5), (255, 255, 255), 3)
            # cv2.circle(img, (x4, y4), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x4, y4), 15, (0, 0, 255), 2)
            # cv2.circle(img, (x5, y5), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x5, y5), 15, (0, 0, 255), 2)
            # cv2.circle(img, (x6, y6), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x6, y6), 15, (0, 0, 255), 2)
            # cv2.putText(img, str(abs(int(angle2))), (x5 - 50, y5 + 50),
            #             cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            #
            # cv2.line(img, (x1, y1), (x7, y7), (255, 255, 255), 3)
            # cv2.circle(img, (x7, y7), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x7, y7), 15, (0, 0, 255), 2)
            # # cv2.circle(img, (x5, y5), 10, (0, 0, 255), cv2.FILLED)
            # # cv2.circle(img, (x5, y5), 15, (0, 0, 255), 2)
            # # cv2.circle(img, (x6, y6), 10, (0, 0, 255), cv2.FILLED)
            # # cv2.circle(img, (x6, y6), 15, (0, 0, 255), 2)
            # cv2.putText(img, str(abs(int(angle3))), (x1 - 50, y1 + 50),
            #             cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            #
            # cv2.line(img, (x4, y4), (x8, y8), (255, 255, 255), 3)
            # cv2.circle(img, (x8, y8), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x8, y8), 15, (0, 0, 255), 2)
            # cv2.putText(img, str(abs(int(angle4))), (x4 - 50, y4 + 50),
            #             cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            #
            # cv2.line(img, (x7, y7), (x9, y9), (255, 255, 255), 3)
            # cv2.circle(img, (x9, y9), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x9, y9), 15, (0, 0, 255), 2)
            # cv2.putText(img, str(abs(int(angle5))), (x7 - 50, y7 + 50),
            #             cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            #
            # cv2.line(img, (x8, y8), (x10, y10), (255, 255, 255), 3)
            # cv2.circle(img, (x10, y10), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x10, y10), 15, (0, 0, 255), 2)
            # cv2.putText(img, str(abs(int(angle6))), (x8 - 50, y8 + 50),
            #             cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            #
            # cv2.line(img, (x9, y9), (x11, y11), (255, 255, 255), 3)
            # cv2.circle(img, (x11, y11), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x11, y11), 15, (0, 0, 255), 2)
            # cv2.putText(img, str(abs(int(angle7))), (x9 - 50, y9 + 50),
            #             cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            #
            # cv2.line(img, (x10, y10), (x12, y12), (255, 255, 255), 3)
            # cv2.circle(img, (x12, y12), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x12, y12), 15, (0, 0, 255), 2)
            # cv2.putText(img, str(abs(int(angle8))), (x10 - 50, y10 + 50),
            #             cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            return angle1




def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:

            cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()