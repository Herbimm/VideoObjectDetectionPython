import cv2
import sys
from random import randint


(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
print(major_ver)
print(minor_ver)
print(subminor_ver)

tracker_types = ['BOOSTING', "MIL", "KCF", "TLD",  "MEDIANFLOW", "MOSSE", "CSRT"]

tracker_type = tracker_types[1]

print(tracker_type)

if int(minor_ver) < 3:
    tracker = tracker_type
else:
    if tracker_type == "BOOSTING":
        print('error boosting')
    if tracker_type == "MIL":
        tracker = cv2.TrackerMIL.create()
    if tracker_type == "KCF":
        tracker = cv2.TrackerKCF.create()
    if tracker_type == "TLD":
        print('ERROR TLD')
    if tracker_type == "MEDIANFLOW":
        print("MEDIANFLOW ERROR")
    if tracker_type == "MOSSE":
        print("MOSSE ERROR")
    if tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT.create()

#print(tracker)

video = cv2.VideoCapture('../videos/race.mp4')
if not video.isOpened():
    print('Não foi possivel carregar o vídeo')
    sys.exit()

ok, frame = video.read()
if not ok:
    print("Não foi possível ler o arquivo de vídeo")
    sys.exit()

#print(ok)

bbox = cv2.selectROI(frame, False)
#print(bbox)

ok = tracker.init(frame, bbox)
print(ok)

colors = (randint(0, 255), randint(0 , 255), randint(0, 255))
print(colors)

while True:
    ok, frame = video.read()
    if not ok:
        break

    timer = cv2.getTickCount()
    ok, bbox = tracker.update(frame)
    #print(ok, bbox)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    if ok:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w,y + h), colors, 2, 1)
    else:
        cv2.putText(frame, "Falha no rastreamento", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, .75, (0,0,255), 2)

    cv2.putText(frame, tracker_type + ' Tracker', (100, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

    cv2.putText(frame, 'FPS' + str(int(fps)) + ' Tracker', (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    cv2.imshow('Tracking', frame)
    if cv2.waitKey(1) & 0XFF == 27:
        break;
