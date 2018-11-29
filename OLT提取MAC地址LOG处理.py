import os
import pandas as pd
os.chdir(r'D:')
all_list = []
count = 0
for root, dirs, files in os.walk('./OLT配置文档'):
    for file in files:
        file_ip = file.split('_')[0]
        f = open(os.path.join('./OLT配置文档', file),'r')
        for line in f.readlines():
            if 'Dynamic' in line or 'Permanent' in line or 'Static' in line:
                lst = line.strip().split()
                dic = {'mac address': lst[0], \
                       'vlan id': lst[1], \
                       'type': lst[2], \
                       'port': lst[3],\
                       'olt ip': file_ip}
                all_list.append(dic)
        f.close()
        count += 1
df = pd.DataFrame(all_list)
df.to_excel('./用户MAC地址汇总.xlsx', index=False)
print('共计处理{}个文件，处理完成!'.format(count))