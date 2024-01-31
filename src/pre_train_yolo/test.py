import os


def find_jpg_files(folder_path):
    jpg_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".jpg"):
                jpg_path = os.path.join(root, file)
                jpg_files.append(jpg_path)
    return jpg_files

import yolov5
import torch
from PIL import Image, ImageDraw

def detect_and_draw(model, jpg_path, save_path):
    # Load the image
    image = Image.open(jpg_path).convert("RGB")

    # Use the model to detect objects
    results = model(image)

    # Get bounding boxes, confidence scores, and class labels
    boxes = results.xyxy[0].cpu().numpy()
    confidences = results.xyxy[0][:, 4].cpu().numpy()
    class_labels = results.xyxy[0][:, 5].cpu().numpy()

    # Create a draw object
    draw = ImageDraw.Draw(image)


    # Iterate over detected objects
    for box, confidence, class_label in zip(boxes, confidences, class_labels):
        # Extract coordinates
        x_min, y_min, x_max, y_max = box[:4]

        # Draw bounding box
        draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=3)

        # Display confidence and class label
        label = f"{int(class_label)}: {confidence:.2f}"
        draw.text((x_min, y_min - 15), label, fill="red")

    # Save the image with detection results
    image.save(os.path.join(save_path,os.path.basename(jpg_path)))
    print("operte:",os.path.join(save_path,os.path.basename(jpg_path)))

if __name__ == "__main__":
    print(os.path.abspath("../../../images"))
    imgs = find_jpg_files("../../../images")
    # Model loading
    model = torch.hub.load(os.path.dirname(yolov5.__file__), 'custom', os.path.join("./", "best.pt"), source='local')
    # model = torch.hub.load("ultralytics/yolov5", "yolov5s")
    for i in imgs:
        detect_and_draw(model, i, "../../../images/r")