#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import os
import numpy as np
from ExcelReader import *

"""
此代码用于将地区对应的专题点的属性表（txt格式）转化为一个表格，
表格每一行有两列，第一列是点位的名字
"""


def main(txt_path, save_path):
    df = pd.read_csv(txt_path, sep=',', encoding='utf-8')
    point_ids = df["编号"]
    cities = df["市"]
    disaster_types = df["灾害活动类"]
    land_types = df["地貌类型"]
    B_types = df["变化前类型"]
    A_types= df["变化后类型"]
    altitudes = df["海拔（米）"]
    lontitudes = df["经度（度）"]
    latitudes = df["纬度（度）"]
    during_time = df["持续时间"]
    affect_range = df["影响范围"]
    dates = df["日期"]
    datas = []
    datas.append(['编号', '经度', '纬度', '描述'])

    for ii in range(len(point_ids)):
        point_id = str(int(np.round(point_ids[ii])))
        date = dates[ii].split(' ')[0]
        adcode = point_id[1:7]
        img_num = point_id[-3:]
        year, month, day = date.split('/')[0][-2:], date.split('/')[1].zfill(2), date.split('/')[2].zfill(2)
        image_name = [f"M{adcode}{year}{month}{day}{img_num}P", f"M{adcode}{year}{month}{day}{img_num}T"]
        description = f"此站点位于辽宁省{cities[ii]}，其对应活动类型是：{disaster_types[ii]}，" \
                      f"具体地理位置：东经{lontitudes[ii]}度，北纬{latitudes[ii]}度，海拔{altitudes[ii]}米," \
                      f"地貌为{land_types[ii]}，在发生此活动之前，生态类型是{B_types[ii]}，" \
                      f"变化后的生态类型变为{A_types[ii]}，影像范围约{affect_range[ii]}，持续时间约{during_time[ii]}。"
        print(description)
        print(image_name)
        datas.append([point_id, lontitudes[ii], latitudes[ii], description])


    write_excel_xlsx(save_path, 'sheet1', datas)

if __name__ == '__main__':
    # txt文件来源于由奥维地图的SHP文件点数据在arcmap上导出的属性表结果
    # 其中，奥维地图的点数据不会记录海拔，建议全部工作完成之后由DEM数据给对应点位在arcmap上进行赋值，字段命名为“Altitude”
    main(txt_path = r'G:\野外考察\专题点分市\Dandong.txt', save_path = r'DandongZhuanti.xlsx')
