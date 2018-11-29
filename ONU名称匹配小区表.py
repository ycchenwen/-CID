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

os.chdir(r'C:\Users\yc\Desktop\FTTB匹配')
ydxq = pd.read_excel('2018年B改H小区明细（移动自建）.xlsx', sheet_name='移动')
xq_names = list(ydxq['小区名称'])
zxonu_df = pd.read_excel('ZXONU-2018-11-16.xlsx', sheet_name='ZXONU-2018-11-16')
zxonu_df['匹配小区'] = zxonu_df['onu_name'].apply(match_xq, args=(xq_names,))
zxonu_df.to_excel('./ZXONU.xlsx', index=False)
