# coding=UTF-8
import pandas as pd
import os
from ExcelReader import *
from fnmatch import fnmatch
from ExcelLoader import *

ALPHA = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L"}
SHEETNAMES = ["生态类型核查点", "动态地物核查点", "生态专题核查点"]
# SHEETNAMES = ["生态类型核查点", "动态地物核查点"]
DIRS = {"生态类型核查点": "类型点", "动态地物核查点": "动态点", "生态专题核查点": "专题点"}
Length = {
    "生态类型核查点": 451,
    "动态地物核查点": 1403,
    "生态专题核查点": 155
}
Width = {
    "生态类型核查点": 10,
    "动态地物核查点": 10,
    "生态专题核查点": 12
}

def rewrite_Images(el: ExcelLoader = None):
    image_names = el.data_dict["根据图片得到的新id"]
    for ii in range(len(image_names)):
        image_name = image_names[ii][2:-2]
        image_names[ii] = f"{image_name}P"
    print(image_names)
    el.data_dict["根据图片得到的新id"] = image_names
    return el.data_dict


def merge_cells(sheet, sheet_name):
    length = Length[sheet_name]
    width = Width[sheet_name]
    for ii in range(2, length, 2):
        for jj in range(1, width):
            print(f"{ALPHA[jj]}{ii}:{ALPHA[jj]}{ii + 1}")
            sheet.merge_cells(f"{ALPHA[jj]}{ii}:{ALPHA[jj]}{ii + 1}")


import shutil
if __name__ == '__main__':

    # for sheet in SHEETNAMES:
    #     EL = ExcelLoader(excel_path=r'D:\Desktop\野外\辽宁省野外核查数据\辽宁省野外核查记录表 - 副本 (9).xlsx', sheet_name=sheet)
    #     data_dict = rewrite_Images(EL)
    #     E_new = pd.DataFrame(data_dict)
    #     E_new.to_excel(f"{sheet}_imageRe.xlsx", index=False)
    wb = openpyxl.load_workbook(r'D:\Desktop\野外\辽宁省野外核查数据\辽宁省野外核查记录表.xlsx')
    for sheet in SHEETNAMES:
        sheet_data = merge_cells(wb[sheet], sheet)
    wb.save(r'辽宁省野外核查记录表_new.xlsx')
