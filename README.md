
## This repository is modified from the public source codes of YunYang1994 (https://github.com/YunYang1994/tensorflow-yolov3)

## Quick start

## 1.  You are supposed  to install some dependencies before getting out hands with these codes.
```bashrc
$ cd yolov3_marking
$ pip install -r ./docs/requirements.txt
```

## 2. Train on your own dataset
Two files are required as follows:

- [`dataset.txt`](https://raw.githubusercontent.com/YunYang1994/tensorflow-yolov3/master/data/dataset/mark_train.txt): 

```
xxx/xxx.jpg 18.19,6.32,424.13,421.83,20 323.86,2.65,640.0,421.94,20 
xxx/xxx.jpg 48,240,195,371,11 8,12,352,498,14
# image_path x_min, y_min, x_max, y_max, class_id  x_min, y_min ,..., class_id 
# make sure that x_max < width and y_max < height
```

- [`class.names`](https://github.com/YunYang1994/tensorflow-yolov3/blob/master/data/classes/mark.names):

```
left_turn
right_turn
straight
left_straight
right_straight
stop
speed_35
speed_40
```

2.1. Convert the dataset
$ python scripts/mark_annotation.py --data_path your_data_folder
```
Then edit your `./core/config.py` to make some necessary configurations

```bashrc
__C.YOLO.CLASSES                = "./data/classes/mark.names"
__C.TRAIN.ANNOT_PATH            = "./data/dataset/mark_train.txt"
__C.TEST.ANNOT_PATH             = "./data/dataset/mark_test.txt"
```


2.2 train from COCO weights(recommend):

```bashrc
$ cd checkpoint
$ wget https://github.com/YunYang1994/tensorflow-yolov3/releases/download/v1.0/yolov3_coco.tar.gz
$ tar -xvf yolov3_coco.tar.gz
$ cd ..
$ python convert_weight.py --train_from_coco
$ python train.py
```
2.3 Evaluate on the testing dataset

```
$ python evaluate.py
$ cd mAP
$ python main.py -na
```

## 3.Evaluate on images or videos
Convert trained weights as pb file
$ python freeze_graph.py

Then you will get some .pb files in the root path., and run the demo script
$ python image_demo.py
$ python video_demo.py # if use camera, set video_path = 0
$ python video_demo_detection.py

