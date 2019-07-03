# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 15:32:55 2018

@author: yc
"""
import os
import pandas as pd
os.chdir(r'D:\OLT配置文档')
# 读取
data = pd.read_excel('家宽ONU摸排（城区5.5更新）(1).xlsx',sheetname='ONU')
yc_account = pd.read_excel('yichang_20190507.xlsx')
mac_table = pd.read_excel('用户MAC地址汇总.xlsx')
# 匹配
account_match = pd.merge(data,yc_account,on='cid',how='left')
mac_match = pd.merge(data,mac_table,on='mark',how='left')
# 保存
account_match.to_excel('account_match.xlsx',index=False)
mac_match.to_excel('mac_match.xlsx',index=False)
