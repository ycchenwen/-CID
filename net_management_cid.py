# -*- coding: utf-8 -*-
import os
import pandas as pd
import datetime
start_time=datetime.datetime.now()   # ��ʼ��ʱ
print('���п�ʼʱ��:',start_time)
# ����·��
os.chdir(r'C:\Users\yc\Desktop\����CID')
# ���·�� output_path
date_name=str(datetime.date.today())
output_path='./output'
if not os.path.exists(output_path):
    os.makedirs(output_path)
# ��ȡԭʼ����
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
print('��ȡ������ϣ�ʱ��:',datetime.datetime.now())
# ��ΪONU��ֵ֤ת��
def hw_reg_transform(strin):
    if strin.endswith('--'):
        y=strin.replace('#--','')
    else:
        y=strin.split('#')[-1]
    return ('0'*(24-len(y))+y).upper()
# ����ONU��ֵ֤ת��
def zx_reg_transform(strin):
    strin=strin.replace('/ztepon','').replace('/1111','').replace('-','')
    return ('0'*(24-len(strin))+strin).upper()
# ��Ϊ����onu���ݴ���
hwonu_df.rename(columns={'ONU����':'onu_name','ONU ID':'ontid'},inplace=True)
hwonu_df['pon']=hwonu_df['OLT����']+'_��:'+hwonu_df['��'].map(str)+'/��:'\
                        +hwonu_df['��'].map(str)+'/�˿�:'+hwonu_df['�˿�'].map(str)
hwonu_df['mark']=hwonu_df['pon']+'/ONTID:'+hwonu_df['ontid'].map(str)
hw_reg_col=hwonu_df['SN/MAC']+'#'+hwonu_df['LOID']
hwonu_df['cid']=hwonu_df['OLT IP��ַ']+'/0/'+hwonu_df['��'].map(str)+'/'+hwonu_df['��'].map(str)+\
                '/0/'+hwonu_df['�˿�'].map(str)+'/'+hw_reg_col.map(hw_reg_transform)
new_hwonu_df=hwonu_df[['mark','onu_name','pon','ontid','cid']]
# ��Ϊ����vlan���ݴ���
hwvlan_df['mark']=hwvlan_df['��Ԫ����']+'_��:'+hwvlan_df['���'].map(str)+'/��:'\
                        +hwvlan_df['�ۺ�'].map(str)+'/�˿�:'+hwvlan_df['�˿ں�'].map(str)\
                        +'/ONTID:'+hwvlan_df['ONU ID'].map(str)
hwvlan_df.rename(columns={'�����VLAN':'svlan','�ڲ�VLAN':'cvlan','�û�VLAN':'uservlan'},inplace=True)
new_hwvlan_df=hwvlan_df[['mark','svlan','cvlan','uservlan']]                      
# ��������onu���ݴ���
zxonu_df.rename(columns={'ONU����':'ontid','����':'onu_name'},inplace=True)
zxonu_df['pon']=zxonu_df['��Ԫ��']+'_��:'+zxonu_df['����'].map(str)+'/��:'+\
                   zxonu_df['��λ'].map(str)+'/�˿�:'+zxonu_df['�˿�'].map(str)
zxonu_df['mark']=zxonu_df['pon']+'/ONTID:'+zxonu_df['ontid'].map(str)
zxonu_df['cid']=zxonu_df['��ԪIP']+'/'+zxonu_df['����'].map(str)+'/'+\
                   zxonu_df['����'].map(str)+'/'+zxonu_df['��λ'].map(str)+\
                   '/0/'+zxonu_df['�˿�'].map(str)+'/'+zxonu_df['��ֵ֤'].map(zx_reg_transform)
new_zxonu_df=zxonu_df[['mark','onu_name','pon','ontid','cid']]
# ��������vlan���ݴ���
zxvlan_df['mark']=zxvlan_df['��Ԫ��������']+'_��:'+zxvlan_df['����'].map(str)+'/��:'\
                   +zxvlan_df['��λ'].map(str)+'/�˿�:'+zxvlan_df['�˿�'].map(str)+'/ONTID:'\
                   +zxvlan_df['ONU ID'].map(str)
zxvlan_df.rename(columns={'�û�VLAN':'uservlan','C-VID':'cvlan','S-VID':'svlan'},inplace=True)
new_zxvlan_df=zxvlan_df[['mark','svlan','cvlan','uservlan']]
# ����ƴ��
all_onu_df=pd.concat([new_zxonu_df,new_hwonu_df])
all_vlan_df=pd.concat([new_zxvlan_df,new_hwvlan_df])
all_onu_df.to_csv(os.path.join(output_path,'allonu-{}.csv'.format(date_name)),index=False)
all_vlan_df.to_csv(os.path.join(output_path,'allvlan-{}.csv'.format(date_name)),index=False)
# ����ƥ��
all_vlan_df['uservlan']=all_vlan_df['uservlan'].astype(str)
filtered_vlan_df=all_vlan_df[(all_vlan_df['uservlan']!='46') & (all_vlan_df['uservlan']!='47')]
filtered_vlan_df.to_csv(os.path.join(output_path,'filteredvlan-{}.csv'.format(date_name)),index=False)
net_management_cid=pd.merge(all_onu_df,filtered_vlan_df,how='left',on='mark')
net_management_cid.to_csv(os.path.join(output_path,'����CID-{}.csv'.format(date_name)),index=False)
# ���㴦��ʱ��
end_time=datetime.datetime.now()
print('���н���ʱ��:',end_time)
print('��������ʱ��:',end_time-start_time)