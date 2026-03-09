import time
import tensorflow as tf #2.15.0
from keras.models import load_model
import cv2  # 4.6.0
import numpy as np #1.23.5
import serial
from playsound3 import playsound
COM_PORT = '/dev/cu.usbmodem14201'
BAUD_RATES = 9600
ser = serial.Serial(COM_PORT, BAUD_RATES)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)
wake = 0


cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame")
        break
    img = cv2.resize(frame , (398, 224))
    show_img = img[0:224, 80:304]

    img = np.asarray(show_img, dtype=np.float32).reshape(1, 224, 224, 3)
    img = (img / 127.5) - 1

    prediction = model.predict(img)
    index = np.argmax(prediction)
    print(index)
    if index == 0 and wake==0:
        print("Not on bed")
        '''try:
            if sound.is_alive():
                sound.stop()
        except:
            continue'''
    elif index == 1 and wake==0:
        print("On bed")
        ser.write(b'TurnOff\n')
        lights = 0
        time.sleep(10)#8hr=28800
        wake = 1
        ser.write(b'TurnOn\n')
        lights = 1
        sound = playsound("mixkit-alert-alarm-1005.wav", block=False)
    elif index==0 and wake==1:
        sound.stop()
        wake = 0
        print("Good Morning!")
        break
    elif index==1 and wake==1:
        print("Not Awake")
        sound = playsound("mixkit-alert-alarm-1005.wav", block=False)
    cv2.imshow("Webcam Image", show_img)
    time.sleep(5)

    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
