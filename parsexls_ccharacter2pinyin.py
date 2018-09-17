# -*- coding: utf-8 -*-
# @Author: Li Qin
# @Date:   2018-09-14 11:07:32
# @Last Modified by:   Li Qin
# @Last Modified time: 2018-09-17 16:16:55
import os
import re
import sys
import pinyin
import pandas as pd
import argparse

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

def main(xls_file, sheet_number, column_name, filter_chars=[]):
    infos = parse_xls(xls_file, sheet_number, column_name)
    filtered_infos = set()
    for info in infos:
        filtrate = re.compile(u'[^\u4E00-\u9FA5]')# 过滤非中文
        data = filtrate.sub(r'', info)
        if data not in filter_chars:
            filtered_infos.add(data)

    return [[info, ccharacter_2_pinyin(info)] for info in sorted(filtered_infos)]

def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     description='parse xls data, get Chinese character and pinyin @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python parsexls_ccharacter2pinyin.py -x <path to xls file> -n <sheet number> -c <column name>
'''

                                        )
    parser.add_argument('-x','--xls', type=str, help='xls file to parse')
    parser.add_argument('-n','--number', type=str, help='sheet number')
    parser.add_argument('-c','--column', type=str, help='column name')
    parser.add_argument('-f','--filter', type=str, help='character need to be filtered, seperate by ,')
    args = parser.parse_args()

    if args.xls is None or args.number is None or args.column is None:
        parser.error("xls file/sheet number/column name is needed")
        sys.exit(1)
    if not os.path.exists(args.xls):
        parser.error('xls file not exist')
        sys.exit(1)

    return args

if __name__ == "__main__":
    args = parse_options()
    filterate = [] if args.filter is None else args.filter.split(",")
    print(main(args.xls, int(args.number), args.column, filterate))


