import face_recognition
import json
import numpy as np
import datetime
import db


def captureFace(img,nama_siswa,sekolah_id,kelas_id):
    
    while True:
        img_load = face_recognition.load_image_file(img)
        faces = face_recognition.face_encodings(img_load)
        if len(faces)==1:
            face_encoded = json.dumps(faces[0].tolist())
            db.execute("INSERT INTO student (nama_siswa,sekolah_id,face_encodings,kelas_id) VALUES ('{}',{},'{}',{})".format(nama_siswa,sekolah_id,face_encoded,kelas_id))
            
            return "successfully added a face to databsae",False
        else:
            return "please show your face to the camera, and avoid other people faces",True
