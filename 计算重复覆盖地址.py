# coding:utf-8
import os
import pandas as pd
os.chdir(r'D:\综资指标')
#  读取一份csv文件
# data_in = pd.read_csv('宜昌覆盖_0.csv',encoding = 'gbk')

#  读取一份excel文件
# data_in = pd.read_excel('ZXONU-2019-02-26.xlsx',sheetname = 'ZXONU-2019-02-26')

#  读取两张表
df1 = pd.read_csv('宜昌覆盖表_0.csv',encoding='gbk')
df2 = pd.read_csv('宜昌覆盖表_1.csv',encoding='gbk')
data_in = pd.concat([df1,df2],ignore_index=True)
temp = data_in['覆盖地址'].value_counts()
temp_df = pd.DataFrame({'覆盖地址':temp.index,'重复次数':temp.values})
chongfu = temp_df[temp_df['重复次数'] > 1].copy()
result = pd.merge(chongfu,data_in,on='覆盖地址',how='left')

#  保存为csv文件
result.to_csv('重复覆盖地址.csv',index=False)
