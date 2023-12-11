from ExcelReader import *
import os
from ReadDateNLocFromImage import *
import numpy as np
import shutil
import pandas as pd

# SHEETNAMES = ["生态类型核查点", "动态地物核查点", "生态专题核查点"]
SHEETNAMES = ["动态地物核查点"]
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
    id_news = id_data[:, 1]
    path_names = [[]]*len(id_news)
    img_names = []
    img_paths = []
    img_poses = []

    for root, dirs, files in os.walk(image_path, topdown=False):
        for name in files:
            filepath = os.path.join(root, name)
            if name[-5] == 'P':
                continue
            # 根据名称获取信息
            img_name = name.split('.')[0]
            IL = ImageLoader(img_path=filepath)
            img_lon, img_lat = float(IL.lon), float(IL.lat)
            img_pos = [img_lon, img_lat]
            img_names.append(img_name)
            img_poses.append(img_pos)
            img_paths.append(filepath)
    img_poses=np.array(img_poses)

    for ii in range(len(id_olds)):
        # if len(str(id_news[ii])) > 0:
        #     continue
        id_old = id_olds[ii]
        id_new = id_news[ii]
        lon, lat = lons[ii], lats[ii]
        lon_diff = np.abs(img_poses[:, 0] - lon)
        lat_diff = np.abs(img_poses[:, 1] - lat)
        diff = list(lon_diff + lat_diff)
        min_index = diff.index(min(diff))
        image_name = img_names[min_index]
        img_path = img_paths[min_index]
        date_code = image_name[7:13]
        img_adcode = image_name[1:7]
        img_num = image_name[-4:-1]
        supposed_id = f"M{img_adcode}{date_code}{img_num}"
        if
        id_news[ii] = f"['{supposed_id}']"
        path_names[ii] = img_path

    data_out = [['原始id', '根据图片得到的新id', '需要转移的图片所在位置']]
    for ii in range(len(id_olds)):
        data_out.append([id_olds[ii], id_news[ii][2:-2], path_names[ii]])
    # 保存文件
    if os.path.isfile(save_path):
        add_sheet(save_path, data_out, sheet_name)
    else:
        write_excel_xlsx(save_path, sheet_name, data_out)


    # 保存文件
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
            id_new = str(row[10].value) if row[10].value is not None else ''
            lon = float(row[2].value)
            lat = float(row[3].value)
            date = str(row[1].value)
            date = f"23{date.split('.')[1]}{date.split('.')[2]}"
            id_list.append([id_old, id_new])
            loc_list.append([lon, lat])
            date_list.append([date])
    return np.array(id_list), np.array(loc_list), np.array(date_list)


if __name__ == '__main__':
    image_path = r'G:\分配后野外图片'
    excel_path = r'D:\Desktop\野外\辽宁省野外核查数据\辽宁省野外核查记录表.xlsx'
    save_path = r'D:\Desktop\野外\辽宁省野外核查数据\表格修改\Test2.xlsx'
    if os.path.exists(save_path):
        os.remove(save_path)
    for name in SHEETNAMES:
        id_data, loc_data, dates = read_excel_to_list(excel_path, name)
        main(image_path, id_data, loc_data, dates, name, save_path)