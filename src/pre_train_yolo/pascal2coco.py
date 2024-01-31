import os
import xml.etree.ElementTree as ET

# 解析PASCAL VOC格式的XML文件
def parse_voc_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    annotation_info = {
        'image_id': root.find('filename').text,
        'width': int(root.find('size/width').text),
        'height': int(root.find('size/height').text),
        'annotations': []
    }

    for obj in root.findall('object'):
        annotation = {
            'category_id': obj.find('name').text,
            'bbox': [
                float(obj.find('bndbox/xmin').text),
                float(obj.find('bndbox/ymin').text),
                float(obj.find('bndbox/xmax').text) - float(obj.find('bndbox/xmin').text),
                float(obj.find('bndbox/ymax').text) - float(obj.find('bndbox/ymin').text)
            ]
        }
        annotation_info['annotations'].append(annotation)

    return annotation_info

#   使用解析得到的信息构建COCO格式的标注数据结构
import json

def convert_to_coco_format(voc_annotations):
    coco_format = {
        'images': [],
        'annotations': [],
        'categories': []
    }

    category_id_mapping = {
        "default":0,
        "fire":1,
        "smoke":2,
        "person":3
    }  
    # Add images and annotations
    for i, annotation in enumerate(voc_annotations['annotations']):
        if coco_format is None or len(coco_format['images']) < 1:
            image_info = {
                'id': i + 1,
                'width': voc_annotations['width'],
                'height': voc_annotations['height'],
                'file_name': voc_annotations['image_id']
            }
            coco_format['images'].append(image_info)

        # 处理类别信息
        category_name = annotation['category_id']
        if category_name in category_id_mapping and category_name not in [c['name'] for c in coco_format['categories'] if c is not None]:
            new_category_id = category_id_mapping[category_name]
            category_info = {'id': new_category_id, 'name': category_name}
            coco_format['categories'].append(category_info)
        
        # 添加注释信息
        coco_annotation = {
            'id': i + 1,
            'image_id': 1,
            'category_id': category_id_mapping[category_name],
            'bbox': annotation['bbox'],
            'area': annotation['bbox'][2] * annotation['bbox'][3],
            'iscrowd': 0
        }
        coco_format['annotations'].append(coco_annotation)

    return coco_format


# COCO格式的标注数据保存为JSON文件
def save_coco_json(coco_data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(coco_data, json_file, indent=4)

def find_xml_files(folder_path):
    xml_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".xml"):
                xml_path = os.path.join(root, file)
                xml_files.append(xml_path)
    return xml_files

if __name__ == "__main__":
    for xml in find_xml_files("data/"):
        print(f"处理:{xml}")
        annotation_info = parse_voc_xml(xml)
        coco_format = convert_to_coco_format(annotation_info)
        file_name = os.path.basename(xml)
        save_coco_json(coco_format, f"data/coco_result/{file_name.split('.')[0]}.json")