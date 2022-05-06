import cv2
import pickle

width, height = 90, 45  # 325-235, 235-190

try:
    with open("CarParkPos", "rb") as f:  # write binary
        pos_list = pickle.load(f)
except Exception:
    pos_list = []


def mouse_click(events, x, y, flags, params):

    if events == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for idx, pos in enumerate(pos_list):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                pos_list.pop(idx)

    with open("CarParkPos", "wb") as f:  # write binary
        pickle.dump(pos_list, f)


while True:
    img = cv2.imread("Parking.PNG")
    for pos in pos_list:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
    # cv2.rectangle(img, (235,190), (325,235), (255,0,255), 2)
    cv2.imshow("frame", img)
    cv2.setMouseCallback("frame", mouse_click)

    if cv2.waitKey(1) == ord("q"):
        break
