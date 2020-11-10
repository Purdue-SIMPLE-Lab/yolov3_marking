#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : image_demo.py
#   Author      : YunYang1994
#   Created date: 2019-01-20 16:06:06
#   Description :
#
#================================================================

import os
import shutil
import cv2
import numpy as np
import core.utils as utils
import tensorflow as tf
from PIL import Image

return_elements = ["input/input_data:0", "pred_sbbox/concat_2:0", "pred_mbbox/concat_2:0", "pred_lbbox/concat_2:0"]
pb_file         = "./yolov3_mark.pb"
image_path      = "./docs/images/test_images"
result_path     = "./docs/images/test_results1"
num_classes     = 8
input_size      = 416
graph           = tf.Graph()

return_tensors = utils.read_pb_return_tensors(graph, pb_file, return_elements)

if os.path.exists(result_path): shutil.rmtree(result_path)
os.mkdir(result_path)

img_list = os.listdir(image_path)

with tf.Session(graph=graph) as sess:
    for filename in img_list:
        original_image = cv2.imread(os.path.join(image_path, filename))
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        original_image_size = original_image.shape[:2]
        image_data = utils.image_preporcess(np.copy(original_image), [input_size, input_size])
        image_data = image_data[np.newaxis, ...]
        pred_sbbox, pred_mbbox, pred_lbbox = sess.run(
            [return_tensors[1], return_tensors[2], return_tensors[3]],
                    feed_dict={ return_tensors[0]: image_data})

        pred_bbox = np.concatenate([np.reshape(pred_sbbox, (-1, 5 + num_classes)),
                                    np.reshape(pred_mbbox, (-1, 5 + num_classes)),
                                    np.reshape(pred_lbbox, (-1, 5 + num_classes))], axis=0)

        bboxes = utils.postprocess_boxes(pred_bbox, original_image_size, input_size, 0.3)
        bboxes = utils.nms(bboxes, 0.45, method='nms')
        image = utils.draw_bbox_with_contrast(original_image, bboxes)
        # image = Image.fromarray(image)
        # image.show()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.join(result_path, filename), image)
        print("Saved to %s.\n" % os.path.join(result_path, filename))




