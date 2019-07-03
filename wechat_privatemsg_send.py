# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 11:36:27 2018

@author: yc
"""
# 群发送定制消息
import wxpy
import os
import time
import csv
os.chdir(r'C:\Users\yc\Desktop')
bot = wxpy.Bot()


def read_info(csv_name):
    f = open('./'+csv_name, 'r')
    reader = csv.DictReader(f)
    return [info for info in reader]


def make_msg(raw_info):
    template = '通知:{n}请于{t}到{a}参加{s}课程,收到请回复，谢谢!'
    return [[info['姓名'], template.format(n=info['姓名'], t=info['时间'], a=info['地点'], s=info['课程'])] for info in raw_info]


def send_msg(msg_list):
    for msg in msg_list:
        friend = bot.friends().search(msg[0])
        if len(friend) == 1:
            friend[0].send(msg[1])
            time.sleep(10)
        else:
            print('check the name you send')


raw_read = read_info('名单.csv')
new_msg = make_msg(raw_read)
send_msg(new_msg)
print('done !')
