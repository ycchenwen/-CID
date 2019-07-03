import pandas as pd
import time
start_time = time.perf_counter()
f = open(r'D:\CID关联综资设备信息-20190605.csv')
names = f.readline().replace('\n', '').split(',')
names.append('cid')
print('已读完第1行数据')
data = []
count = 1
while True:
    temp = []
    temp = f.readline().replace('\n', '').split(',')
    if temp == ['']:
        break
    count += 1
    print('已读完第{}行数据'.format(count))
    # 数据筛选及处理
    if temp[3] == '宜昌':
        try:
            rack = temp[9].split('/')[0]
            slot = temp[9].split('/')[1]
            port = temp[9].split('/')[2]
            cid = temp[8] + '/' + rack + '/' + rack + '/' + slot + \
                '/0/' + port + '/' + '0' * (24 - len(temp[7])) + temp[7]
        except:
            cid = ''
        temp.append(cid)
        data.append(temp)
f.close()
print('读取数据完毕')
df = pd.DataFrame(data, columns=names)
df.to_csv(r'D:\yichang.csv', index=False)
end_time = time.perf_counter()
print('共计耗时{}秒'.format(end_time - start_time))
