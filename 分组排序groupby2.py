# coding:utf-8
import os
import numpy as np
import pandas as pd
os.chdir(r'D:')
#  读取一份csv文件
# data_in = pd.read_csv('宜昌覆盖_0.csv',encoding = 'gbk')

#  读取一份excel文件
data_in = pd.read_excel('zxonu.xlsx')

#  读取两张表
# df1=pd.read_excel('副本.xlsx',sheetname = '副本1')
# df2=pd.read_excel('副本.xlsx',sheetname = '副本2')
# data_in = pd.concat([df1,df2],ignore_index = True)

data_group = data_in.groupby(['认证值'])
lst = []
arr = []
for name, group in data_group:
    arr_temp = len(group)*np.ones(len(group),dtype = np.int)
    ls_temp = list(range(1,len(group)+1))
    s_temp = pd.Series(ls_temp,index=group.index)
    ar_temp = pd.Series(arr_temp,index=group.index)
    lst.append(s_temp)
    arr.append(ar_temp)
#  列中含有数值项时不能str拼接
# data_in['关联设备排列']=data_in['关联设备']+'-'+pd.concat(lst).map(str)

data_in['认证值序号']=pd.concat(lst)
data_in['认证值重复']=pd.concat(arr)
#  保存为csv文件
# data_in.to_csv('onu名称重复.csv',index=False)
#  保存为excel文件(文件原数据会被覆盖掉)
data_in.to_excel('new_zxonu.xlsx',sheet_name = '合并',index = False)
