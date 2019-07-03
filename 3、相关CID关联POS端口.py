# coding:utf-8
import os
import pandas as pd
import datetime
today = str(datetime.date.today()).replace('-', '')
old_path = r'D:\综资指标'
# 路径设为日期文件夹下
# 确保相关cid网管上存在
# 确保onu_name的唯一性
os.chdir(os.path.join(old_path,today))
raw_cid = pd.read_excel('related cid module.xlsx',sheetname='相关CID')
net_cid = pd.read_csv('allonu.csv',encoding='gbk')
raw_onu = pd.read_csv('ONU管理.csv')
zl_free_posport = pd.read_csv('全量空闲的直连用户POS端口关联PON口关系.csv',encoding='gbk')
match_cid = pd.merge(raw_cid,net_cid,on='cid',how='left')
related_cid = match_cid[match_cid['mark'].notnull()].copy()
raw_onu.rename(columns={'\ufeff资源标识':'资源标识','ONU名称':'onu_name'},inplace=True)
temp = pd.merge(related_cid,raw_onu,on='onu_name',how='inner')
temp1 = temp[temp['上联设备'].notnull()].copy()
temp2 = temp[temp['上联设备'].isnull()].copy()
temp1.to_excel('匹配到ONU管理表中上联.xlsx',index=False)
temp2.to_excel('未匹配到ONU管理中上联.xlsx',index=False)
temp11 = temp1[['cid','mark','pon','ontid','onu_name','上联设备','上联设备端口']].copy()
temp22 = temp2[['cid','mark','pon','ontid','onu_name']].copy()
temp22_group = temp22.groupby(['pon'])
lst = []
for name, group in temp22_group:
    ls_temp = list(range(1,len(group)+1))
    s_temp = pd.Series(ls_temp,index=group.index)
    lst.append(s_temp)
#  列中含有数值项时不能str拼接
temp22['所属PON口排列'] = temp22['pon']+'-'+pd.concat(lst).map(str)
result22 = pd.merge(temp22,zl_free_posport,on='所属PON口排列',how='left')
result22.rename(columns={'分光器名称':'上联设备','端口名称':'上联设备端口'},inplace=True)
del result22['端口状态']
del result22['端口类型']
del result22['端口序号']
del result22['所属PON口']
del result22['所属PON口排列']
result = pd.concat([temp11,result22],ignore_index=True)
result.rename(columns={'上联设备':'pos','上联设备端口':'posport'},inplace=True)
result.to_excel('相关CID关联POS端口结果.xlsx',index=False)
