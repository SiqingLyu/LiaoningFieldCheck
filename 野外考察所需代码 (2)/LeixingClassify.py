import os
from ExcelReader import *
excel_path = r'D:\Desktop\野外\辽宁省野外核查数据\辽宁省野外核查记录表.xlsx'
sheet = read_excel_xlsx(excel_path, sheet_name="Sheet4")
classify = [['归类后一级类型']]
CLASS_KEYWORD_DICT = {
    '耕地': ["水田", "旱地"],
    '林地': ["有林地", "灌木林", "疏林地", "其他林地"],
    '草地': ["高覆盖度草地", "中覆盖度草地", "低覆盖度草地"],
    '水域': ["河渠", "湖泊", "水库坑塘", "永久性冰川雪地", "滩涂", "滩地", "海域"],
    '城乡、工矿、居民用地': ["城镇用地", "农村居民点", "其他建设用地"],
    '未利用土地': ["沙地", "戈壁", "盐碱地", "沼泽地", "裸土地", "裸岩石砾地", "其他"]
}


for row in sheet.rows:
    stop_flag = False

    if row[0].value == "地貌类型":
        continue
    elif row[0].value is not None:
        d_type = row[0].value
        for key in CLASS_KEYWORD_DICT.keys():
            class_keywords = CLASS_KEYWORD_DICT[key]
            if d_type in class_keywords:
                classify.append([key])
                stop_flag = True
                break

            if stop_flag:
                break
    else:
        continue

import shutil

write_excel_xlsx(r'类型点变化归类表.xlsx', sheet_name='sheet1', value=classify)