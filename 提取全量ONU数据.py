
# -*- coding: utf-8 -*-
import os
import pandas as pd
import datetime
start_time = datetime.datetime.now()   # 开始计时
print('运行开始时间:', start_time)
# 输入路径
os.chdir(r'C:\Users\yc\Desktop\网管CID')
# 输出路径 output_path
date_name = str(datetime.date.today())
output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)
# 读取原始数据
hwonu_df = pd.read_csv('hwonu.csv', encoding='utf8')
m = []
for i in range(1,15):
    zxonu_slice = pd.read_excel('{}.xls'.format(str(i)))
    m.append(zxonu_slice)
zxonu_df = pd.concat(m)
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


hwonu_df.rename(columns={'ONU名称':'onu_name','ONU ID':'ontid','ONUTYPE':'type'},inplace=True)
hwonu_df['pon']=hwonu_df['OLT名称']+'_框:'+hwonu_df['框'].map(str)+'/槽:'\
                        +hwonu_df['槽'].map(str)+'/端口:'+hwonu_df['端口'].map(str)
hwonu_df['mark']=hwonu_df['pon']+'/ONTID:'+hwonu_df['ontid'].map(str)
hw_reg_col=hwonu_df['SN/MAC']+'#'+hwonu_df['LOID']
hwonu_df['cid']=hwonu_df['OLT IP地址']+'/0/'+hwonu_df['框'].map(str)+'/'+hwonu_df['槽'].map(str)+\
                '/0/'+hwonu_df['端口'].map(str)+'/'+hw_reg_col.map(hw_reg_transform)
hwonu_df.to_csv(os.path.join(output_path,'HWONU-{}.csv'.format(date_name)),index=False)
new_hwonu_df=hwonu_df[['mark','onu_name','pon','ontid','cid','type']].copy()
new_hwonu_df['wg']='华为'
# 中兴网管onu数据处理
zxonu_df.rename(columns={'ONU索引':'ontid','名称':'onu_name','业务类型':'type'},inplace=True)
zxonu_df['pon']=zxonu_df['网元名']+'_框:'+zxonu_df['机框'].map(str)+'/槽:'+\
                   zxonu_df['槽位'].map(str)+'/端口:'+zxonu_df['端口'].map(str)
zxonu_df['mark']=zxonu_df['pon']+'/ONTID:'+zxonu_df['ontid'].map(str)
zxonu_df['cid']=zxonu_df['网元IP']+'/'+zxonu_df['机架'].map(str)+'/'+\
                   zxonu_df['机框'].map(str)+'/'+zxonu_df['槽位'].map(str)+\
                   '/0/'+zxonu_df['端口'].map(str)+'/'+zxonu_df['认证值'].map(zx_reg_transform)
zxonu_df.to_csv(os.path.join(output_path,'ZXONU-{}.csv'.format(date_name)),index=False)
new_zxonu_df=zxonu_df[['mark','onu_name','pon','ontid','cid','type']].copy()
new_zxonu_df['wg']='中兴'
# 计算处理时长
all_onu_df=pd.concat([new_zxonu_df,new_hwonu_df])
temp = all_onu_df['onu_name'].value_counts()
temp1 = pd.DataFrame({'onu_name':temp.index,'times':temp.values})
result = pd.merge(all_onu_df,temp1,on='onu_name',how='left')
result.to_csv(os.path.join(output_path,'allonu-{}.csv'.format(date_name)),index=False)
end_time=datetime.datetime.now()
print('运行结束时间:',end_time)
print('共计运行时间:',end_time-start_time)
