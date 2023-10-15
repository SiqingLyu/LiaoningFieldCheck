#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
from CoordPos import *
from ExcelReader import *
import os
"""
此代码用于将shp的属性表（txt）格式文件转换为提交所需的Excel，可以将所有的点放在一起转换位txt，
不用按区县分类，代码可以自行处理
"""

DYNAMICWORLDCLASS = ["水体", "有林地", "草地", "水田", "耕地", "灌木林", "建筑用地", "裸地", "裸地"]


def get_adcode(lon, lat):
    position = Coord2Pos(lon, lat)
    loc = position['adcode']
    return loc


class ExcelMaker:
    def __init__(self, df, savepath):
        self.savepath = savepath

        self.names = df['O_Name']
        self.lats = df['O_Lat']
        self.lons = df['O_Lng']
        self.dates = df['Date']
        self.land_types = df['LandType']

        self.alts = None
        self.alts = df['elevation']

        # 第一类调查，类型核查点地物类型
        self.land_types = df['LandType']
        self.field_types = df['FieldType']

        # 第二类调查，动态点变化前后类型
        self.befores = df['label']
        self.afters = df['A_land']
        self.causes = df['Cause']

        # 第三类调查，草原植被覆盖核查
        self.coverages = df['VCoverage']
        self.directions = df['Direction']
        self.cover_percentages = df['PCoverage']

        # 第四类调查，专题点的灾害活动类型、持续天数、影响范围，变化前后类型
        self.diseases = df['Disa_Type']
        self.durations = df['Duration']
        self.ranges = df['Range']
        self.before_diseases = df['B_disa']
        self.after_diseases = df['A_disa']

        self.len = len(df['FID'])

        self.first_sheet = '生态类型核查点'
        self.second_sheet = '动态地物核查点'
        self.thrid_sheet = '草原覆盖度核查点'
        self.fourth_sheet = '生态专题核查点'

        self.make_sheets_first_type()
        self.make_sheets_second_type()
        self.make_sheets_third_type()
        self.make_sheets_fourth_type()

    def make_sheets_first_type(self):
        datas = []
        datas.append(['编号', '日期', '经度（度）', '纬度（度）', '海拔（米）', '地貌类型', '野外类型', '判读类型', '正/误', '野外相片编号'])
        for ii in range(self.len):
            name = str(self.names[ii])

            type_of_data = name[0]
            if type_of_data != '1':
                continue

            date = self.dates[ii]
            lon = self.lons[ii]
            lat = self.lats[ii]
            alt = self.alts[ii] if self.alts is not None else 0
            l_type = self.land_types[ii]
            f_type = self.field_types[ii]
            judge = ''
            R_W = ''
            loc = get_adcode(lon, lat)

            number = f'{type_of_data}{loc}{name[1:]}'
            date_6_code = date.split('-')[0][-2:]+date.split('-')[1]+date.split('-')[2]
            image_names = f'M{loc}{date_6_code}{name[-4:]}P, M{loc}{date_6_code}{name[-4:]}T'

            data = [number, date, lon, lat, alt, l_type, f_type, judge, R_W, image_names]
            datas.append(data)

            write_excel_xlsx(self.savepath, self.first_sheet, datas)

    def make_sheets_second_type(self):
        datas = []
        datas.append(['编号', '日期', '经度（度）', '纬度（度）', '海拔（米）', '地貌类型', '变化前类型', '变化后类型', '变化原因', '野外相片编号'])
        for ii in range(self.len):
            name = str(self.names[ii])

            type_of_data = name[0]
            if type_of_data != '2':
                continue

            date = self.dates[ii]
            lon = self.lons[ii]
            lat = self.lats[ii]
            alt = self.alts[ii] if self.alts is not None else 0
            l_type = self.land_types[ii]
            before = DYNAMICWORLDCLASS[int(self.befores[ii])]
            after = self.afters[ii]
            cause = self.causes[ii]

            loc = get_adcode(lon, lat)

            number = f'{type_of_data}{loc}{name[1:]}'
            date_6_code = date.split('-')[0][-2:]+date.split('-')[1]+date.split('-')[2]
            image_names = f'M{loc}{date_6_code}{name[-4:]}P, M{loc}{date_6_code}{name[-4:]}T'

            data = [number, date, lon, lat, alt, l_type, before, after, cause, image_names]
            datas.append(data)

        if os.path.isfile(self.savepath):
            add_sheet(self.savepath, datas, self.second_sheet)
        else:
            write_excel_xlsx(self.savepath, self.second_sheet, datas)

    def make_sheets_third_type(self):
        '''
        辽宁省不需要这个
        '''
        pass

    def make_sheets_fourth_type(self):
        datas = []
        datas.append(['编号', '日期', '经度（度）', '纬度（度）', '海拔（米）', '地貌类型', '变化前类型', '变化后类型', '灾害活动类型', '持续时间', '影响范围', '野外相片编号'])
        for ii in range(self.len):
            name = str(self.names[ii])

            type_of_data = name[0]
            if type_of_data != '4':
                continue

            date = self.dates[ii]
            lon = self.lons[ii]
            lat = self.lats[ii]
            alt = self.alts[ii] if self.alts is not None else 0
            l_type = self.land_types[ii]
            b_disease = self.before_diseases[ii]
            a_disease = self.after_diseases[ii]
            disease_type = self.diseases[ii]
            duration_ = self.durations[ii]
            range_ = self.ranges[ii]

            loc = get_adcode(lon, lat)

            number = f'{type_of_data}{loc}{name[1:]}'
            date_6_code = date.split('-')[0][-2:]+date.split('-')[1]+date.split('-')[2]
            image_names = f'M{loc}{date_6_code}{name[-4:]}P, M{loc}{date_6_code}{name[-4:]}T'

            data = [number, date, lon, lat, alt, l_type, b_disease, a_disease, disease_type, duration_, range_, image_names]
            datas.append(data)
        if os.path.isfile(self.savepath):
            add_sheet(self.savepath, datas, self.fourth_sheet)
        else:
            write_excel_xlsx(self.savepath, self.fourth_sheet, datas)


def main(txt_path, save_path):
    df = pd.read_csv(txt_path, sep=',', encoding='utf-8')
    ExcelMaker(df=df, savepath=save_path)


if __name__ == '__main__':
    # txt文件来源于由奥维地图的SHP文件点数据在arcmap上导出的属性表结果
    # 其中，奥维地图的点数据不会记录海拔，建议全部工作完成之后由DEM数据给对应点位在arcmap上进行赋值，字段命名为“Altitude”
    main(txt_path = r'G:\野外考察\所有点位信息.txt', save_path = r'Test1.xlsx')