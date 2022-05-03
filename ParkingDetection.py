import cv2
import pickle
import numpy as np

width, height = 90, 45
frame = cv2.VideoCapture("Parking.mp4")

with open("CarParkPos", "rb") as f:  # write binary
    pos_list = pickle.load(f)


def checkParkingSpace(imgProz):

    free_parking_zones = 0

    for pos in pos_list:
        x, y = pos
        imgCrop = imgProz[y : y + height, x : x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 850:
            color = (0, 255, 0)
            t = 5
            free_parking_zones += 1
        else:
            color = (0, 0, 255)
            t = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, t)
    cv2.putText(img, f"Free Parking Zones: {free_parking_zones}", (50, 100), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2)


while True:

    # Number of Frames / toatal number of Frames
    if frame.get(cv2.CAP_PROP_POS_FRAMES) == frame.get(cv2.CAP_PROP_FRAME_COUNT):
        frame.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = frame.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((2, 2))
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=3)

    checkParkingSpace(imgDilate)

    cv2.imshow("img", img)
    # cv2.imshow("blur", imgBlur)
    # cv2.imshow("imgMedian", imgMedian)

    if cv2.waitKey(50) == ord("q"):
        break
