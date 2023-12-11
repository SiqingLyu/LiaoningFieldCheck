from ExcelReader import *
import os
from ReadDateNLocFromImage import *
import numpy as np
import shutil
import pandas as pd
from ExcelLoader import *
TYPE_COR = {
    "耕地": ["旱地"],
    "灌木林": ["灌木林"],
    "建筑用地": ["城镇用地"],
    "裸地": ["裸土地"],
    "有林地": ["有林地"],
    "水体": ["水库坑塘"],
    "水田": ["水田"]
}

JUDGE_COR = {
    "城镇用地": ["城镇用地", "其他建设用地"],
    "灌木林": ["灌木林", "有林地"],
    "疏林地": ["有林地", "疏林地"],
    "旱地": ["旱地"],
    "湖泊": ["水库坑塘", "湖泊"],
    "水体": ["水库坑塘"],
    "水田": ["水田"],
    "高覆盖度草地": ["高覆盖度草地"],
    "河渠": ["河渠"],
    "裸土地": ["裸土地"],
    "裸岩石砾地": ["裸岩石砾地"],
    "农村居民点": ["农村居民点"],
    "其他建设用地": ["其他建设用地", "城镇用地"],
    "其他未利用地": ["其他未利用地", "裸土地", "裸岩石砾地"],
    "水库坑塘": ["水库坑塘"],
    "滩地": ["河渠", "滩地"],
    "有林地": ["有林地", "其他林地", "灌木林", "疏林地"],
    "中覆盖度草地": ["高覆盖度草地", "中覆盖度草地"],
    "低覆盖度草地": ["低覆盖度草地", "中覆盖度草地"],
    "海域": ["海域"],
    "滩涂": ["滩涂", "河渠"],

}


def get_dongtai_acc(el: ExcelLoader = None):
    before_types = el.data_dict["变化前类型"]
    after_types = el.data_dict["变化后类型"]
    judges = np.zeros_like(after_types)
    same_num = 0
    amount = len(before_types)
    for ii in range(amount):
        before_type = before_types[ii]
        after_type = after_types[ii]
        if after_type in TYPE_COR[before_type]:
            same_num += 1
            judges[ii] = "未变化"
        else:
            judges[ii] = "变化"

    acc = (amount - same_num) / amount
    el.data_dict["是否变化"] = judges
    return np.round(acc, 6), el


def get_dongtai_acc_for_each(el: ExcelLoader = None):
    land_types = el.data_dict["地貌类型"]
    if_changes = el.data_dict["是否变化"]
    land_nums = {}
    for ii in range(len(land_types)):
        land_type = land_types[ii]
        if_change = if_changes[ii]
        if land_type not in land_nums.keys():
            land_nums[land_type] = 0
        if if_change == '变化':
            land_nums[land_type] += 1
    list_out = [['地貌类型', '变化识别正确率']]
    land_types = np.array(land_types)
    for key in land_nums.keys():
        if len(land_types[land_types==key]) <= 3:
            continue
        acc = land_nums[key] / len(land_types[land_types==key])
        print(acc)

        list_out.append([key, acc])
    return list_out


def get_leixing_acc_for_each(el: ExcelLoader = None):
    land_types = el.data_dict["地貌类型"]
    if_changes = el.data_dict["正/误"]
    land_nums = {}
    for ii in range(len(land_types)):
        land_type = land_types[ii]
        if_change = if_changes[ii]
        if land_type not in land_nums.keys():
            land_nums[land_type] = 0
        if if_change == '正':
            land_nums[land_type] += 1
    list_out = [['地貌类型', '类型识别正确率']]
    land_types = np.array(land_types)
    for key in land_nums.keys():
        acc = land_nums[key] / len(land_types[land_types==key])
        print(acc)
        list_out.append([key, acc])
    return list_out


def get_leixing_acc_and_rewrite(el: ExcelLoader = None):
    land_types = el.data_dict["地貌类型"]
    judge_types = el.data_dict["判读类型"]
    judges = np.zeros_like(land_types)
    same_num = 0
    nodata_num = 0
    amount = len(land_types)
    for ii in range(amount):
        land_type = land_types[ii]
        judge_type = judge_types[ii]
        if judge_type == "无数据":
            nodata_num += 1
            judges[ii] = "误"

            continue
        if judge_type in JUDGE_COR[land_type]:
            same_num += 1
            judges[ii] = "正"
            judge_types[ii] = land_type
        else:
            judges[ii] = "误"
    acc = same_num / (amount - nodata_num)
    el.data_dict["判读类型"] = judge_types
    el.data_dict["正/误"] = judges
    return np.round(acc, 6), el


if __name__ == '__main__':
    EL = ExcelLoader(excel_path=r'D:\Desktop\野外\辽宁省野外核查数据\辽宁省野外核查记录表.xlsx', sheet_name="动态地物核查点")
    # acc, EL = get_leixing_acc_and_rewrite(EL)
    acc, EL = get_dongtai_acc(EL)
    EL_new = pd.DataFrame(EL.data_dict)
    # EL_new.to_excel("Test_rewriteleixing.xlsx", index=False)
    EL_new.to_excel("Test_rewritDongtai.xlsx", index=False)

    # EL = ExcelLoader(excel_path=r'D:\Desktop\野外\辽宁省野外核查数据\辽宁省野外核查记录表 - 副本 (8).xlsx', sheet_name="类型点判读情况")
    # list_out = get_leixing_acc_for_each(EL)
    # write_excel_xlsx("Test_leixingacc_foreach.xlsx","acc", list_out)

    # print(acc)