import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)
success, img = cap.read()

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0



def flex(angle1,angle2):
    per1 = np.interp(angle1, (30, 160), (0, 100))
    per2 = np.interp(angle2, (30, 160), (0, 100))
    avg = (per1 + per2) / 2

    return int(avg)

def standing_crunch(dist1, dist2):

    count = 0
    dir = 0
    max1 = 0
    max2 = 0
    avg = 0
    color = (255, 0, 255)

    per1 = np.interp(dist1, (10, 20), (0, 100))
    if per1 >= max1:
        max1 = per1
    per2 = np.interp(dist2, (10, 20), (0, 100))
    if per2 >= max2:
        max2 = per2


    if per1 == 50:
        color = (0, 255, 0)
        if dir == 0:
            count += 0.5
            dir = 1

    if per2 == 50:
        color = (0, 255, 0)
        if dir == 1:
            count += 0.5
            dir = 0


            avg = (max1 + max2) / 2
    return int(avg), count


while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    # img = cv2.imread("AiTrainer/test.jpg")
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        # Right Arm
        angle1 = detector.findAngle(img,12,14,16)
        #Left Arm
        angle2 = detector.findAngle(img,15,13,11)
        #Right Shoulder
        angle3 = detector.findAngle(img,14,12,24)
        #Left Shoulder
        angle4 = detector.findAngle(img,13,11,23)
        #Right Hip
        angle5 = detector.findAngle(img,12,24,26)
        #Left Hip
        angle6 = detector.findAngle(img,11,23,25)
        #Right Knee
        angle7 = detector.findAngle(img,23,25,27)
        #Left Knee
        angle8 = detector.findAngle(img,24,26,28)

        distance = detector.get_distance_by_names(14,25)
        distance2 = detector.get_distance_by_names(13,26)

        #Percentages

        #Bars


        # Conditional
        color = (255, 0, 255)
        # if per1 == 100 and per2 == 100:
        #     color = (0, 255, 0)
        #     if dir == 0:
        #         count += 0.5
        #         dir = 1
        #
        # if per1 == 0 and per2 == 0:
        #     color = (0, 255, 0)
        #     if dir == 1:
        #         count += 0.5
        #         dir = 0


        val, count = standing_crunch(distance,distance2)
        print(val)
        # Draw Bar
        # cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        # cv2.rectangle(img, (1100, int(bar1)), (1175, 650), color, cv2.FILLED)
        # cv2.putText(img, f'{int(per1)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
        #             color, 4)
        # cv2.rectangle(img, (500, 100), (600, 650), color, 3)
        # cv2.rectangle(img, (500, int(bar2)), (600, 650), color, cv2.FILLED)
        # cv2.putText(img, f'{int(per2)} %', (500, 75), cv2.FONT_HERSHEY_PLAIN, 4,
        #             color, 4)
        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)