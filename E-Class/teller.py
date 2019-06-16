#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

import xml.etree.ElementTree as ET

import urllib
import urllib.request
import http.client

import noti


items = []
category = dict()

def initData():
    conn = http.client.HTTPConnection("kocw.net")
    conn.request("GET",
         #"/home/api/handler.do?key=537adad829de4e65782196737ced103f35930363b8e30956&category_type=t&category_id=" + str(id+1) + "&from=" + str(self.dateStart) + "&to=" + str(self.dateEnd) + "&end_num=30000"
         "/home/api/handler.do?key=537adad829de4e65782196737ced103f35930363b8e30956&category_type=t&from=20170101&to=20191201&end_num=30000"
         #"/home/api/handler.do?key=537adad829de4e65782196737ced103f35930363b8e30956&from=20100101&to=20200201&end_num=30000"
         )
    req = conn.getresponse()
    xml = req.read().decode('utf-8')

    root = ET.fromstring(xml)

    items.clear()
    for item in root.find('list'):
        data = dict()
        for d in item:
            data[d.tag] = d.text
        if 'course_title' in data.keys():
            items.append(data)

    for d in items:
        global category
        if 'taxon' in d.keys():
            taxon = d['taxon'].split('>')
            if taxon.__len__() < 2:
                taxon.append(taxon[0])
            if taxon.__len__() < 3:
                taxon.append(taxon[1])

            if not taxon[0] in category:
                category[taxon[0]] = dict()

            if not taxon[1] in category[taxon[0]]:
                category[taxon[0]][taxon[1]] = dict()

            if not taxon[2] in category[taxon[0]][taxon[1]]:
                category[taxon[0]][taxon[1]][taxon[2]] = 0

def replyAptData(taxon, user, course_title):
    print(user, taxon, course_title)
    res_list = noti.getData(taxon,course_title)
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '해당하는 데이터가 없습니다.')

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage( user, row )

def printList0(user):
    msg = ''
    for d in category.keys():
        msg += d+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '해당하는 데이터가 없습니다.')

def printList1(user, key0):
    msg = ''
    for d in category[key0].keys():
        msg += d+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '해당하는 데이터가 없습니다.')

def printList2(user, key0, key1):
    msg = ''
    for d in category[key0][key1].keys():
        msg += d+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '해당하는 데이터가 없습니다.')

def printList3(user, key0, key1, key2):
    msg = ''
    for d in items:
        if 'taxon' in d:
            if d['taxon'] == key0+'>'+key1+'>'+key2:
                msg += d['course_title']+'\n'
                msg += d['provider']+'/'+d['lecturer']+'\n'
                msg += d['course_url'] +'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '해당하는 데이터가 없습니다.')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    #검색 자연과학
    if text.startswith('검색') and len(args)>1:
        print('try to 검색', args[1])
        replyAptData(chat_id, args[1],args[2])
    elif text.startswith('확인'):
        print('try to 확인')
        check( chat_id )
    #elif text.startswith('대분류'):
    #    if len(args) > 1:
    elif text.startswith('?'):
        if len(args) == 1:
            printList0(chat_id)
        if len(args) == 2:
            printList1(chat_id, args[1])
        if len(args) == 3:
            printList2(chat_id, args[1], args[2])
        if len(args) == 4:
            printList3(chat_id, args[1], args[2], args[3])
    else:
        noti.sendMessage(chat_id,
"""
모르는 명령어입니다.
사용가능 명령어
대분류
""")

print('loading data')
initData()
print('complete loading')

today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', noti.TOKEN )

bot = telepot.Bot(noti.TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)