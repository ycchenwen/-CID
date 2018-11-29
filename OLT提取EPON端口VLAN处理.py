import os
import pandas as pd
from datetime import datetime
os.chdir(r'D:\OLT配置文档')
t1 = datetime.now()
print('运行开始时间:{}'.format(t1))
vlan_json = []
for root, dirs, files in os.walk('.'):
    if files == ['startrun.dat']:
        olt_ip = root[root.rfind('10.'):]
        f = open(os.path.join(root,files[0]),'r')
        # 读取有用信息vlan_txt,qinq_txt
        vlan_txt = []
        qinq_txt = []
        for line in f.readlines():
            if 'pon-onu-mng epon-onu' in line or 'vlan port ' in line:
                vlan_txt.append(line.replace('\n', ''))
            elif 'vlan-smart-qinq ingress-port' in line:
                qinq_txt.append(line.replace('\n', ''))
        f.close()
        # 提取OLT的vlan-smart-qinq信息
        qinq_json =[]
        qinq_dic = {}
        for qinq in qinq_txt:
            qinq_dic['olt']=olt_ip
            qinq_dic['pon']=qinq[qinq.find('epon-olt'):qinq.find(' cvlan')]
            qinq_dic['svlan']=eval(qinq[qinq.find('svlan')+6:qinq.find('svlan')+10])    # svlan一般都是4位数字
            if 'to' in qinq:
                qinq_dic['begin_cvlan']=eval(qinq[qinq.find('cvlan')+6:qinq.find(' to')])
                qinq_dic['end_cvlan']=eval(qinq[qinq.find('to')+3:qinq.find(' ',qinq.find('to')+3)])
            else:
                qinq_dic['end_cvlan']=qinq_dic['begin_cvlan']=eval(qinq[qinq.find('cvlan')+6:qinq.find(' ',qinq.find('cvlan')+6)])
            x =qinq_dic.copy()
            qinq_json.append(x)
        # 获取onu端口cvlan，计算svlan信息
        vlan_dic = {}
        for item in vlan_txt:
            if 'pon-onu-mng epon-onu' in item:
                j = vlan_txt.index(item)+1
                while 'vlan port ' in vlan_txt[j]:
                    vlan_dic['olt'] = olt_ip
                    vlan_dic['onu_id'] = item[item.find('epon-onu'):]
                    vlan_dic['pon'] = vlan_dic['onu_id'].split(':')[0].replace('onu', 'olt')
                    vlan_dic['port_id'] = vlan_txt[j][vlan_txt[j].find('eth_'):vlan_txt[j].find(' mode')]
                    try:
                        if 'tag' in vlan_txt[j]:
                            vlan_dic['cvlan'] = eval(vlan_txt[j][vlan_txt[j].find('tag vlan')+9:vlan_txt[j].find(' ',vlan_txt[j].find('tag vlan')+9)])
                            for element in qinq_json:
                                if vlan_dic['pon'] == element['pon'] and element['end_cvlan']>=vlan_dic['cvlan']>=element['begin_cvlan']:
                                    vlan_dic['svlan']=element['svlan']
                                    break
                            else:
                                vlan_dic['svlan'] = None
                        elif 'vlan-list' in vlan_txt[j]:
                            vlan_dic['cvlan'] = vlan_txt[j][vlan_txt[j].find('vlan-list')+10:vlan_txt[j].find(' ',vlan_txt[j].find('vlan-list')+10)]
                            temp = vlan_dic['cvlan'].split(',')
                            result = []
                            for i in temp:
                                for element in qinq_json:
                                    if vlan_dic['pon'] == element['pon'] and element['end_cvlan']>=eval(i)>=element['begin_cvlan']:
                                        m = str(element['svlan'])
                                        break
                                else:
                                    m = ''
                                result.append(m)
                            vlan_dic['svlan'] = ','.join(result)
                    except:
                        print('{}的{}的{}执行内外标计算中发生异常'.format(vlan_dic['olt'], vlan_dic['onu_id'], vlan_dic['port_id']))
                        vlan_dic['svlan'] = vlan_dic['cvlan'] = None
                    y = vlan_dic.copy()
                    vlan_json.append(y)
                    j += 1
                    if j > len(vlan_txt)-1:
                        break
all_vlan_df = pd.DataFrame(vlan_json)
all_vlan_df.to_excel('EPON端口VLAN.xlsx', index=False)
t2 = datetime.now()
print('运行结束时间:{}'.format(t2))
print('共计运行时间:{}'.format(t2-t1))
