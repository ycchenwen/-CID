# coding:utf-8
import os
import pandas as pd
import datetime
today = str(datetime.date.today()).replace('-', '')
old_path = r'D:\综资指标'
# 路径设为日期文件夹下
os.chdir(os.path.join(old_path,today))
# 前提是确保网管ONU名称的唯一性
# 读取原始数据
raw_onu = pd.read_csv('ONU管理.csv')
raw_onu.rename(columns={'\ufeff资源标识':'资源标识','ONU名称':'onu_name'},inplace=True)
zl_free_posport = pd.read_csv('全量空闲的直连用户POS端口关联PON口关系.csv',encoding='gbk')
net_cid = pd.read_csv('allonu.csv',encoding='gbk')
# 剔除综资ONU管理表中ONU名称重复
temp = raw_onu['onu_name'].value_counts()
temp_df = pd.DataFrame({'onu_name':temp.index,'重复次数':temp.values})
chongfu = temp_df[temp_df['重复次数'] > 1].copy()
unique = temp_df[temp_df['重复次数'] == 1].copy()
del chongfu['重复次数']
del unique['重复次数']
chongfu_onu = pd.merge(chongfu,raw_onu,on='onu_name',how='left')
clean_onu = pd.merge(unique,raw_onu,on='onu_name',how='left')
empty_onu = raw_onu[raw_onu['onu_name'].isnull()].copy()
empty_onu.to_excel('ONU管理名称空值.xlsx',index=False)
chongfu_onu.to_excel('ONU管理名称重复.xlsx',index=False)
# 筛选出综资没有上联POS的ONU名称 或者没有上联POS端口的ONU名称
filtered_onu = clean_onu[clean_onu['上联设备'].isnull()].copy()
del filtered_onu['上联设备']
del filtered_onu['上联设备端口']
match_cid_onu = pd.merge(filtered_onu,net_cid,on='onu_name',how='left')
match_cid_onu_group = match_cid_onu.groupby(['pon'])
lst = []
for name, group in match_cid_onu_group:
    ls_temp = list(range(1,len(group)+1))
    s_temp = pd.Series(ls_temp,index=group.index)
    lst.append(s_temp)
#  列中含有数值项时不能str拼接
match_cid_onu['所属PON口排列'] = match_cid_onu['pon']+'-'+pd.concat(lst).map(str)
result = pd.merge(match_cid_onu,zl_free_posport,on='所属PON口排列',how='left')
result.rename(columns={'分光器名称':'上联设备','端口名称':'上联设备端口','所属PON口_y':'分光器所属PON口'},inplace=True)
del result['端口状态']
del result['端口类型']
del result['端口序号']
result.to_excel('无上联ONU关联POS结果.xlsx',index=False)
# 最后保存的关联结果onu_name重复(对多条cid)的情况手动处理。
