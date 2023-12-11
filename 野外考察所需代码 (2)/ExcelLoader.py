from ExcelReader import *
import os
from ReadDateNLocFromImage import *
import numpy as np
import shutil
import pandas as pd
SHEETNAMES = ["生态类型核查点", "动态地物核查点", "生态专题核查点"]
SHEETCOLOMNS = {
    "生态专题核查点": ['编号', '日期', '经度（度）', '纬度（度）', '海拔（米）', '地貌类型', '变化前类型', '变化后类型',
                '灾害活动类型', '持续时间', '影响范围', '原始id', '根据图片得到的新id'],
    "动态地物核查点": ['编号', '日期', '经度（度）', '纬度（度）', '海拔（米）', '地貌类型', '变化前类型', '变化后类型',
                '变化原因', '原始id', '根据图片得到的新id'],
    "生态类型核查点": ['编号', '日期', '经度（度）', '纬度（度）', '海拔（米）', '地貌类型', '野外类型', '判读类型',
                '正/误', '原始id', '根据图片得到的新id'],
    "动态点判读情况": ["地貌类型", "是否变化"],
    "类型点判读情况": ["地貌类型", "正/误"]
}


class ExcelLoader:
    def __init__(self, excel_path:str = None, sheet_name:str = None):
        if excel_path.endswith('xls'):
            self.data = read_excel_xls(excel_path, sheet_name)
        else:
            self.data = read_excel_xlsx(excel_path, sheet_name)
        self.data_init(sheet_name)

    def data_init(self, name):
        self.data_dict = {}
        self.caps = SHEETCOLOMNS[name]
        for cap in self.caps:
            self.data_dict[cap] = []
        self.get_arr()

    def get_arr(self):
        for row in self.data.rows:
            if (row[0].value == "编号") | (row[0].value == "地貌类型") :
                continue
            else:
                for ii in range(len(self.caps)):
                    cap = self.caps[ii]
                    self.data_dict[cap].append(row[ii].value)
        # for cap in self.caps:
        #     self.data_dict[cap] = np.array(self.data_dict[cap])


if __name__ == '__main__':
    EL = ExcelLoader(excel_path=r'D:\Desktop\野外\辽宁省野外核查数据\辽宁省野外核查记录表.xlsx', sheet_name="动态地物核查点")
    print(EL.data_dict)
