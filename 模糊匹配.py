import pandas as pd
import os
from jieba import lcut


def get_max_match_str(s,lst):
    """
    字符串s与字符串列表lst的最大近似模糊匹配
    """
    dic = {}
    m = ''
    for item in lst:
        count = 0
        for i in lcut(s):
            if i in item:
                count += 1
        dic[item] = count
    for element in dic:
        if dic[element] == max(dic.values()):
            if m == '':
                m += element[5:]
            elif m != '':
                m += '|'+element[5:]
    return m


os.chdir(r'D:\works')
df0 = pd.read_excel('./居民小区信息表.xlsx', sheetname='宜昌资管小区信息')
df1 = pd.read_excel('./居民小区信息表.xlsx', sheetname='小区点')
df2 = pd.read_excel('./居民小区信息表.xlsx', sheetname='居民小区面')
xq_list = list(df0['辅助列'])
df1['匹配小区'] = df1['辅助列'].apply(get_max_match_str,args=(xq_list,))
df2['匹配小区'] = df2['辅助列'].apply(get_max_match_str,args=(xq_list,))
df1.to_excel('./小区点.xlsx', index=False)
df2.to_excel('./居民小区面.xlsx', index=False)
