# PreTrainYOLO

## 目标
在已有烟雾和火焰的数据集（Pascal VOC格式）和人物图片(不包含标注文件)的的条件下，使用yolov5训练出能够同时识别烟雾，火焰，人的模型。
   

思路：
1. 将voc转换为coco格式
2. 使用yolov5s模型给定图片的推理中人的信息存保存为coco标注，如果该图片有火烟雾就将两个coco融合为同一个coco标注文件，即包含吧烟雾，火，人的coco标注文件。
3. 如果图片宽或高超过640px则裁剪到640px大小内。
4. yolov5训练。

## 数据来源
1. [火焰和烟雾的数据集](https://aistudio.baidu.com/datasetdetail/107770)
2. 带有人的图片可用从[Visual Object Classes Challenge 2012 (VOC2012)](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar)下载，在通过python程序清洗掉不带人的图片。

## 开始
1. *data/img*存放包含火，烟雾和人的图片
2. *data/voc*存放pascal数据集的火监测xml数据（Pascal VOC格式）
3. *data/coco_result*存放pascal转coco后的监测数据（执行python .\pascal2coco.py生成的结果）
```shell
python .\pascal2coco.py
```

4. *data/coco_result_merged*存放监测到的人的数据和*data/coco_result*合并后的数据（执行python .\detect_person.py生成的结果）
```shell
python .\detect_person.py
```

5. *data/coco_result*存放从*data/coco_result_merged*coco数据集格式转化为yolo数据集格式的数据（执行python .\coco2yolo.py生成的结果）
```shell
python .\coco2yolo.py
```

6. 将该项目中的*data/coco_result* 和 *data/img* 文件夹中的内容放入*datasets的images和labels文件夹*中。

7. 调用python .\scale_down.py将图片最长的变改为640。等比例缩小图片。
```shell
python .\scale_down.py
```
8. 编写*data/fire.yaml*确定训练路径和目标。

9. 开始训练
```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5

python train.py --img 640 --epochs 3 --data C:\Users\luoru\Desktop\PreTrainYOLO\src\pre_train_yolo\data\fire.yaml --weights yolov5s.pt
```

10. 获取最终的结果runs/exp/weigths/best.pt

11. 使用test测试pt。