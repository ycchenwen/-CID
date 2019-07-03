# coding:utf-8
import re
import pandas as pd
pat1 = re.compile('interface gpon-olt_[0-1]/[0-9]*/[0-9]*')
pat2 = re.compile('onu [0-9]+ type.*')
f = open(r'D:\官当割接\startrun.dat')
data = []
count = 0
while True:
    st = f.readline().replace('\n','').strip()
    if st == '':
        count += 1
        if count >= 6:
            break
        continue
    elif st != '':
        count = 0
        if pat1.findall(st) or pat2.findall(st):
            data.append(st)
f.close()
result = []
while True:
    try:
        u = data.pop(0)
        if pat1.findall(u):
            result.append('exit')
            result.append(u)
        else:
            result.append(u)
    except IndexError:
        break
result.append(result.pop(0))
df = pd.DataFrame(result,columns=['code'])
df.to_excel(r'D:\官当割接\add_reg.xlsx',index=False)
