from fastapi import FastAPI, File, UploadFile, Form, Response, status, HTTPException, Security
import register_face
import shutil
import os
import recognize_face
import db
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()
app = FastAPI()

@app.get('/')
def index():
    return {"test":"hello"}

@app.post('/api/register/face')
def register_face_api(
    image: UploadFile = File(...), 
    nama_siswa: str = Form(...), 
    sekolah_id : int = Form(...),
    kelas_id : int = Form(...),
    response: Response = Response):
    
    dirname = "TrainingImage"
    count_file = len(os.listdir(dirname))
    file_name = str(count_file+1)+".jpg"

    with open(dirname+'/'+file_name,'wb') as buffer:
        shutil.copyfileobj(image.file,buffer)

    result, errStat = register_face.captureFace(dirname+'/'+file_name,nama_siswa,sekolah_id,kelas_id)
    os.unlink(dirname+'/'+file_name)
    if errStat:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": 400,
            "message":result}
    response.status_code = status.HTTP_200_OK
    return {
        "status": 200,
        "message":result}

@app.post('/api/recognize')
def recognize_face_api(
    image: UploadFile = File(...),
    kelas_id : int = Form(...),
    response: Response = Response):

    dirname = "RecognizeImage"
    count_file = len(os.listdir(dirname))
    file_name = str(count_file+1)+".jpg"

    with open(dirname+'/'+file_name,'wb') as buffer:
        shutil.copyfileobj(image.file,buffer)

    result, errStat = recognize_face.recognize(dirname+'/'+file_name,kelas_id)

    os.unlink(dirname+'/'+file_name)

    if errStat:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": 400,
            "message":result}
    response.status_code = status.HTTP_200_OK
    return {
        "status": 200,
        "message":result}

@app.get('/api/getsekolah')
def getSekolah(response: Response = Response):
    result = db.execute("SELECT * FROM sekolah")
    result = [{"id":i[0],"nama":i[1],"alamat":i[2]} for i in result]
    response.status_code = status.HTTP_200_OK
    return {
        "status": 200,
        "message":"success",
        "result":result}
# delete coming soon
# @app.post('/api/delete/face')
# def deleteFace(
#     credentials: HTTPAuthorizationCredentials = Security(security),
#     siswa_id : int = Form(...),
#     response: Response = Response):
#     token = credentials.credentials
#     db.execute("DELETE ")