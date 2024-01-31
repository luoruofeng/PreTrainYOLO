import json
import os

def coco_to_yolo(coco_json_folder, yolo_txt_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(yolo_txt_folder, exist_ok=True)

    # List all json files in the folder
    for json_file in os.listdir(coco_json_folder):
        if json_file.endswith('.json'):
            json_path = os.path.join(coco_json_folder, json_file)
            if os.path.exists(json_path):
                with open(json_path, 'r') as file:
                    coco_data = json.load(file)

                    # Index images by id for quick lookup
                    images = {image['id']: image for image in coco_data['images']}

                    # Process each annotation
                    for annotation in coco_data['annotations']:
                        image_id = annotation['image_id']
                        category_id = annotation['category_id']  # YOLO class-ids start at 0
                        bbox = annotation['bbox']
                        image_info = images[image_id]
                        width, height = image_info['width'], image_info['height']

                        # Convert COCO bbox format (top-left x/y, width, height) to YOLO format
                        x_center = (bbox[0] + bbox[2] / 2) / width
                        y_center = (bbox[1] + bbox[3] / 2) / height
                        bbox_width = bbox[2] / width
                        bbox_height = bbox[3] / height

                        # Prepare YOLO formatted annotation
                        yolo_annotation = f"{category_id} {x_center} {y_center} {bbox_width} {bbox_height}\n"

                        # Write YOLO formatted annotation to txt file
                        txt_filename = os.path.splitext(json_file)[0] + '.txt'
                        txt_path = os.path.join(yolo_txt_folder, txt_filename)
                        with open(txt_path, 'a') as txt_file:
                            txt_file.write(yolo_annotation)

if __name__ == "__main__":
    # Example usage:
    coco_to_yolo('data/coco_result_merged', 'data/yolo')
