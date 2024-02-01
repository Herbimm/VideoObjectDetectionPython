import cv2
import sys
from random import randint


(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
print(major_ver)
print(minor_ver)
print(subminor_ver)

tracker_types = [ "MIL","KCF", "CSRT", "BOOSTING"]

def createTrackerByName(trackerType):
    if trackerType == tracker_types[0]:
        tracker = cv2.legacy.TrackerMIL.create()
    elif trackerType == tracker_types[1]:
        tracker = cv2.legacy.TrackerKCF.create()
    elif trackerType == tracker_types[2]:
        tracker = cv2.legacy.TrackerCSRT.create()
    elif trackerType == tracker_types[3]:
        tracker = cv2.legacy.TrackerBoosting.create()
    else:
        tracker = None
        print("Nome Incorreto")
        print("Os Rastreadores disponíveis são: ")
        for t in tracker_types:
            print(t)

    return tracker

#print(createTrackerByName('CSRT'))

cap = cv2.VideoCapture("videos/race.mp4")

ok, frame = cap.read()

if not ok:
    print("Não foi possivel ler o arquivo de vídeo")
    sys.exit(1)

bboxes = []
colors = []

while True:
    bbox = cv2.selectROI('MultiTracker', frame)
    bboxes.append(bbox)
    colors.append((randint(0, 255), randint(0 , 255), randint(0 , 255)))
    print("Precione Q para sair das caixas de seleção e começar o rastreamento")
    print("Precione qualquer outra tecla para selecionar o proximo objeto")
    k = cv2.waitKey(0) & 0XFF
    if (k == 113):
        break

print("Caixas delimitadores selecionadas {}".format(bboxes))
print("Cores {}".format(colors))


trackertype = 'BOOSTING'
multiTracker = cv2.legacy.MultiTracker.create()

for bbox in bboxes:
    multiTracker.add(createTrackerByName(trackertype), frame, bbox)

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break;

    ok, boxes = multiTracker.update(frame)

    for i, newbox in enumerate(boxes):
        (x , y , w , h ) = [int(v) for v in newbox]
        cv2.rectangle(frame, (x , y ), (x + w, y  + h ), colors[i], 2 , 1)

    cv2.imshow("MultiTracker", frame)

    if cv2.waitKey(1) & 0XFF == 27:
        break;



