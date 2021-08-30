const video = document.getElementById('video');
const canvas = document.getElementById('canvas')
const buttonCapture = document.getElementById('btnRegister')
Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
    faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
    faceapi.nets.faceRecognitionNet.loadFromUri('/models'),
    faceapi.nets.faceExpressionNet.loadFromUri('/models')
]).then(startVideo)

function startVideo(){
    navigator.getUserMedia(
        { video: {} },
        stream => {
            video.srcObject = stream
            
            

        },
        err => console.error(err)

    )
}


video.addEventListener('play',()=>{
    canvas.srcObject = video.srcObject;
    const drawer = faceapi.createCanvasFromMedia(video)
    
    document.body.append(drawer)
    const displaySize = {
        width: video.width,
        height:video.height
    }
    faceapi.matchDimensions(drawer,displaySize)
    setInterval(async()=>{
        
        const detections = await faceapi
            .detectAllFaces(video,new faceapi.TinyFaceDetectorOptions())
            .withFaceLandmarks()
            .withFaceExpressions()

        if (detections.length == 1){
            buttonCapture.disabled = false
            buttonCapture.innerText = "Register Face"
        }else{
            buttonCapture.disabled = true
            buttonCapture.innerText = "Please show your face to the camera, and only 1 face is required"
        }
        
        
        const resizedDetections = faceapi.resizeResults(
            detections,
            displaySize
        )
        drawer.getContext('2d').clearRect(0,0,drawer.width,drawer.height)
        faceapi.draw.drawDetections(drawer,resizedDetections)
        // faceapi.draw.drawFaceLandmarks(drawer,resizedDetections)
        
    },100)
})



function registerFace(){
    console.log("registering face...")
}


