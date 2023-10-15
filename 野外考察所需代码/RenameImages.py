#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
这个代码用于将一个文件夹下面所有的图片根据所在县区位置分类放置，图片的已有命名格式应当为：
第一位为核查点类型：1，2，或者4
2-5位是同一区县下的图片编号：如0001
后面跟着的是奥维地图自动生成的ID，这个不用管，在ReadDateNLocFromImage中已经考虑此问题。
"""
import os
import shutil
from ReadDateNLocFromImage import *



def make_dirs(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)
    return path


def rename_single_image(image_path):
    pass


def main(ori_path, target_path):
    make_dirs(target_path)
    for root, dirs, files in os.walk(ori_path, topdown=False):
        for name in files:
            filepath = os.path.join(root, name)
            type_name = name.split('_')[0][0]

            type_path = 'unknown'  # init
            if type_name == '1':
                type_path = '类型点'
            elif type_name == '2':
                type_path = '动态点'
            elif type_name == '3':
                type_path = '覆盖点'
            elif type_name == '4':
                type_path = '专题点'

            IL = ImageLoader(img_path=filepath)
            image_new_name = IL.name_the_image() + '.jpg'
            # adcode = str(IL.get_loc())  # 县区代码，这里选择县区名字命名文件夹，故不需要这个
            district = IL.district
            save_district_path = make_dirs(os.path.join(target_path, district, type_path))
            print(filepath, os.path.join(save_district_path, image_new_name))
            shutil.copyfile(filepath, os.path.join(save_district_path, image_new_name))

if __name__ == '__main__':
    main(ori_path=r'G:\野外照片\野外照片', target_path=r'G:\野外照片\辽阳丹东')