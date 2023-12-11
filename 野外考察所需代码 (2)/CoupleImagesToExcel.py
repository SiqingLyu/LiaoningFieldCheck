from ExcelReader import *
import os
from ReadDateNLocFromImage import *
import numpy as np
import shutil
import pandas as pd

SHEETNAMES = ["生态类型核查点", "动态地物核查点", "生态专题核查点"]
DIRS = {"生态类型核查点": "类型点", "动态地物核查点": "动态点", "生态专题核查点": "专题点"}
POINT_TYPES = {
    '1': "生态类型核查点",
    '2': "动态地物核查点",
    '4': "生态专题核查点"
}



def main(image_path, id_data, loc_data, dates, sheet_name, save_path=r''):
    lats = loc_data[:, 1]
    lons = loc_data[:, 0]
    id_olds = id_data[:, 0]
    dates = dates[:, 0]
    id_olds_base = []
    filename_base = []
    repetitive_base = {}
    datas = {}
    IF_EXIST = np.zeros(len(id_olds))

    for root, dirs, files in os.walk(image_path, topdown=False):
        for name in files:
            filepath = os.path.join(root, name)
            if name[-5] == 'P':
                continue

            # 根据名称获取信息
            img_name = name.split('.')[0]
            date_code = img_name[7:13]
            img_adcode = img_name[1:7]
            img_num = img_name[-4:-1]
            IL = ImageLoader(img_path=filepath)
            lon, lat = float(IL.lon), float(IL.lat)
            # print(filepath, name, date_code, lon, lat)

            # 根据与表格中的经纬度对比找到地理位置与该图片最接近的信息条id
            lats_diff = np.abs(lats - lat)
            lons_diff = np.abs(lons - lon)
            diff = list(lats_diff + lons_diff)
            # print(min(diff))
            min_index = diff.index(min(diff))
            id_old = id_olds[min_index]
            date = dates[min_index]
            if date != date_code:
                continue
            id_num = '0' + img_num
            # print(IF_EXIST)
            # 判断该信息条是否已经出现过
            if IF_EXIST[min_index] >= 1:
                # print(f"{filepath}在{id_old}点位上和{filename_base[id_olds_base.index(id_old)]}重复了。")
                if id_old in repetitive_base.keys():
                    repetitive_base[id_old].append(filepath)
                else:
                    repetitive_base[id_old] = [filepath, filename_base[id_olds_base.index(id_old)]]

            excel_new_id = f"M{img_adcode}{date_code}{img_num}"
            if id_old in datas.keys():
                if excel_new_id in datas[id_old]:
                    print(f"此处似乎有图片重名：{sheet_name}的{name}")
                datas[id_old] += [excel_new_id]
            else:
                datas[id_old] = [excel_new_id]

            IF_EXIST[min_index] += 1  # 对应位置信息条使用次数加一
            id_olds_base.append(id_old)
            filename_base.append(filepath)

    # 将重新设计的点位编号一一对应到原始编号上
    data_out = [['原始id', '根据图片得到的新id']]
    for id_old in id_olds:
        excel_new_id_flag = ''
        if id_old in datas.keys():
            excel_new_id_flag = datas[id_old]
        data_out.append([id_old, str(excel_new_id_flag)])

    # 保存文件
    if os.path.isfile(save_path):
        add_sheet(save_path, data_out, sheet_name)
    else:
        write_excel_xlsx(save_path, sheet_name, data_out)


def read_excel_to_list(excel_path, sheet_name):
    id_list = []
    loc_list = []
    date_list = []
    sheet = read_excel_xlsx(excel_path, sheet_name)
    for row in sheet.rows:
        if row[0].value == "编号":
            continue
        else:
            id_old = str(row[0].value)
            lon = float(row[2].value)
            lat = float(row[3].value)
            date = str(row[1].value)
            date = f"23{date.split('.')[1]}{date.split('.')[2]}"
            id_list.append([id_old])
            loc_list.append([lon, lat])
            date_list.append([date])
    return np.array(id_list), np.array(loc_list), np.array(date_list)


if __name__ == '__main__':
    image_path = r'D:\Desktop\野外\辽宁省野外核查数据\野外核查照片'
    excel_path = r'D:\Desktop\野外\辽宁省野外核查数据\辽宁省野外核查记录表.xlsx'
    save_path = r'D:\Desktop\野外\辽宁省野外核查数据\表格修改\Test1.xlsx'
    if os.path.exists(save_path):
        os.remove(save_path)
    for name in SHEETNAMES:
        img_path = os.path.join(image_path, name)
        id_data, loc_data, dates = read_excel_to_list(excel_path, name)
        main(img_path, id_data, loc_data, dates, name, save_path)