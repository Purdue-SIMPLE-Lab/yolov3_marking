import os
import argparse
import xml.etree.ElementTree as ET
import cv2

def convert_voc_annotation(data_path, data_type, anno_path, use_difficult_bbox=True):

    # classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
    #            'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse',
    #            'motorbike', 'person', 'pottedplant', 'sheep', 'sofa',
    #            'train', 'tvmonitor']
    classes = ['left_turn', 'right_turn', 'straight', 'left_straight', 'right_straight', 'stop', 'speed_35', 'speed_40']
    img_inds_file = os.path.join(data_path, 'ImageSets', 'Main', data_type + '.txt')
    with open(img_inds_file, 'r') as f:
        txt = f.readlines()
        image_inds = [line.strip()[:13] for line in txt]

    with open(anno_path, 'a') as f:
        for image_ind in image_inds:
            image_path = os.path.join(data_path, 'JPEGImages', image_ind + '.jpg')
            annotation = image_path
            image_path_mirror = os.path.join(data_path, 'JPEGImages', image_ind + '_mirror.jpg')
            annotation_mirror = image_path_mirror
            label_path = os.path.join(data_path, 'Annotations', image_ind + '.xml')
            root = ET.parse(label_path).getroot()
            objects = root.findall('object')
            im_save = False
            for obj in objects:
                difficult = obj.find('difficult').text.strip()
                if (not use_difficult_bbox) and(int(difficult) == 1):
                    continue
                bbox = obj.find('bndbox')
                class_ind = classes.index(obj.find('name').text.lower().strip())
                xmin = bbox.find('xmin').text.strip()
                xmax = bbox.find('xmax').text.strip()
                ymin = bbox.find('ymin').text.strip()
                ymax = bbox.find('ymax').text.strip()
                annotation += ' ' + ','.join([xmin, ymin, xmax, ymax, str(class_ind)])

                # if class_ind == 0 or class_ind == 1:
                #     if not im_save:
                #         img = cv2.imread(image_path)
                #         img_mir = cv2.flip(img, 1)
                #         cv2.imwrite(image_path_mirror, img_mir)
                #         im_save = True
                #     width = float(root.find('size').find('width').text.strip())
                #     annotation_mirror += ' ' + ','.join([str(width-float(xmax)), ymin, str(width-float(xmin)), ymax, str(1 - class_ind)])

            print(annotation)
            f.write(annotation + "\n")
            if im_save:
                print(annotation_mirror)
                f.write(annotation_mirror + "\n")
    return len(image_inds)

# # generate some right-turn images by adding gaussian noise
# def convert_voc_annotation(data_path, data_type, anno_path, use_difficult_bbox=True):

#     # classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
#     #            'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse',
#     #            'motorbike', 'person', 'pottedplant', 'sheep', 'sofa',
#     #            'train', 'tvmonitor']
#     classes = ['left_turn', 'right_turn', 'straight', 'left_straight', 'right_straight', 'stop', 'speed_35', 'speed_40']
#     img_inds_file = os.path.join(data_path, 'ImageSets', 'Main', data_type + '.txt')
#     with open(img_inds_file, 'r') as f:
#         txt = f.readlines()
#         image_inds = [line.strip()[:13] for line in txt]

#     with open(anno_path, 'a') as f:
#         for image_ind in image_inds:
#             image_path = os.path.join(data_path, 'JPEGImages', image_ind + '.jpg')
#             annotation = image_path
#             image_path_mirror = os.path.join(data_path, 'JPEGImages', image_ind + '_mirror.jpg')
#             annotation_mirror = image_path_mirror
#             label_path = os.path.join(data_path, 'Annotations', image_ind + '.xml')
#             root = ET.parse(label_path).getroot()
#             objects = root.findall('object')
#             im_save = False
#             for obj in objects:
#                 difficult = obj.find('difficult').text.strip()
#                 if (not use_difficult_bbox) and(int(difficult) == 1):
#                     continue
#                 bbox = obj.find('bndbox')
#                 class_ind = classes.index(obj.find('name').text.lower().strip())
#                 xmin = bbox.find('xmin').text.strip()
#                 xmax = bbox.find('xmax').text.strip()
#                 ymin = bbox.find('ymin').text.strip()
#                 ymax = bbox.find('ymax').text.strip()
#                 annotation += ' ' + ','.join([xmin, ymin, xmax, ymax, str(class_ind)])

#                 if class_ind == 0 or class_ind == 1:
#                     if not im_save:
#                         img = cv2.imread(image_path)
#                         img_mir = cv2.flip(img, 1)
#                         cv2.imwrite(image_path_mirror, img_mir)
#                         im_save = True
#                     width = float(root.find('size').find('width').text.strip())
#                     annotation_mirror += ' ' + ','.join([str(width-float(xmax)), ymin, str(width-float(xmin)), ymax, str(1 - class_ind)])

#             print(annotation)
#             f.write(annotation + "\n")
#             if im_save:
#                 print(annotation_mirror)
#                 f.write(annotation_mirror + "\n")
#     return len(image_inds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="F:\\OD_Data\\RoadMarkingDataset\\Annotations\\RoadMarking-Labelling-PascalVOC-export")
    parser.add_argument("--train_annotation", default="../data/dataset/mark_train_ori.txt")
    parser.add_argument("--test_annotation",  default="../data/dataset/mark_test_ori.txt")
    flags = parser.parse_args()

    if os.path.exists(flags.train_annotation):os.remove(flags.train_annotation)
    if os.path.exists(flags.test_annotation):os.remove(flags.test_annotation)

    num1 = convert_voc_annotation(flags.data_path, 'left_straight_train', flags.train_annotation, False)
    num2 = convert_voc_annotation(flags.data_path,  'left_straight_val', flags.test_annotation, False)
    print('=> The number of image for train is: %d\tThe number of image for test is:%d' %(num1, num2))


