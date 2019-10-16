# 计算每个PON口下不重复账号数目
import pandas as pd
import xlwings as xw
d1 = {}
d2 = {}
data = pd.read_excel(r'D:\AAA活跃用户清单_1571186487541.xlsx')   # 计算出pon口和olt之后
data_gr1 = data.groupby(['pon'])
data_gr2 = data.groupby(['olt'])
for name1,group1 in data_gr1:
    d1[name1] = len(group1['account'].unique())
for name2,group2 in data_gr2:
    d2[name2] = len(group2['account'].unique())
wb = xw.Book(r'D:\AAA活跃用户统计表.xlsx')
sht1 = wb.sheets['PON统计']
sht2 = wb.sheets['OLT统计']
sht1.range('a2').value = d1
sht2.range('a2').value = d2
wb.save()
wb.close()
