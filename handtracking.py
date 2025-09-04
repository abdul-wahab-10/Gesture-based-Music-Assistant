import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np


class HandTracker:
    
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

        # Initialize MediaPipe Drawing
        self.mp_drawing = mp.solutions.drawing_utils

        # # Open a webcam or video source
        # cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or provide the path to a video file
        self.devices = AudioUtilities.GetSpeakers()

        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        # volume = AudioUtilities.GetSpeakers()[0]

        self.min_vol, self.max_vol, _ = self.volume.GetVolumeRange()

    def findhands(self, img):
        # Convert the frame to RGB format (required by MediaPipe)
        frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the frame to detect hands
        self.results = self.hands.process(frame_rgb)

        # Draw landmarks and connections on the frame
        if self.results.multi_hand_landmarks:
            for landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(img, landmarks, self.mp_hands.HAND_CONNECTIONS)

        return img

    def findposition(self, img, handNo=0, draw=True):

        lmlist = []

        if self.results.multi_hand_landmarks:

            myhand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmlist

    # while True:
    #     # Read a frame from the webcam/video source
    #     ret, frame = cap.read()
    #     if not ret:
    #         break

    #     # Display the frame with landmarks and connections
    #     cv2.imshow('Hand Tracking', frame)
    #
    #     # Break the loop when the 'q' key is pressed
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #
    # # Release the video capture object and close the OpenCV window
    # cap.release()
    # cv2.destroyAllWindows()

    def runner(self):
        tracker = HandTracker()
        
        while True:
            _, frame = self.cap.read()
    
            img = tracker.findhands(frame)
            lmlist = tracker.findposition(img, draw=False)
            if len(lmlist) != 0:
                # print(lmlist[4])
    
                x1, y1 = lmlist[4][1], lmlist[4][2]
                x2, y2 = lmlist[8][1], lmlist[8][2]
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
                print(length)
    
                if length < 23:
                    cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

            cv2.imshow("Img", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
