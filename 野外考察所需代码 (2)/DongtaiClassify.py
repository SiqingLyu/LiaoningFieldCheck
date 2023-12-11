import os
from ExcelReader import *
excel_path = r'D:\Desktop\野外\辽宁省野外核查数据\辽宁省野外核查记录表.xlsx'
sheet = read_excel_xlsx(excel_path, sheet_name="Sheet1")
classify = [['归类后变化原因']]
CLASS_KEYWORD_DICT = {
    '光伏建设': ["光伏"],
    '伐木活动': ["伐", "砍"],
    '水文活动': ["河", "坝"],
    '自然灾害': ["雪", "滑坡", "泥石流"],
    '生态建设': ["公园", "花海", "风车", "风力", "绿化", "种植树木", "退耕还林", "植树"],
    '作物种植': ["种", "玉米", "耕地", "开垦", "农田", "耕"],
    '农村建设': ["大棚", "畜牧", "草场", "农民", "棚户", "鱼塘", "水产", "池塘", "晒粮食"],
    '采石采砂': ["挖土", "沙", "采"],
    '自然生长': ["长", "自然", "荒", "生态修复", "恢复"],
    '拆除废弃': ["拆", "弃", "中断"],
    '堆放活动': ["堆", "待开发", "石材", "石头"],
    '修路活动': ["道路", "桥", "高速", "路", "涵洞"],
    '建筑建设': ["盖", "停车场", "篮球场", "公司", "建设", "房", "楼", "加油站", "工", "厂", "建", "小区"],
    '其他活动': ['未知', '']
}


for row in sheet.rows:
    stop_flag = False

    if row[0].value == "变化原因":
        continue
    elif row[0].value is not None:
        reason = row[0].value
        for key in CLASS_KEYWORD_DICT.keys():
            class_keywords = CLASS_KEYWORD_DICT[key]

            for keyword in class_keywords:
                if keyword in reason:
                    classify.append([key])
                    stop_flag = True
                    break

            if stop_flag:
                break
    else:
        continue

import shutil

write_excel_xlsx(r'动态点变化归类表.xlsx', sheet_name='sheet1', value=classify)