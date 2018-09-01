# -*- coding: utf-8 -*-
import os
import pandas as pd
import datetime
start_time=datetime.datetime.now()   # 开始计时
print('运行开始时间:',start_time)
# 输入路径
os.chdir(r'C:\Users\yc\Desktop\网管CID')
# 输出路径 output_path
date_name=str(datetime.date.today())
output_path='./output'
if not os.path.exists(output_path):
    os.makedirs(output_path)
# 读取原始数据
hwonu_df=pd.read_csv('hwonu.csv',encoding='utf8')
hwvlan1=pd.read_csv('hwvlan.csv',encoding='gbk',skiprows=8)
hwvlan2=pd.read_csv('hwvlan@1.csv',encoding='gbk')
hwvlan3=pd.read_csv('hwvlan@2.csv',encoding='gbk')
hwvlan_df=pd.concat([hwvlan1,hwvlan2,hwvlan3])
zxvlan1=pd.read_csv('a.csv',encoding='gbk')
zxvlan2=pd.read_csv('b.csv',encoding='gbk')
zxvlan3=pd.read_csv('c.csv',encoding='gbk')
zxvlan_df=pd.concat([zxvlan1,zxvlan2,zxvlan3])
m=[]
for i in range(1,10):
    zxonu_slice=pd.read_excel('{}.xls'.format(str(i)))
    m.append(zxonu_slice)
zxonu_df=pd.concat(m)
print('读取数据完毕，时间:',datetime.datetime.now())
# 华为ONU认证值转换
def hw_reg_transform(strin):
    if strin.endswith('--'):
        y=strin.replace('#--','')
    else:
        y=strin.split('#')[-1]
    return ('0'*(24-len(y))+y).upper()
# 中兴ONU认证值转换
def zx_reg_transform(strin):
    strin=strin.replace('/ztepon','').replace('/1111','').replace('-','')
    return ('0'*(24-len(strin))+strin).upper()
# 华为网管onu数据处理
hwonu_df.rename(columns={'ONU名称':'onu_name','ONU ID':'ontid'},inplace=True)
hwonu_df['pon']=hwonu_df['OLT名称']+'_框:'+hwonu_df['框'].map(str)+'/槽:'\
                        +hwonu_df['槽'].map(str)+'/端口:'+hwonu_df['端口'].map(str)
hwonu_df['mark']=hwonu_df['pon']+'/ONTID:'+hwonu_df['ontid'].map(str)
hw_reg_col=hwonu_df['SN/MAC']+'#'+hwonu_df['LOID']
hwonu_df['cid']=hwonu_df['OLT IP地址']+'/0/'+hwonu_df['框'].map(str)+'/'+hwonu_df['槽'].map(str)+\
                '/0/'+hwonu_df['端口'].map(str)+'/'+hw_reg_col.map(hw_reg_transform)
new_hwonu_df=hwonu_df[['mark','onu_name','pon','ontid','cid']]
# 华为网管vlan数据处理
hwvlan_df['mark']=hwvlan_df['网元名称']+'_框:'+hwvlan_df['框号'].map(str)+'/槽:'\
                        +hwvlan_df['槽号'].map(str)+'/端口:'+hwvlan_df['端口号'].map(str)\
                        +'/ONTID:'+hwvlan_df['ONU ID'].map(str)
hwvlan_df.rename(columns={'网络侧VLAN':'svlan','内层VLAN':'cvlan','用户VLAN':'uservlan'},inplace=True)
new_hwvlan_df=hwvlan_df[['mark','svlan','cvlan','uservlan']]                      
# 中兴网管onu数据处理
zxonu_df.rename(columns={'ONU索引':'ontid','名称':'onu_name'},inplace=True)
zxonu_df['pon']=zxonu_df['网元名']+'_框:'+zxonu_df['机框'].map(str)+'/槽:'+\
                   zxonu_df['槽位'].map(str)+'/端口:'+zxonu_df['端口'].map(str)
zxonu_df['mark']=zxonu_df['pon']+'/ONTID:'+zxonu_df['ontid'].map(str)
zxonu_df['cid']=zxonu_df['网元IP']+'/'+zxonu_df['机架'].map(str)+'/'+\
                   zxonu_df['机框'].map(str)+'/'+zxonu_df['槽位'].map(str)+\
                   '/0/'+zxonu_df['端口'].map(str)+'/'+zxonu_df['认证值'].map(zx_reg_transform)
new_zxonu_df=zxonu_df[['mark','onu_name','pon','ontid','cid']]
# 中兴网管vlan数据处理
zxvlan_df['mark']=zxvlan_df['网元名及类型']+'_框:'+zxvlan_df['机框'].map(str)+'/槽:'\
                   +zxvlan_df['槽位'].map(str)+'/端口:'+zxvlan_df['端口'].map(str)+'/ONTID:'\
                   +zxvlan_df['ONU ID'].map(str)
zxvlan_df.rename(columns={'用户VLAN':'uservlan','C-VID':'cvlan','S-VID':'svlan'},inplace=True)
new_zxvlan_df=zxvlan_df[['mark','svlan','cvlan','uservlan']]
# 数据拼接
all_onu_df=pd.concat([new_zxonu_df,new_hwonu_df])
all_vlan_df=pd.concat([new_zxvlan_df,new_hwvlan_df])
all_onu_df.to_csv(os.path.join(output_path,'allonu-{}.csv'.format(date_name)),index=False)
all_vlan_df.to_csv(os.path.join(output_path,'allvlan-{}.csv'.format(date_name)),index=False)
# 数据匹配
all_vlan_df['uservlan']=all_vlan_df['uservlan'].astype(str)
filtered_vlan_df=all_vlan_df[(all_vlan_df['uservlan']!='46') & (all_vlan_df['uservlan']!='47')]
filtered_vlan_df.to_csv(os.path.join(output_path,'filteredvlan-{}.csv'.format(date_name)),index=False)
net_management_cid=pd.merge(all_onu_df,filtered_vlan_df,how='left',on='mark')
net_management_cid.to_csv(os.path.join(output_path,'网管CID-{}.csv'.format(date_name)),index=False)
# 计算处理时长
end_time=datetime.datetime.now()
print('运行结束时间:',end_time)
print('共计运行时间:',end_time-start_time)