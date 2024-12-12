import cv2
import numpy as np

# Indlæs YOLO-modellen
weights_path = "objektgenkendelse/yolov3-tiny.weights"
config_path = "objektgenkendelse/yolov3-tiny.cfg"
#weights_path = "objektgenkendelse/yolov3.weights"
#config_path = "objektgenkendelse/yolov3.cfg"
labels_path = "objektgenkendelse/coco.names"

#link til de fortrænede modeller: https://pjreddie.com/darknet/yolo/

# Læs klassenavne
with open(labels_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Farver til bounding boxes
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classes), 3), dtype="uint8")

# Indlæs YOLO med OpenCV
net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

# Fang webcam-input
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Opret input blob til YOLO
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Hent output-lag-navne
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Kør YOLO-modellen
    detections = net.forward(output_layers)

    height, width = frame.shape[:2]
    boxes = []
    confidences = []
    class_ids = []

    # Processer resultater
    for output in detections:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:  # Minimum tillid
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Beregn koordinater for boksen
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Fjern overlappende bokse med NMS
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    if len(indices) > 0:  # Sørg for, at indices ikke er tom
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            color = [int(c) for c in colors[class_ids[i]]]
            label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


    # Vis resultatet
    cv2.imshow("YOLO-frame", frame)

    # Afslut med 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
