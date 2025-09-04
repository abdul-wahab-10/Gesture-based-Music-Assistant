import face_recognition
from handtracking import *
import cv2

name = ""


class FaceRecognition():

    def __init__(self):

        self.cap = cv2.VideoCapture(0)

        self.known_image_1 = face_recognition.load_image_file("./images/awc.jpeg")
        self.known_encoding_1 = face_recognition.face_encodings(self.known_image_1)[0]

        self.known_image_2 = face_recognition.load_image_file("./images/nayef.jpeg")
        self.known_encoding_2 = face_recognition.face_encodings(self.known_image_2)[0]

        self.known_image_3 = face_recognition.load_image_file("./images/awwab.jpeg")
        self.known_encoding_3 = face_recognition.face_encodings(self.known_image_3)[0]

        self.known_image_4 = face_recognition.load_image_file("./images/kaif.jpeg")
        self.known_encoding_4 = face_recognition.face_encodings(self.known_image_4)[0]

        self.known_face_encodings = [self.known_encoding_1, self.known_encoding_2, self.known_encoding_3,
                                     self.known_encoding_4]
        self.known_face_names = ["awc", "nayef", "awwab", "kaif"]
        # self.devices = AudioUtilities.GetSpeakers()
        #
        # self.interface = self.devices.Activate(
        #     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        #
        # self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        # # volume = AudioUtilities.GetSpeakers()[0]
        #
        # self.min_vol, self.max_vol, _ = self.volume.GetVolumeRange()
        # print(volume.GetVolumeRange())

    def Recognizer(self):
        global name
        tracker = HandTracker()

        while True:
            _, frame = self.cap.read()

            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for face_encoding in face_encodings:

                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("Img", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

        return name
