# coding:utf-8
import os
import pandas as pd
import datetime
today = str(datetime.date.today()).replace('-', '')
old_path = r'D:\综资指标'
# 路径设为日期文件夹下
os.chdir(os.path.join(old_path,today))


def rep(s):
    return str(s).replace('\ufeff"','').replace('"','')


# 读入日期文件夹下的原始POS管理，POS端口管理
raw_pos = pd.read_csv('POS管理.csv')
raw_posport = pd.read_csv('POS端口管理.csv')
# 提取可用空闲的POS端口关联pon口关系表
pos_in = raw_pos[['分光器名称','所属PON口']].copy()
posport_in = raw_posport[['端口名称','端口状态','端口类型','所属分光器','端口序号']].copy()
posport_in.rename(columns={'所属分光器':'分光器名称'},inplace = True)
free_posport = posport_in[(posport_in['端口状态']=='空闲') & (posport_in['端口类型']=='分光器下联口')].copy()
all_free_posport = pd.merge(free_posport,pos_in,on='分光器名称',how='left')
# all_free_posport.to_csv('全量空闲POS端口.csv',index=False)
# all_free_posport为所有空闲分光器端口，不分一二级，不分直连用户与否
# 是否一二级，是否直连用户，需根据是否有覆盖地址判断
all_fg = pd.read_csv('FTTH覆盖范围.csv')
all_fg.rename(columns={'\ufeff关联设备':'关联设备'},inplace=True)
all_fg['关联设备'] = all_fg['关联设备'].apply(rep)
ref_col = all_fg['关联设备'].copy()
zl_pos = pd.DataFrame({'分光器名称':ref_col.unique()})
# zl_pos.to_csv('直连用户的POS.csv',index = False)
# 空闲可用的直连用户POS端口关联PON口关系表
zl_free_posport = pd.merge(zl_pos,all_free_posport,on='分光器名称',how='inner')
result1 = zl_free_posport[zl_free_posport['所属PON口'].notnull()]
raw_onu = pd.read_csv('ONU管理.csv')
la = list(raw_onu['上联设备端口'].unique())
result = result1[True ^ result1['端口名称'].isin(la)].copy()
result.sort_values(by='端口序号',inplace=True)
# ONU或CID需要根据所属PON口的排列进行匹配到POS端口
result_group = result.groupby(['所属PON口'])
lst = []
for name, group in result_group:
    ls_temp = list(range(1,len(group)+1))
    s_temp = pd.Series(ls_temp,index=group.index)
    lst.append(s_temp)
#  列中含有数值项时不能str拼接
result['所属PON口排列'] = result['所属PON口']+'-'+pd.concat(lst).map(str)
#  保存为csv文件
result.to_csv('全量空闲的直连用户POS端口关联PON口关系.csv',index=False)
