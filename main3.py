from handtracking import *
import cv2 as cv
# import math
import time

cap = cv.VideoCapture(0)
tracker = HandTracker()
pTime = 0
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
min_vol, max_vol, _ = volume.GetVolumeRange()
vol_bar = 0
vol_per = 0

while True:
    _, frame = cap.read()
    frame = tracker.findhands(img=frame)
    lmlist = tracker.findposition(img=frame, draw=False)
    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1], lmlist[4][2]  # For thumb tip
        x2, y2 = lmlist[8][1], lmlist[8][2]  # For Index fingertip
        x3, y3 = lmlist[12][1], lmlist[12][2]  # For Middle fingertip
        x4, y4 = lmlist[16][1], lmlist[16][2]  # For Ring fingertip
        x5, y5 = lmlist[20][1], lmlist[20][2]  # For Pinky fingertip
        lx, ly = 550, 400
        rx, ry = 80, 400
        cx, cy = (rx + lx) // 2, (ry + ly) // 2
        c1_x, c1_y = cx - 100, cy
        c2_x, c2_y = cx + 100, cy
        c_x, c_y = (x1 + x2) // 2, (y1 + y2) // 2

        # RHS RANGE: x(450-600) and y(340-500)
        # LHS RANGE: x(30-150) and y(340-500)
        if x2 in range(0, 700) and y2 in range(250, 501):
            cv2.circle(frame, (rx, ry), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (lx, ly), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(frame, (rx, ry), (lx, ly), (255, 0, 255), 3)
            cv2.circle(frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (c1_x, c1_y), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (c2_x, c2_y), 15, (255, 0, 255), cv2.FILLED)

            length_c = math.hypot(rx - cx, ry - cy)
            length_r = math.hypot(x2 - rx, y2 - ry)
            length_y = math.hypot(x2 - lx, y2 - ly)
            length_c1 = math.hypot(rx - c1_x, ry - c1_y)
            length_c2 = math.hypot(lx - c2_x, ly - c2_y)

            # if length_r >= length_c and length_y < length_c:
            #     cv2.circle(frame, (rx, ry), 15, (0, 0, 255), cv2.FILLED)
            #     cv2.circle(frame, (lx, ly), 15, (0, 0, 255), cv2.FILLED)
            #     cv2.putText(frame, 'Next Music', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
            #                     1, (255, 0, 0), 3)
            if x2 in range(rx, cx):
                cv2.line(frame, (x2, y2), (rx, ry), (0, 255, 0), 3)
                if length_r >= length_c1:
                    cv2.putText(frame, 'Next Music', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                                1, (255, 0, 0), 3)

            elif x2 in range(cx, lx):
                cv2.line(frame, (x2, y2), (lx, ly), (0, 255, 0), 3)
                if length_y >= length_c2:
                    cv2.putText(frame, 'Previous Music', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                                1, (255, 0, 0), 3)
            # if length_y >= length_c and length_r < length_c:
            #     cv2.circle(frame, (rx, ry), 15, (255, 0, 0), cv2.FILLED)
            #     cv2.circle(frame, (lx, ly), 15, (255, 0, 0), cv2.FILLED)
        # elif x2 in range(30, 151) and y2 in range(340, 501):
        #     cv2.putText(frame, 'LHS', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
        #                 1, (255, 0, 0), 3)
        elif y2 < y1 and y2 < y5 and y1 < y5:
            length_vol = math.hypot(x2 - x1, y2 - y1)
            cv2.line(frame, (x2, y2), (x1, y1), (255, 0, 255), 3)
            vol = np.interp(length_vol, [8, 150], [min_vol, max_vol])
            vol_bar = np.interp(length_vol, [8, 150], [400, 150])
            vol_per = np.interp(length_vol, [8, 150], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)

            if length_vol < 20:
                cv2.circle(frame, (c_x, c_y), 10, (255, 0, 0), cv2.FILLED)

            cv2.circle(frame, (c_x, c_y), 10, (255, 0, 255), cv2.FILLED)
            cv2.rectangle(frame,  (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(frame,  (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f'{int(vol_per)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 0, 0), 3)
            # HAND RANGE : 10 - 180
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(frame, f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 0, 0), 3)
    cv.imshow("Frame", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
