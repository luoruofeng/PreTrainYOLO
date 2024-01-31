import os
import torch

MODEL_NAME = "yolov5s"

PERSON_CONFIDENCE = 0.4
def detect_objects(model,image_path):
    img = image_path
    results = model(img)
    results.print()  # Other options: .show(), .save(), .crop(), .pandas(), etc.
    objs = results.xyxy[0]
    targets = []
    w,h = get_image_dimensions(image_path)
    for o in objs:
        if len(o) > 4:
            if o[5].item() != 0 or o[4].item() < PERSON_CONFIDENCE:
                continue
            target_info = {
                "left_top": (o[0].item(), o[1].item()),
                "right_bottom": (o[2].item(), o[3].item()),
                "width": o[2].item() - o[0].item(),
                "height": o[3].item() - o[1].item(),
                "confidence": o[4].item(),
                "class_id": o[5].item(),
                "img_w": w,
                "img_h": h
            }
            targets.append(target_info)

    return targets



def find_jpg_files(folder_path):
    jpg_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".jpg"):
                jpg_path = os.path.join(root, file)
                jpg_files.append(jpg_path)
    return jpg_files

import json


def convert_to_coco_format(data_list, img_name, categories_id, categories_name):
    if data_list is None or len(data_list) < 1:
        return None

    coco_data = {
        "images": [],
        "annotations": [],
        "categories": [{"id": categories_id, "name": categories_name}]
    }

    annotation_id = 1

    image_info = {
        "id": 1,
        "width": int(data_list[0]['img_w']),
        "height": int(data_list[0]['img_h']),
        "file_name": img_name
    }

    # Flag to check if an image has been added
    image_added = False

    for item in data_list:
        if not image_added:
            coco_data["images"].append(image_info)
            image_added = True

        annotation_info = {
            "id": annotation_id,
            "image_id": 1,
            "category_id": categories_id,
            "area": int(item['width'] * item['height']),
            "bbox": [
                int(item['left_top'][0]),
                int(item['left_top'][1]),
                int(item['width']),
                int(item['height'])
            ],
            "iscrowd": 1 if is_bbox_covering(item, data_list) else 0
        }

        coco_data["annotations"].append(annotation_info)

        annotation_id += 1

    return json.dumps(coco_data, indent=4)

def is_bbox_covering(bbox, data_list):
    for other_bbox in data_list:
        if bbox == other_bbox:
            continue
        # Check if bbox is covering any other bbox
        if (bbox['left_top'][0] <= other_bbox['left_top'][0] and bbox['left_top'][1] <= other_bbox['left_top'][1] and
                bbox['right_bottom'][0] >= other_bbox['right_bottom'][0] and bbox['right_bottom'][1] >= other_bbox['right_bottom'][1]):
            return True
    return False

def merge_coco_datasets(coco_data1, coco_data2):
    if not coco_data1 or not coco_data2:
        return None

    # Parse JSON strings
    data1 = json.loads(coco_data1)
    data2 = json.loads(coco_data2)

    # Merge images, keeping only unique ones
    image_ids1 = {image['id'] for image in data1.get('images', [])}
    unique_images2 = [image for image in data2.get('images', []) if image['id'] not in image_ids1]
    merged_images = data1.get('images', []) + unique_images2

    # Merge categories, keeping only unique ones
    category_ids1 = {category['id'] for category in data1.get('categories', [])}
    unique_categories2 = [category for category in data2.get('categories', []) if category['id'] not in category_ids1]
    merged_categories = data1.get('categories', []) + unique_categories2

    # Merge annotations, keeping only unique ones
    merged_annotations = merge_annotation_lists(data1.get('annotations', []), data2.get('annotations', []))

    # changed all image_id of annotations to 1
    for a in merged_annotations:
        a["image_id"] = 1

    # Create the final merged dataset
    merged_data = {
        'images': merged_images,
        'annotations': merged_annotations,
        'categories': merged_categories
    }

    return json.dumps(merged_data, indent=4)

def merge_annotation_lists(annotations1, annotations2):
    merged_annotations = []

    # Merge annotations and update IDs
    for i, annotation in enumerate(annotations1 + annotations2):
        annotation['id'] = i + 1
        merged_annotations.append(annotation)

    return merged_annotations

def change_file_extension(file_path, new_extension):
    # Check if the file path exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Split the file path into directory, base name, and extension
    directory, file_name_with_extension = os.path.split(file_path)
    file_name, old_extension = os.path.splitext(file_name_with_extension)

    # Create the new file name with the specified extension
    new_file_name = f"{file_name}.{new_extension}"

    return new_file_name


def read_file_to_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

from PIL import Image
def get_image_dimensions(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width, height
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_coco_json_str(coco_data, json_path):
    with open(json_path, 'w') as json_file:
        json_file.write(coco_data)

DEFAULT_ID = 0
FIRE_ID = 1
SMOKE_ID = 2
PERSON_ID = 3

if __name__ == "__main__":
    model = torch.hub.load("ultralytics/yolov5", MODEL_NAME)
    for jpg in find_jpg_files("data/img/"):
        json_file_name = os.path.join("data/coco_result",change_file_extension(jpg,"json"))
        coco_result_merged_path = os.path.join("data/coco_result_merged", os.path.basename(json_file_name)) 
        save_json = None
        r = detect_objects(model,jpg)
        d_json = convert_to_coco_format(r, os.path.basename(jpg),PERSON_ID,"person")
        if os.path.exists(json_file_name):
            if r is None or len(r) < 1:
                save_coco_json_str(read_file_to_json(json_file_name), coco_result_merged_path)
                continue
            o_json = read_file_to_json(json_file_name)
            save_json = merge_coco_datasets(o_json, d_json)
        else:
            save_json = d_json
        if save_json is not None:
            save_coco_json_str(save_json, coco_result_merged_path)