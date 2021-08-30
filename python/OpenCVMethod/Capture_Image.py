import csv
import Train_Image
import pyautogui
import cv2
import os
import numpy as np
import db


# counting the numbers


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False



# Take image function

def takeImages():


    Id = input("Id: ")
    nama = input("Nama: ")

    if(is_number(Id) and nama.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while(True):
            ret, img = cam.read()
            # img = pyautogui.screenshot()
            # img = np.array(img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
                #incrementing sample number
                sampleNum = sampleNum+1
                cv2.putText(img, "sample :"+str(sampleNum),(x, y),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),2,cv2.LINE_AA)
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage" + os.sep +nama + "."+Id + '.' +
                            str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                #display the frame
                cv2.imshow('frame', img)
            #wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 25:
                break
        cam.release()
        cv2.destroyAllWindows()
        db.execute("INSERT INTO student (id,name) VALUES (%s,'%s')"%(Id, nama))
        
        Train_Image.TrainImages()
        
                
    else:
        if(is_number(Id)):
            print("Enter Alphabetical Name")
        if(nama.isalpha()):
            print("Enter Numeric ID")


