# coding=utf-8
'''
labelme to coco
@ author: zylhub
'''

import os
import json
import numpy as np
import glob

np.random.seed(41)

# 0为背景
# classname_to_id = {'不导电': 1, '擦花': 2, '角位漏底': 3, '桔皮': 4, '漏底': 5, '喷流': 6, '漆泡': 7, '起坑': 8, '杂色': 9, '脏点': 10}


class Lableme2CoCo:

    def __init__(self):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.ann_id = 0

    def save_coco_json(self, instance, save_path):
        json.dump(instance, open(save_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)  # indent=2 更加美观显示

    # 由json文件构建COCO
    def to_coco(self, json_path_list):
        self._init_categories()
        for json_path in json_path_list:
            obj = self.read_jsonfile(json_path)
            for im_name, item in obj.items():
                self.images.append(self._image(item))
                shapes = item['regions']
                # todo
                for _, shape in shapes.items():
                    annotation = self._annotation(shape)
                    if None==annotation:
                        continue
                    self.annotations.append(annotation)
                    self.ann_id += 1
                self.img_id += 1
        instance = {}
        instance['info'] = 'zylhub created'
        instance['license'] = ['license']
        instance['images'] = self.images
        instance['annotations'] = self.annotations
        instance['categories'] = self.categories
        return instance

    # 构建类别
    def _init_categories(self):
        for k, v in classname_to_id.items():
            category = {}
            category['id'] = v
            category['name'] = k
            self.categories.append(category)

    # 构建COCO的image字段
    def _image(self, obj):
        image = {}
        # from labelme import utils
        # utils.img_b64_to_arr读取文件很耗时,若图片大小都一致，可以固定h,w
        # img_x = utils.img_b64_to_arr(obj['imageData'])
        # h, w = img_x.shape[:-1]
        image['height'] = 1024
        image['width'] = 1024
        image['id'] = self.img_id
        image['file_name'] = obj['filename']
        return image

    # 构建COCO的annotation字段
    def _annotation(self, shape):
        print(shape)
        if 'name' not in shape['region_attributes']:
            print('not name attr in shape !')
            return None
        label = shape['region_attributes']['name']
        points = list(zip(shape['shape_attributes']['all_points_x'], shape['shape_attributes']['all_points_y']))
        annotation = {}
        annotation['id'] = self.ann_id
        annotation['image_id'] = self.img_id
        print(label)
        if "house/DP" in label:
            label = "house"
        if 'blank' in label:
            return None
        annotation['category_id'] = classname_to_id[label]
        annotation['segmentation'] = [np.asarray(points).flatten().tolist()]
        annotation['bbox'] = self._get_box(points)
        annotation['iscrowd'] = 0
        annotation['area'] = 1.0
        return annotation

    # 读取json文件，返回一个json对象
    def read_jsonfile(self, path):
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)

    # COCO的格式： [x1,y1,w,h] 对应COCO的bbox格式
    def _get_box(self, points):
        min_x = min_y = np.inf
        max_x = max_y = 0
        for x, y in points:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return [min_x, min_y, max_x - min_x, max_y - min_y]


def train_test_split(data, test_size=0.12):
    n_val = int(len(data) * test_size)
    np.random.shuffle(data)
    train_data = data[:-n_val]
    val_data = data[-n_val:]
    return train_data, val_data


if __name__ == '__main__':
    # 把所有的jpg和json都放到了images目录下
    base_dir = ''
    # 获取images目录下所有的joson文件列表
    json_list_path = glob.glob(base_dir + "/*.json")

    # 数据划分,这里没有区分val2017和tran2017目录，所有图片都放在images目录下
    # train_path, val_path = train_test_split(json_list_path, test_size=0.12)
    # print("train_n:", len(train_path), 'val_n:', len(val_path))
    import os
    if not os.path.exists('annotations'):
        os.mkdir('annotations')
    # 把训练集转化为COCO的json格式
    l2c_train = Lableme2CoCo()
    train_instance = l2c_train.to_coco(json_list_path)
    l2c_train.save_coco_json(train_instance, 'annotations/coco_cunluo_part3_train.json')

    # 把验证集转化为COCO的json格式
    # l2c_val = Lableme2CoCo()
    # val_instance = l2c_val.to_coco(val_path)
    # l2c_val.save_coco_json(val_instance, 'annotations/instances_val2017.json')
