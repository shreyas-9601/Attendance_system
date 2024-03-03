import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from accounts.models import CustomUser


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        with open('media/Attendance.csv', 'r+') as f:
            f.truncate(0)
            f.writelines('Name,Time')
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        # path = 'media/images'
        users = list(CustomUser.objects.all())
        self.newmylist = {}
        print(" users = ", users)
        for user in users:
            if user.image:
                self.newmylist[user.username] = user.image.path
        # print(" newmylist = ", self.newmylist)
        self.newImages = []
        self.newClassNames = []
        for i in self.newmylist:
            cur = cv2.imread(self.newmylist[i])
            self.newImages.append(cur)
            self.newClassNames.append(i)
        # print(" newImages = ", self.newImages)
        # print(" newClassNames = ", self.newClassNames)
        # self.images = []
        # self.classNames = []
        # self.mylist = os.listdir(path)
        # print(self.mylist)
        # for i in self.mylist:
        #     self.curImg = cv2.imread(f'{path}/{i}')
        #     self.images.append(self.curImg)
        #     self.classNames.append(os.path.splitext(i)[0])
        # print(self.classNames)
        self.encodeListKnown = self.findEncodings()
        print('Encoding Complete')

    def __del__(self):
        self.video.release()

    def findEncodings(self):
        encodeList = []
        # for img in self.images:
        for img in self.newImages:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def markAttendance(self, name):
        with open('media/Attendance.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])

            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')

    def get_frame(self):
        # encodeListKnown = self.findEncodings()
        # print('Encoding Complete')
        success, img = self.video.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(
                self.encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(
                self.encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                # name = self.classNames[matchIndex].upper()
                name = self.newClassNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2),
                              (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
                # print(" Attended---", name)
                self.markAttendance(name)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
