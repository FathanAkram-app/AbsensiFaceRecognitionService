import datetime
import os
import time
import pyautogui
import numpy as np
import cv2
import pandas as pd
import db
import time

#-------------------------
def recognize_attendence():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel"+os.sep+"Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = db.execute("SELECT * FROM student")
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    attended = False
    color = (10, 159, 255)
    while True:
        ret, img = cam.read()
        if ret:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5,minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)
            for(x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), color , 2)
                Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

                if conf < 100:

                    aa = [i for i in df if Id == i[0]]
                    confstr = "  {0}%".format(round(100 - conf))
                    tt = str(Id)+"-"+aa[0][1]
                else:
                    Id = '  Unknown  '
                    tt = str(Id)
                    confstr = "  {0}%".format(round(100 - conf))


                if(100-conf) > 70 and (100-conf) < 99:
                    tt = tt + " [Pass]"
                    cv2.putText(img, str(tt), (x+5,y-5), font, 1, (255, 255, 255), 2)
                    date = datetime.datetime.utcnow()
                    attended = True

                    db.execute("INSERT INTO absensi (user_id,waktu) VALUES (%s,'%s')"%(Id,date))
                    
                else:
                    cv2.putText(img, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                color = (25, (100-conf)*(255/100), 0)
                
                if (100-conf) > 70:
                    cv2.putText(img, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
                elif (100-conf) > 50:
                    
                    cv2.putText(img, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
                else:
                    cv2.putText(img, "unknown", (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)
                
                if attended:
                    break



            cv2.imshow('Attendance', img)
            if attended:
                break
            if (cv2.waitKey(1) == ord('q')):
                break
    
    cam.release()
    cv2.destroyAllWindows()


