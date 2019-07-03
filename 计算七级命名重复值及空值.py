# coding:utf-8
import os
import pandas as pd
import re
os.chdir(r'D:')
pattern = re.compile('ONU-\d{1,3}:\d{1,3}')


def pand(s):
    if str(s).isdigit():
        return True
    else:
        return False


def unst(s):
    return pattern.findall(str(s)) != []


# data_in = pd.read_csv('hwonu.csv',encoding = 'gbk')
data_in = pd.read_excel('ZXONU-2019-07-01.xlsx',sheetname = 'ZXONU-2019-07-01')
out = data_in[data_in['onu_name'].isnull()].copy()
out.to_csv('空值ONU名称.csv',index=False)
digit_name = data_in[data_in['onu_name'].apply(pand)].copy()
fi = data_in[data_in['onu_name'].apply(unst)].copy()
di_name = pd.concat([digit_name,fi],ignore_index=True)
di_name.to_csv('数值ONU名称.csv',index=False)
temp = data_in['onu_name'].value_counts()
temp_df = pd.DataFrame({'onu_name':temp.index,'重复次数':temp.values})
chongfu = temp_df[temp_df['重复次数'] > 1].copy()
result = pd.merge(chongfu,data_in,on='onu_name',how='left')
result.to_csv('重复ONU名称.csv',index=False)
