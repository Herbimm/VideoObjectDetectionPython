from random import randint

import cv2
import sys

tracker = cv2.TrackerCSRT.create()

video = cv2.VideoCapture("videos/walking.avi")

if not video.isOpened():
    print("Não foi possivel abrir o vídeo")
    sys.exit()

ok, frame = video.read()
if not ok:
    print("Não é possivel ler o arquivo de video")
    sys.exit()

cascade = cv2.CascadeClassifier('cascade/fullbody.xml')

def detectar():
    while True:
        ok , frame = video.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detection = cascade.detectMultiScale(frame_gray)
        for ( x , y, l , a) in detection:
            cv2.rectangle(frame, (x, y ), (x + l, y + a), (0,0,255), 2)

            if x > 0:
                print("Detecção efetuada pelo haarscascade")
                return x , y ,l , a


bbox = detectar()
#print(bbox)

ok = tracker.init(frame, bbox)
color = (randint(0, 255), randint(0, 255), randint(0 ,255))

while True:
    ok, frame = video.read()
    if not ok:
        break

    ok, bbox = tracker.update(frame)
    if ok:
        (x, y , w , h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y+ h), color, 2 , 1)
    else:
        print("Falha no rastreamento será executado o detector novamente haarcascade")
        bbox = detectar()
        tracker = cv2.TrackerCSRT.create()
        tracker.init(frame, bbox)

    cv2.imshow("Tracking", frame)
    k = cv2.waitKey(1) & 0XFF
    if k == 27:
        break
