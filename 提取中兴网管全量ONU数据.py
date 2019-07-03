
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
m = []
for i in range(1, 16):
    zxonu_slice = pd.read_excel('{}.xls'.format(str(i)))
    m.append(zxonu_slice)
zxonu_df = pd.concat(m)
print('读取数据完毕，时间:', datetime.datetime.now())

# 中兴ONU认证值转换


def zx_reg_transform(strin):
    strin = strin.replace('/ztepon', '').replace('/1111', '').replace('-', '')
    return ('0' * (24 - len(strin)) + strin).upper()


# 中兴网管onu数据处理
zxonu_df.rename(columns={'ONU索引': 'ontid', '名称': 'onu_name'}, inplace=True)
zxonu_df['pon'] = zxonu_df['网元名'] + '_框:' + zxonu_df['机框'].map(str) + '/槽:' +\
    zxonu_df['槽位'].map(str) + '/端口:' + zxonu_df['端口'].map(str)
zxonu_df['mark'] = zxonu_df['pon'] + '/ONTID:' + zxonu_df['ontid'].map(str)
zxonu_df['cid'] = zxonu_df['网元IP'] + '/' + zxonu_df['机架'].map(str) + '/' +\
    zxonu_df['机框'].map(str) + '/' + zxonu_df['槽位'].map(str) +\
    '/0/' + zxonu_df['端口'].map(str) + '/' + zxonu_df['认证值'].map(zx_reg_transform)
zxonu_df.to_csv(
    os.path.join(
        output_path,
        'ZXONU-{}.csv'.format(date_name)),
    index=False)
# 计算处理时长
end_time = datetime.datetime.now()
print('运行结束时间:', end_time)
print('共计运行时间:', end_time - start_time)
