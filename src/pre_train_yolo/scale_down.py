from PIL import Image
import os

def resize_images_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.jpg'):
                file_path = os.path.join(root, file)
                with Image.open(file_path) as img:
                    width, height = img.size

                    # 检查是否需要缩放
                    if width > 640 or height > 640:
                        # 确定缩放比例
                        scale = min(640/width, 640/height)

                        # 计算新的尺寸
                        new_width = int(width * scale)
                        new_height = int(height * scale)

                        # 缩放图片
                        resized_img = img.resize((new_width, new_height), Image.LANCZOS)

                        # 保存图片
                        resized_img.save(file_path)

                        print(f"Resized {file_path} to {new_width}x{new_height}")


if __name__ == "__main__":
    resize_images_in_folder("datasets/images")