# coding:utf-8
import pandas as pd
import os
def match_xq(name,lst):
    s = ''
    for i in lst:
        if i in str(name):
            if s == '':
                s += i
            elif s != '':
                s += '|'+i
    return s

os.chdir(r'D:')
xiaoqu = pd.read_excel('小区名称表.xlsx', sheet_name='小区名称')
xq_names = xiaoqu['小区名称'].tolist()
quxian = pd.read_excel('区县表.xlsx', sheet_name='区县')
qx_names = quxian['区县'].tolist()
fgdizhi = pd.read_excel('补充小区副本.xlsx', sheet_name='标准地址')
fgdizhi['匹配小区'] = fgdizhi['标准地址'].apply(match_xq, args=(xq_names,))
fgdizhi['匹配区县'] = fgdizhi['标准地址'].apply(match_xq, args=(qx_names,))
fgdizhi.to_excel('匹配结果.xlsx', index=False)
