import cv2
import time
import numpy as np
import mediapipe as mp
from handtracking import *
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from music import *


class Runner:
    def __init__(self):

        self.wCam, self.hCam = 640, 480
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.wCam)
        self.cap.set(4, self.hCam)
        self.pTime = 0

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.min_vol, self.max_vol, _ = self.volume.GetVolumeRange()

    def run(self):
        tracker = HandTracker()
        # m = Music()
        # m.play_music(name="awwab")

        while True:
            _, frame = self.cap.read()
            img = tracker.findhands(frame)
            lmList = tracker.findposition(img, draw=False)
            if len(lmList) != 0:

                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                length = math.hypot(x2 - x1, y2 - y1)

                # HAND RANGE : 8 - 150
                # VOL RANGE : -65 - 0

                vol = np.interp(length, [8, 150], [self.min_vol, self.max_vol])
                self.volume.SetMasterVolumeLevel(vol, None)
                # print(length)

                if length < 23:
                    cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

                cTime = time.time()
                fps = 1 / (cTime - self.pTime)
                self.pTime = cTime

                cv2.putText(img, f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                            1, (255, 0, 0), 3)

            cv2.imshow("Image", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    runner = Runner()
    runner.run()
