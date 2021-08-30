import Train_Image
import Capture_Image
import Recognize
import Delete_Image

def main():
    print("[1] Register Face")
    print("[2] Absensi")
    print("[3] Delete Face")
    inputs = int(input("Choose input: "))
    
    if inputs == 1:
        Capture_Image.takeImages()
        main()
    if inputs == 2:
        Recognize.recognize_attendence()
        main()
    if inputs == 3:
        Delete_Image.deleteNow()
        main()
        
    else:
        pass


if __name__ == '__main__':
    main()
