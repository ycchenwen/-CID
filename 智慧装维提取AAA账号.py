import pandas as pd
import re
from datetime import date
today = date.today()
pat1 = re.compile(r'(?:lag-\d*|trunk.*):\d{1,4}\.\d{1,4}')    # lag-102:2171.2036
pat2 = re.compile(r'(?:\d{1,3}\.){3}\d{1,3}/[01]/[01]/\d{1,3}/0/\d{1,3}/.{24}')   # cid
pat3 = re.compile(r'vlanid=\d{1,4}')      # 铁通自建cvlan
pat4 = re.compile(r'vlanid2=\d{1,4}')     # 铁通自建svlan


def get_info(st):
    try:
        if 'vlanid' in st:
            sv = pat4.findall(st)[0].replace('vlanid2=','')
            cv = pat3.findall(st)[0].replace('vlanid=','')
            ci = ''
            return sv,cv,ci
        else:
            sv = pat1.findall(st)[0].split(':')[-1].split('.')[0]
            cv = pat1.findall(st)[0].split(':')[-1].split('.')[-1]
            try:
                ci = pat2.findall(st)[0]
            except IndexError:
                ci = ''
            return sv,cv,ci
    except:
        sv = cv = ci = ''
        return sv,cv,ci


def get_svlan(st):
    return get_info(st)[0]


def get_cvlan(st):
    return get_info(st)[1]


def get_cid(st):
    return get_info(st)[-1]


df = pd.read_excel(r'D:\AAA活跃用户清单_1562730164546.xls',sheetname='数据1')
df['account'] = df['上网账号']+'@'+df['域名']
df['svlan'] = df['绑定信息'].apply(get_svlan)
df['cvlan'] = df['绑定信息'].apply(get_cvlan)
df['cid'] = df['绑定信息'].apply(get_cid)
df.to_csv(r'd:\aaa-{}.csv'.format(str(today)),index=False)
