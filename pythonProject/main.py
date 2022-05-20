import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import wmi
import os
from tensorflow.keras.models import load_model

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.9)
mpDraw = mp.solutions.drawing_utils

model = load_model('mp_hand_gesture')
flag = 0
programHandle = wmi.WMI()
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)
detectedGestures = []
lst1 = ['okay', 'peace', 'thumbs up', 'thumbs down', 'call me', 'stop', 'rock', 'live long', 'fist', 'smile']
cap = cv2.VideoCapture(0)
dictProcess = {
    'peace': 'brave.exe',
    'call me': 'taskmgr.exe',
    'okay': '%windir%\explorer.exe shell:::{3080F90D-D7AD-11D9-BD98-0000947B0257}'  # show desktop
}


def startProcess(className):
    flag = 0
    if (className in dictProcess.keys()):
        process1 = dictProcess[className]
        print("Check1")
        for process in programHandle.Win32_Process():
            if (".exe" in process1):
                if (process1) == process.Name:
                    print("Application is Running")
                    flag = 1
                    break
                else:
                    flag = 0
        if (flag == 0):
            os.system("cmd /c start " + process1)


while True:
    _, frame = cap.read()

    x, y, c = frame.shape

    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(framergb)

    className = ''

    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])

            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            prediction = model.predict([landmarks])
            classID = np.argmax(prediction)
            className = classNames[classID]
            i = len(detectedGestures)
            if (i < 2):
                detectedGestures.append(className)
                print(detectedGestures)
        else:
            if (className != detectedGestures[-1]):
                detectedGestures.append(className)
                print(className)
                startProcess(className)

cap.release()


