# coding=UTF-8
import pandas as pd
import os
from ExcelReader import *
from fnmatch import fnmatch
from CoordPos import *
import time
import threading

'''
此代码用于将错误标定的图片序号重新标定。
'''

ALPHA = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L"}
SHEETNAMES = ["生态类型核查点", "动态地物核查点", "生态专题核查点"]
DIRS = {"生态类型核查点": "类型点", "动态地物核查点": "动态点", "生态专题核查点": "专题点"}
POINT_TYPES = {
    '1': "生态类型核查点",
    '2': "动态地物核查点",
    '4': "生态专题核查点"
}
# sheet = read_excel_xlsx(r"G:\野外考察\辽宁省提交数据\核查表格\所有点位核查表格.xlsx", SHEETNAMES[0])
# for row in sheet.rows:
#     print(row[0].value)
    # for cell in row:
        # print(cell.value, "\t", end="")
    # print()

def get_adcode(lon, lat):
    position = Coord2Pos(lon, lat)
    # print(lon, lat)
    # print(position)
    if position is None:
        # print(f"{lat},{lon}")
        # print(position)
        return 'None'
    else:
        # print(position)
        loc = str(position['adcode'])
    return loc

class ExcelReorganizer:
    def __init__(self, excel_path, save_path):
        self.Lengths = {}
        self.Widths = {}
        self.save_path = save_path
        self.re_identify_path = os.path.join(self.save_path, "Reorganize_names.xlsx")
        self.leixing_sheet = read_excel_xlsx(excel_path, SHEETNAMES[0])
        self.dongtai_sheet = read_excel_xlsx(excel_path, SHEETNAMES[1])
        self.zhuanti_sheet = read_excel_xlsx(excel_path, SHEETNAMES[2])
        self.re_identify_sheets()

    def re_identify_sheets(self):
        self.re_identify_ids(self.leixing_sheet)
        self.re_identify_ids(self.dongtai_sheet)
        self.re_identify_ids(self.zhuanti_sheet)

    def re_identify_ids(self, sheet):
        data = [["旧编号", "新编号"]]
        point_type = 'UNKNOWN'
        for row in sheet.rows:
            if row[0].value == "编号":
                continue
            else:
                id_old = str(row[0].value)
                id_new = ''

                adcode_old = id_old[1:7]
                point_type = POINT_TYPES[id_old[0]]
                lon = str(row[2].value)
                lat = str(row[3].value)
                # print(id, point_type, adcode_old, lon, lat)
                loc = get_adcode(lon, lat)
                if loc == 'None':
                    data.append([id_old, id_new])
                    continue
                # district = position['district']
                # city = position['city']
                # town = position['town']
                if loc != adcode_old:
                    adcode_new = loc
                    id_new = f"{id_old[0]}{adcode_new}{id_old[-4:]}"
                    print(id_old, loc, id_new)
                data.append([id_old, id_new])
        if os.path.isfile(self.re_identify_path):
            add_sheet(self.re_identify_path, data, point_type)
        else:
            write_excel_xlsx(self.re_identify_path, point_type, data)


import shutil
if __name__ == '__main__':
    E = ExcelReorganizer(excel_path=r"D:\Desktop\野外\辽宁省野外核查数据\辽宁省野外核查记录表.xlsx", save_path=r'D:\Desktop\野外\辽宁省野外核查数据\表格修改')

