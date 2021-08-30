import face_recognition
import db
import json
import numpy as np

def recognize(img,kelas_id):
    students = db.execute("SELECT * FROM student WHERE kelas_id = %s"%kelas_id)
    for i in students:
        unknown_image = face_recognition.load_image_file(img)

        face_encoded = face_recognition.face_encodings(unknown_image)[0]

        results = face_recognition.compare_faces([np.array(json.loads(i[3]))],face_encoded)
        if results[0]:
            db.execute("INSERT INTO absensi (user_id,waktu,kelas_id) VALUES (%s,NOW(),%s)"%(i[0],kelas_id))
            return "Successfully attend the class",False
        else:
            return "Unknown Face, Please try again",True


    
