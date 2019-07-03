import pandas as pd
import time
start_time = time.perf_counter()
f = open(r'D:\2019年3月宽带活跃清单（匹配经分）\data.txt')
names = f.readline().replace('\n', '').split(',')
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
    if temp[4] == '宜昌':
        data.append(temp)
f.close()
print('读取数据完毕')
df = pd.DataFrame(data, columns=names)
df.to_csv(r'D:\2019年3月宽带活跃清单（匹配经分）\yichang.csv', index=False)
end_time = time.perf_counter()
print('共计耗时{}秒'.format(end_time - start_time))
