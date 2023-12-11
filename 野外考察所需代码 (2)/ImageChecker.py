'''
代码使用前，一定要将图片备份！！
LSQ 2023.12.04
'''

import PySimpleGUI as sg

import datetime

# 获取当前时间
current_time = datetime.datetime.now()

# 打印当前时间
print("当前时间：", current_time)
import shutil
import os
from PIL import Image
from PIL import ImageFile
from ExcelReader import *

list_coment = ['未显示经纬度', '车上拍摄', '拍摄马路(修路除外)', '其他问题']
comment_keys = {
    1: '未显示经纬度',
    2: '车上拍摄',
    3: '拍摄马路(修路除外)',
    4: '其他问题',
}
CITIES = ['辽阳市', '丹东市']

def jpg_to_png(file):
    if file.endswith('jpg'):
        png_path = file.replace('jpg', 'png')
        im = Image.open(file)
        im.save(png_path)
        return png_path
    elif file.endswith('png'):
        return file


def compress_image(outfile, mb=100, quality=85, k=0.9):
    """不改变图片尺寸压缩到指定大小
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB   190kb
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = os.path.getsize(outfile) // 1024
    if o_size <= mb:
        return outfile
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    while o_size > mb:
        im = Image.open(outfile)
        x, y = im.size
        out = im.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
        try:

            out.save(outfile, quality=quality)
        except Exception as e:
            print(e)
            break
        o_size = os.path.getsize(outfile) // 1024
    return outfile


def main(image_path = r'图片', problem_path=r'问题图片'):
    assert image_path.endswith('png')
    image_name = image_path.split('\\')[-1].split('.')[0]
    city = image_path.split('\\')[-3]
    district = image_path.split('\\')[-2]
    type_name = image_path.split('\\')[-4]

    sg.theme('DarkTeal6')
    # 定义按钮颜色
    sg.theme_button_color(('blue', '#6D9F85'))
    layout = [
        [sg.Text('请判断图片问题：')],
        [sg.Image(filename=image_path)],
        [sg.Radio(i, group_id=1)for i in list_coment],
        [sg.Button('确认'), sg.Button('没问题，下一张')],
    ]
    # 打印字體的顔色和背景顔色
    window = sg.Window('任务-代号J', layout)
    record_list = []
    reason = ''
    while True:
        event, values = window.read()
        # 窗口关闭事件
        if event is None:
            return None

        # 给确认按钮定义弹窗
        if event == '确认':
            for key in values:
                if values[key] is True:
                    reason = comment_keys[key]
            if len(reason) <= 0:
                sg.Popup('请选择问题内容！！')
            else:
                record_list = [image_name, type_name, "辽宁省", city, district, reason]
                make_dir(image_path.replace('TEST', 'TEST_问题图片')[:-21])
                shutil.copy(image_path, image_path.replace('TEST', 'TEST_问题图片'))
                print("问题已记录")

                # sg.Popup('问题已记录')
                break
        # 给取消按钮定义弹窗
        if event == '没问题，下一张':
            break
    window.close()
    return record_list


def make_dir(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)
    return path

import numpy as np
import gc
if __name__ == '__main__':
    root_path = r'D:\Desktop\野外\TEST'
    save_path = r'D:\Desktop\野外\TEST\记录结果表格.xlsx'
    names_path = r'D:\Desktop\野外\TEST\all_names.npy'
    problem_path = make_dir(r'D:\Desktop\野外\TEST_问题图片')
    record_lists = [['图片名称', '点位类型', '省', '市', '区/县', '原因']]

    if os.path.exists(names_path):
        all_names = np.load(names_path).tolist()
        print(all_names)
    else:
        all_names = []

    stop_flag = False
    for root, dirs, files in os.walk(root_path, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            img_name = path.split('\\')[-1].split('.')[0]
            city = path.split('\\')[-3]

            if city not in CITIES:
                continue
            if img_name in all_names:
                continue
            if not path.endswith('jpg'):
                continue
            if os.path.exists(path.replace("TEST", "TEST_问题图片").replace('jpg', 'png')):
                continue
            print(f"processing{path}")
            gc.collect()


            compress_image(path)
            path = jpg_to_png(path)
            record_list = main(path, problem_path)

            if record_list is None:
                stop_flag = True
                break
            if len(record_list) > 0:
                record_lists.append(record_list)
            all_names.append(img_name)
        if stop_flag:
            break
    print(record_lists)

    sheet_name = ''
    for ii in range(len(CITIES)):
        sheet_name += CITIES[ii]
    time_id = str(current_time.day).zfill(2)+str(current_time.hour).zfill(2)+str(current_time.minute).zfill(2)+str(current_time.second).zfill(2)

    if os.path.isfile(save_path):
        add_sheet(save_path, record_lists, sheet_name+time_id)
    else:
        write_excel_xlsx(save_path, sheet_name+time_id, record_lists)

    all_names = np.array(all_names)
    np.save(names_path, all_names)
