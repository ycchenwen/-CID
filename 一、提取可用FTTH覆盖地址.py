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


# 读取数据
raw_fg = pd.read_csv('FTTH覆盖范围.csv',usecols=[0,1])
# 0列关联设备，1列覆盖地址
raw_fg.rename(columns={'\ufeff关联设备':'pos','覆盖地址':'st_address'},inplace=True)
raw_fg['pos'] = raw_fg['pos'].apply(rep)
st = pd.read_csv('家客标准地址.csv',usecols=[4])
# 4列标准地址完整名称
stt = pd.DataFrame({'st_address':st['地址完整名称'].unique()})
match = pd.merge(raw_fg,stt,on='st_address',how='inner')
match3 = match[match['pos'].notnull()].copy()
raw_pos = pd.read_csv('POS管理.csv',usecols=[2,6])
# 2列分光器名称，6列所属PON口
raw_pos.rename(columns={'分光器名称':'pos','所属PON口':'pon'},inplace=True)
match2 = pd.merge(match3,raw_pos,on='pos',how='left')
result = match2[match2['pon'].notnull()].copy()
result.to_csv('全量数据库FTTH覆盖地址关联PON口关系.csv',index=False)
