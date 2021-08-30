import face_recognition
import cv2
import json
import numpy as np
import datetime
import db


def captureFace():
    cam = cv2.VideoCapture(0)
    countDown = 5
    capture = int(datetime.datetime.utcnow().strftime("%S"))+countDown
    if capture >= 60:
        capture -= 60
    while True:
        ret, frame = cam.read()
        if ret:
            cv2.imwrite("test.jpg",frame)
            img_load = face_recognition.load_image_file("test.jpg")
            faces = face_recognition.face_encodings(img_load)
            cv2.imshow("frame",frame)
            if len(faces)==1:
                cv2.putText(frame,"Capturing in 5 seconds",(20,25),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),2)
                if capture == int(datetime.datetime.utcnow().strftime("%S")):
                    print(json.dumps(faces[0].tolist()))
                    break
            else:
                cv2.putText(frame,"Please show your face to the camera",(20,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
                capture = int(datetime.datetime.utcnow().strftime("%S"))+countDown
                if capture >= 60:
                    capture -= 60
            cv2.imshow("frame",frame)
                    
            
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
    cam.release()
    cv2.destroyAllWindows()
    

    
captureFace()