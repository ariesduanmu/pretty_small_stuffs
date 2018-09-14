# -*- coding: utf-8 -*-
# @Author: Li Qin
# @Date:   2018-09-14 11:07:32
# @Last Modified by:   Li Qin
# @Last Modified time: 2018-09-14 14:10:20
import pinyin
import pandas as pd

'''
读取xls文件中的姓名信息,并且返回拼音缩写
'''

def parse_xls(xls_file, sheet_number, column_name):
    '''
    Parse xls file, get info from the (sheet_number) sheet, in column (column_name)
    
    Args:
        xls_file: xls file path
        sheet_number: target sheet
        column_name: target column name

    Returns:
        target data
    '''
    wb = pd.ExcelFile(xls_file)
    info_sheet = wb.parse(sheet_number)
    return info_sheet[column_name]

def ccharacter_2_pinyin(ccharacter):
    '''
    Convert Chinese character into the combination of it's first pinyin letters
    '''
    py = pinyin.get(ccharacter, format="strip", delimiter=" ").split(" ")
    return "".join(p[0] for p in py)

def main(xls_file, sheet_number, column_name):
    infos = parse_xls(xls_file, sheet_number, column_name)
    return [[info, ccharacter_2_pinyin(info)] for info in infos]

