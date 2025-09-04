from handtracking import *
import cv2
import time
from music import *
from faceRecognize import *

cap = cv2.VideoCapture(0)
tracker = HandTracker()
m = Music()
recognizer = FaceRecognition()

pTime = 0
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
min_vol, max_vol, _ = volume.GetVolumeRange()
vol_bar = 0
vol_per = 0


def hand_gesture(name):
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
            # cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            lx, ly = 550, 400
            rx, ry = 80, 400
            cx, cy = (rx + lx) // 2, (ry + ly) // 2
            c1_x, c1_y = cx - 60, cy
            c2_x, c2_y = cx + 60, cy
            c_x, c_y = (x1 + x2) // 2, (y1 + y2) // 2

            if y1 < y2 and y1 < y3 and y2 < y3:  # Thumbs up
                cv2.putText(frame, 'Resume', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                            1, (255, 0, 0), 3)
                m.resume()

            elif x2 in range(0, 700) and y2 in range(250, 501):
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

                if x2 in range(rx, cx):
                    cv2.line(frame, (x2, y2), (rx, ry), (0, 255, 0), 3)
                    if length_r >= length_c1 and length_r <= length_c:
                        cv2.putText(frame, 'Next Music', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                                    1, (255, 0, 0), 3)

                        m.go_next(name=name)
                elif x2 in range(cx, lx):
                    cv2.line(frame, (x2, y2), (lx, ly), (0, 255, 0), 3)
                    if length_y >= length_c2:
                        cv2.putText(frame, 'Previous Music', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                                    1, (255, 0, 0), 3)
                        m.go_previous(name=name)

            elif y1 > y2 and y1 > y3 and y1 > y4 and y1 > y5 and y2 > y3 and y2 < y5 and y5 > y3 and y5 > y4:
                # Normal hand
                cv2.putText(frame, 'Pause', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                            1, (255, 0, 0), 3)
                m.pause_music()

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
                cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
                cv2.rectangle(frame, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, f'{int(vol_per)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                            1, (255, 0, 0), 3)
                # HAND RANGE : 10 - 180

        cv2.putText(frame, f'[Playing: {m.music_list[m.count]}]', (150, 400), cv2.FONT_HERSHEY_COMPLEX,
                        0.5, (0, 0, 255), 2)
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    name = recognizer.Recognizer()
    m.play_music(name=name)
    hand_gesture(name=name)
    # input_thread = threading.Thread(target=hand_gesture(name))
    # continue_thread = threading.Thread(target=continue_music)
    # input_thread.daemon = True
    # input_thread.start()

    # while not exit_requested:
    #     for event in pygame.event.get():
    #         if event.type == pygame.USEREVENT:
    #             m.count += 1
    #             mixer.music.load(f"./{name}/{m.music_list[m.count]}")
    #             mixer.music.play()
    # continue_thread.start()

    # input_thread.join()
    # continue_thread.join()
