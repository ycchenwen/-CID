# coding:utf-8
import re
import pandas as pd
pat1 = re.compile('interface gpon-onu_[0-9]+/[0-9]+/[0-9]+:[0-9]+')
pat2 = re.compile('tcont [0-9]+.*profile.*')
pat3 = re.compile('gemport [0-9]+.*tcont.*')
pat4 = re.compile('service-port [0-9]+ vport [0-9]+.*')
pat5 = re.compile('port-identification sub-option remote-id enable vport.*')
pat6 = re.compile('pppoe-intermediate-agent enable vport.*')
pat7 = re.compile('pppoe-intermediate-agent trust true replace vport.*')
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
        if pat1.findall(st) or pat2.findall(st) or pat3.findall(st) or pat4.findall(st) or \
        pat5.findall(st) or pat6.findall(st) or pat7.findall(st):
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
df.to_excel(r'D:\官当割接\add_gem.xlsx',index=False)
