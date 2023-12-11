# coding=UTF-8
import pandas as pd
import os
from ExcelReader import *
from fnmatch import fnmatch

ALPHA = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L", 13: "M", 14: "N"}
SHEETNAMES = ["生态类型核查点", "动态地物核查点", "生态专题核查点"]
DIRS = {"生态类型核查点": "类型点", "动态地物核查点": "动态点", "生态专题核查点": "专题点"}
# sheet = read_excel_xlsx(r"G:\野外考察\辽宁省提交数据\核查表格\所有点位核查表格.xlsx", SHEETNAMES[0])
# for row in sheet.rows:
#     print(row[0].value)
    # for cell in row:
        # print(cell.value, "\t", end="")
    # print()

class ExcelReorganizer:
    def __init__(self, excel_path, save_path):
        self.Lengths = {}
        self.Widths = {}
        self.save_path = save_path
        self.reorganize_names_path = os.path.join(self.save_path, "Reorganize_names.xlsx")
        self.merged_path = os.path.join(self.save_path, "Merged.xlsx")
        self.leixing_sheet = read_excel_xlsx(excel_path, SHEETNAMES[0])
        self.dongtai_sheet = read_excel_xlsx(excel_path, SHEETNAMES[1])
        self.zhuanti_sheet = read_excel_xlsx(excel_path, SHEETNAMES[2])
        self.rename_all_sheets()
        # self.merge_all_sheets()

    def merge_all_sheets(self):
        wb = openpyxl.load_workbook(self.reorganize_names_path)
        self.merge_sheet(wb[SHEETNAMES[0]], SHEETNAMES[0])
        self.merge_sheet(wb[SHEETNAMES[1]], SHEETNAMES[1])
        self.merge_sheet(wb[SHEETNAMES[2]], SHEETNAMES[2])
        wb.save(self.merged_path)


    def merge_sheet(self, sheet, sheet_name):
        print(self.Lengths)
        print(self.Lengths, self.Widths)
        length = self.Lengths[sheet_name]
        width = self.Widths[sheet_name]
        for ii in range(1, length, 2):
            for jj in range(1, width):
                # print(f"{ALPHA[jj]}{ii}:{ALPHA[jj]}{ii+1}")
                sheet.merge_cells(f"{ALPHA[jj]}{ii}:{ALPHA[jj]}{ii+1}")

    def rename_all_sheets(self):
        self.rename_sheet(self.leixing_sheet, SHEETNAMES[0])
        self.rename_sheet(self.dongtai_sheet, SHEETNAMES[1])
        self.rename_sheet(self.zhuanti_sheet, SHEETNAMES[2])

    def rename_sheet(self, sheet, sheet_name):
        self.reorganize_photo_names(sheet, sheet_name)

    def get_id_corresponds(self, sheet):
        ids = []
        pre_codes = []
        corresponds = {}
        correspond_names = []
        for row in sheet.rows:
            if row[0].value == "编号":
                continue
            id_name = str(row[0].value)
            ids.append(id_name)
            pre_code = id_name[0:7]

            if pre_code not in pre_codes:
                pre_codes.append(pre_code)
                corresponds[pre_code] = 1
            else:
                corresponds[pre_code] = corresponds[pre_code] + 1

            number = str(corresponds[pre_code])
            correspond_name = f"{pre_code}{number.zfill(4)}"
            correspond_names.append(correspond_name)
        return correspond_names

    def get_photo_corresponds(self, sheet, sheet_name):
        photo_names = []
        pre_codes = []
        corresponds = {}
        correspond_names = []
        for row in sheet.rows:
            if row[-1].value == "野外相片编号":
                continue
            photo_name = row[-1].value
            photo_names.append(photo_name)
            pre_code = photo_name[0:13]

            if pre_code not in pre_codes:
                pre_codes.append(pre_code)
                corresponds[pre_code] = 1
            else:
                corresponds[pre_code] = corresponds[pre_code] + 1

            number = str(corresponds[pre_code])
            correspond_name = f"{pre_code}{number.zfill(3)}"
            correspond_names.append(correspond_name)

            photo_name.replace(" ", "")
            photo_name1 = f"{photo_name.split(',')[0]}"
            cor_name1 = f"{correspond_name}P"
            photo_name2 = photo_name1.replace("P", "T")
            cor_name2 = f"{correspond_name}T"
            print(photo_name.split(",")[0], photo_name.split(",")[1])
            for root, dirs, files in os.walk(r'G:\野外考察\辽宁省提交数据\野外照片'):
                for file in files:
                    path = os.path.join(root, file)
                    if path.split('\\')[-2] == DIRS[sheet_name]:
                        new_path = ''
                        if photo_name1 in path:
                            new_path = path.replace(photo_name1, cor_name1)
                        if photo_name2 in path:
                            new_path = path.replace(photo_name2, cor_name2)

                        if new_path != '':
                            os.rename(path, new_path)
        all_file_names = []
        problems_idx = []
        for root, dirs, files in os.walk(r'G:\野外考察\辽宁省提交数据\野外照片'):
            for file in files:
                path = os.path.join(root, file)
                if path.split('\\')[-2] == DIRS[sheet_name]:
                    all_file_names.append(file[0: -5])
        for ii in range(len(correspond_names)):
            name = correspond_names[ii]
            if name not in all_file_names:
                problems_idx.append(ii)
                # print(photo_names[ii], name, sheet_name)
        return correspond_names, problems_idx

    def reorganize_photo_names(self, sheet, sheet_name):
        id_cor_names = self.get_id_corresponds(sheet)
        photo_cor_names, problems_idx = self.get_photo_corresponds(sheet, sheet_name)
        print(problems_idx)
        new_data = []
        ii = 0
        for row in sheet.rows:

            if row[0].value == "编号":
                title = row
                ii += 1
                continue

            if problems_idx.__contains__(ii):
                ii += 1
                continue

            if ii >= len(id_cor_names):
                break

            row_list = []
            for cell in row:
                row_list.append(cell.value)
            if (sheet_name == SHEETNAMES[0]) & (len(row_list[6]) == 0):
                row_list[6] = row_list[5]
            if (sheet_name == SHEETNAMES[1]) & (len(row_list[8]) == 0):
                row_list[8] = "未知"
            row_list_ = row_list.copy()
            row_list[0] = id_cor_names[ii]
            row_list[-1] = photo_cor_names[ii]+"P"
            row_list_[0] = id_cor_names[ii]
            row_list_[-1] = photo_cor_names[ii]+"T"
            new_data += [row_list, row_list_]
            ii += 1
        self.Lengths[sheet_name] = len(new_data)
        self.Widths[sheet_name] = len(new_data[0])
        title_names = []
        for cell in title:
            title_names.append(cell.value)
        new_data.append(title_names)
        # if os.path.isfile(self.reorganize_names_path):
        #     add_sheet(self.reorganize_names_path, new_data, sheet_name)
        # else:
        #     write_excel_xlsx(self.reorganize_names_path, sheet_name, new_data)
        return

import shutil
if __name__ == '__main__':
    E = ExcelReorganizer(excel_path=r"D:\Desktop\野外\辽宁省野外核查数据\辽宁省野外核查记录表.xlsx", save_path=r'D:\Desktop\野外\辽宁省野外核查数据\表格修改')

