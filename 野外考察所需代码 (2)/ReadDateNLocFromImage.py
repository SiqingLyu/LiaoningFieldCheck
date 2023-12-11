#!/usr/bin/env python
# -*- coding:utf-8 -*-
import exifread
from CoordPos import *

"""
此代码用于利用百度地图API从原图图像中读取日期位置等数据，并按照要求完成图像的命名
"""


def format_lati_long(data):
    list_tmp=str(data).replace('[', '').replace(']', '').split(',')
    list_ = [ele.strip() for ele in list_tmp]
    data_sec = int(list_[-1].split('/')[0]) /(int(list_[-1].split('/')[1])*3600)# 秒的值
    data_minute = int(list_[1])/60
    data_degree = int(list_[0])
    result=data_degree + data_minute + data_sec
    return result


class ImageLoader:
    def __init__(self, img_path):
        self.img_path = img_path
        self.init_data()

    def init_data(self):
        img = exifread.process_file(open(self.img_path, 'rb'))
        if 'Image DateTime' in img.keys():
            self.datetime = str(img['Image DateTime'])
        else:
            self.datetime = str(img['EXIF DateTime'])

        latitude = format_lati_long(str(img['GPS GPSLatitude']))
        longitude = format_lati_long(str(img['GPS GPSLongitude']))
        self.lat = latitude
        self.lon = longitude
        # self.get_all()


    def get_datetime(self):
        return self.datetime

    def get_date(self):
        date_temp = self.datetime.split(' ')[0]
        self.date = str(date_temp.split(':')[0][-2:]) + str(date_temp.split(':')[1]) + str(date_temp.split(':')[2])
        return self.date

    def get_loc(self):
        position = Coord2Pos(self.lon, self.lat)
        self.district = position['district']
        self.city = position['city']
        self.town = position['town']
        self.loc = position['adcode']
        return self.loc

    def get_pos(self):
        return [self.lat, self.lon]

    def get_all(self):
        self.get_pos()
        self.get_date()
        self.get_loc()
        self.get_datetime()

    def print_info(self):
        print(f"The image locates at {self.lat, self.lon}, shot on {self.date}, specific time is {self.datetime}, adcode is {self.loc}")

    def name_the_image(self):
        '''
        注意： 10001指的是第一类核查点的第1张影像，
        10001_1代表这是一张全景影像（P），10001_2代表这是一张典型地物影像(T)
        本函数根据文件名自动得到命名，得到18位编码
        注意：每个县的点位编号都要从0001开始编起。
        :return:
        '''
        filename = self.img_path.split('\\')[-1].split('(')[0]
        number = filename.split('_')[0][-4:]
        P_or_T = 'P' if filename.split('_')[-1] == '1' else 'T'
        image_name = 'M' + f'{self.loc}{self.date}{number}{P_or_T}'
        return image_name


if __name__ == '__main__':
    I = ImageLoader(img_path=r'C:\Users\29010\Desktop\10002_1(6531693082115049854).jpg')
    I.print_info()
    print("The name of the image should be:", I.name_the_image())