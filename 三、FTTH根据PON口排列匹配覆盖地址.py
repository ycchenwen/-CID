# coding:utf-8
import os
import pandas as pd
import datetime
today = str(datetime.date.today()).replace('-', '')
old_path = r'D:\综资指标'
# 路径设为日期文件夹下
os.chdir(os.path.join(old_path,today))
all_fg = pd.read_csv('全量数据库FTTH覆盖地址关联PON口关系.csv',encoding='gbk')
un_fg = pd.read_excel('useless st_address module.xlsx')
data_in = pd.read_excel('related account module.xlsx',sheetname='根据PON口排列匹配覆盖')
la = list(un_fg['st_address'].unique())
filtered_fg = all_fg[True ^ all_fg['st_address'].isin(la)].copy()
filtered_fg_group = filtered_fg.groupby(['pon'])
lst = []
for name, group in filtered_fg_group:
    ls_temp = list(range(1,len(group)+1))
    s_temp = pd.Series(ls_temp,index=group.index)
    lst.append(s_temp)
#  列中含有数值项时不能str拼接
filtered_fg['PON口排列'] = filtered_fg['pon']+'-'+pd.concat(lst).map(str)
data_out = pd.merge(data_in,filtered_fg,on='PON口排列',how='left')
data_out.to_excel('FTTH账号根据PON口排列匹配覆盖地址结果.xlsx',index=False)
