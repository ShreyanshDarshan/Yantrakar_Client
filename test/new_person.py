import cv2
from vision.ssd.mobilenet import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor

model_path = "models/mobilenet-v1-ssd-mp-0_675.pth"
label_path = "models/voc-model-labels.txt"

class_names = [name.strip() for name in open(label_path).readlines()]
num_classes = len(class_names)
net = create_mobilenetv1_ssd(len(class_names), is_test=True)
net.load(model_path)
predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)

orig_image = cv2.imread("/home/zoh/Downloads/M7LOWI7I5FG37M7K6OUYWWTIVY.jpg")

image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
boxes, labels, probs = predictor.predict(image, 10, 0.4)

print(boxes, labels, probs)

new_boxes = []
new_labels = []
new_probs = []

for i in range(len(labels)):
    if labels[i] == 15:
        new_boxes.append(boxes[i, :])
        new_labels.append(15)
        new_probs.append(probs[i])

boxes = new_boxes
labels = new_labels
probs = new_probs

for i in range(len(boxes)):
    box = boxes[i]
    if labels[i] != 15:
        continue
    label = f"{class_names[labels[i]]}: {probs[i]:.2f}"
    cv2.rectangle(orig_image, (box[0], box[1]),
                  (box[2], box[3]), (255, 255, 0), 4)

cv2.imshow('annotated', orig_image)
#cv2.imwrite("test4.png", orig_image)

cv2.waitKey(0)

cv2.destroyAllWindows()
