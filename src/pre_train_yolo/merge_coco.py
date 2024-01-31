# 未使用

import json
import os
from collections import defaultdict

def merge_json_files(folder_path):
    merged_data = {
        "images": [],
        "annotations": [],
        "categories": []
    }
    
    # 用于确保categories的唯一性
    category_set = defaultdict(dict)
    next_image_id = 1
    next_annotation_id = 1
    
    # 遍历文件夹中的所有JSON文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                
                # 处理images和annotations，更新ID
                for image in data['images']:
                    image['id'] = next_image_id
                    merged_data['images'].append(image)
                    next_image_id += 1
                
                print(f"images:{image}")

                for annotation in data['annotations']:
                    annotation['id'] = next_annotation_id
                    # 更新image_id到新的ID
                    annotation['image_id'] = merged_data['images'][-1]['id']
                    merged_data['annotations'].append(annotation)
                    next_annotation_id += 1
                    
                # 处理categories，确保唯一性
                for category in data['categories']:
                    cat_id = category['id']
                    if cat_id not in category_set or category_set[cat_id] != category:
                        category_set[cat_id] = category
                        merged_data['categories'].append(category)
    
    return merged_data

# 假设你的JSON文件存放在'json_folder'目录下
folder_path = 'json_folder'
merged_data = merge_json_files(folder_path)

# 如果你需要将合并后的数据保存为新的JSON文件
with open('merged_data.json', 'w') as outfile:
    json.dump(merged_data, outfile)