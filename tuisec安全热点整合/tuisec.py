# @author:九世
# @time:2019/5/7
# @function:抓取tuisec更新的内容
# @file:tuisec.py

import gevent
from gevent import monkey;monkey.patch_all()
import requests
from multiprocessing import Process
import re
from bs4 import BeautifulSoup
import base64
import pymysql
import time
import config


jg={}

class Tuisec:
    def __init__(self,headers,url):
        self.headers=headers
        self.url=url

    def zhuaqu(self,path):
        paths=str(self.url).rstrip('/')+str(path).strip()
        rbt=requests.get(url=paths,headers=self.headers)
        go=re.findall('<a href=".*" target="_blank" rel=".*">.*</a>',rbt.text)
        go=list(set(go))
        for a in go:
            bt=BeautifulSoup(a,'html.parser')
            for c in bt.find_all('a'):
                href=str(c.get('href')).replace('/go/','')
                if 'https' in href:
                    pass
                else:
                    tg=bytes.decode(base64.b64decode(href),encoding='utf-8')
                    try:
                        rvt=requests.get(url=tg,headers=headers,timeout=3)
                        rk=BeautifulSoup(rvt.text,'html.parser')
                        for t in rk.find_all('title'):
                            jg[(str(t.get_text()).replace('\n','').strip())]=rvt.url

                    except Exception as r:
                        print('错误:{}'.format(r))
                        pass

    def sjk(self):
        db = pymysql.connect(host=config.HOST,port=config.PORT,user=config.USERNAME, passwd=config.PASSWORD, db=config.DATABASE)
        current = db.cursor()
        try:
            key=list(jg.keys())
            value=list(jg.values())
            for k in range(0,len(key)):
                sql="select * from urls where url='{}'".format(value[k])
                zx=current.execute(sql)
                if zx==0:
                    sql="insert into urls(title,url) values ('{}','{}')".format(key[k],value[k])
                    current.execute(sql)
                    db.commit()
                    print('成功将title:{} url:{}写入数据库'.format(key[k],value[k]))
                else:
                    print('发现重复不写入数据库')
        except:
            db.rollback()

    def xc(self,detail):
        reg=[]
        for e in detail:
            reg.append(gevent.spawn(self.zhuaqu,e))

        gevent.joinall(reg)
        self.sjk()

    def djc(self):
        rw=[]
        calc=0
        rqt=requests.get(url=self.url,headers=self.headers,timeout=3)
        detail=re.findall('/detail/.*"\s',rqt.text)
        for d in detail:
            if calc==100:
                p=Process(target=self.xc,args=(rw,))
                p.start()
                calc=0
                rw.clear()
            rw.append(str(d).replace('"',''))
            calc+=1

        if len(rw)>0:
            p = Process(target=self.xc, args=(rw,))
            p.start()
if __name__ == '__main__':
    headers={'user-agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)'}
    urls='https://paper.tuisec.win/'
    while True:
        obj=Tuisec(headers=headers,url=urls)
        try:
            obj.djc()
        except requests.exceptions.ConnectionError:
            print('网络超时，程序退出....<= =>')
            exit()
        time.sleep(config.TIME)