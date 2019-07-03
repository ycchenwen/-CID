# coding:utf-8
import os
import pandas as pd
os.chdir(r'D:')
# 读取一份csv文件
# data_in = pd.read_csv('宜昌覆盖_0.csv',encoding = 'gbk')

# 读取一份excel文件
data_in = pd.read_excel('ZXONU-2019-07-01.xlsx',sheetname = 'ZXONU-2019-07-01')
temp = data_in['MAC/SN'].value_counts()
temp_df = pd.DataFrame({'MAC/SN':temp.index,'重复次数':temp.values})
chongfu = temp_df[temp_df['重复次数'] > 1].copy()
result = pd.merge(chongfu,data_in,on='MAC/SN',how='left')

# 保存为csv文件
result.to_csv('重复MACSN.csv',index=False)
