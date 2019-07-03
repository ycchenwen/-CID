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
zxvlan1=pd.read_csv('a.csv',encoding='gbk')
zxvlan2=pd.read_csv('b.csv',encoding='gbk')
zxvlan3=pd.read_csv('c.csv',encoding='gbk')
zxvlan4=pd.read_csv('d.csv',encoding='gbk')
zxvlan5=pd.read_csv('e.csv',encoding='gbk')
zxvlan6=pd.read_csv('f.csv',encoding='gbk')
zxvlan_df=pd.concat([zxvlan1,zxvlan2,zxvlan3,zxvlan4,zxvlan5,zxvlan6])
m=[]
for i in range(1,13):
    zxonu_slice=pd.read_excel('{}.xls'.format(str(i)))
    m.append(zxonu_slice)
zxonu_df=pd.concat(m)
print('读取数据完毕，时间:',datetime.datetime.now())
# 中兴ONU认证值转换
def zx_reg_transform(strin):
    strin=strin.replace('/ztepon','').replace('/1111','').replace('-','')
    return ('0'*(24-len(strin))+strin).upper()                    
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
# 数据匹配
new_zxvlan_df['uservlan']=new_zxvlan_df['uservlan'].astype(str)
filtered_vlan_df=new_zxvlan_df[(new_zxvlan_df['uservlan']!='46') & (new_zxvlan_df['uservlan']!='47')]
net_management_cid=pd.merge(new_zxonu_df,filtered_vlan_df,how='left',on='mark')
net_management_cid.to_csv(os.path.join(output_path,'中兴网管CID-{}.csv'.format(date_name)),index=False)
# 计算处理时长
end_time=datetime.datetime.now()
print('运行结束时间:',end_time)
print('共计运行时间:',end_time-start_time)
