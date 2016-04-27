
# coding: utf-8

# In[ ]:

#網頁抓取
#說明文件 https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
import requests
from bs4 import BeautifulSoup

res = requests.get("網址列")
soup = BeautifulSoup(res.text, "lxml")

for name in soup.select("tag位址"):
    print (name.text)

#-------------------------------------------------------

#資料庫連接
import pymysql

connection = pymysql.connect(host="127.0.0.1", user="名字", passwd="密碼", db="資料庫名字",charset='utf8')

try:
    with connection.cursor() as cursor:
        sql = "INSERT into actor(name) values(\"{}\")" #前者為table及其屬性，後者為要放進去的值
        cursor.execute(sql.fortmat("放入值"))
    
    #若有修改到資料庫，必須有這行才會執行動作
    connection.commit()
    
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `actor` WHERE `id`=1" #基本sql指令
        cursor.execute(sql)
            
        for i in cursor:
            print (i)    
finally:
    connection.close()
    
#--------------------------------------------------------

#正規表示法運用
#以下是判斷單字是否為中文字(已轉成ASCII)，並回傳true/false
re.search(u'[\u4e00-\u9fa5]+',"單字")

#正規表示法可參照下列網頁
#http://marco79423.twbbs.org/articles/%E6%B7%BA%E8%AB%87-regex-%E5%8F%8A%E5%85%B6%E6%87%89%E7%94%A8/
#http://ccckmit.wikidot.com/regularexpression


# In[ ]:

#ALTER TABLE tablename AUTO_INCREMENT = 1
#update actor set id=id+12817
import requests
from bs4 import BeautifulSoup
import pymysql

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')

try:
    '''with connection.cursor() as cursor:
        res = requests.get('http://www.imdb.com/title/tt4991632/fullcredits?ref_=tt_cl_sm#cast')
        soup = BeautifulSoup(res.text,'lxml')
        sql = "INSERT into actor(name) values(%s)"
        for name in soup.select('.itemprop')[::2]:
            cursor.execute(sql,(' '.join(name.text.split())),)
            print (name.text.split())
    
    connection.commit()'''
    
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `actor` WHERE `id`=1"
        cursor.execute(sql)
        with open('temp.txt','w') as f:
            for i in cursor:
                print (i)
                f.write(str(i))
    
finally:
    connection.close()


# In[2]:

from urllib.request import urlopen
import json
u = urlopen('http://www.imdb.com/xml/find?json=1&nr=1&nm=on&q=Leonardo+DiCaprio')
resp = json.loads(u.read().decode('utf-8'))
print (resp['name_popular'])
print ()
for i in resp['name_approx']:
    print (i)


# In[9]:

from urllib.request import urlopen
#http://imdb.wemakesites.net/api/IMDB_RESOURCE_ID
u = urlopen('http://imdb.wemakesites.net/api/nm0000138')
resp = json.loads(u.read().decode('utf-8'))
for i in resp['data']['filmography']:
    print (i)


# In[4]:

#建立oscar的staff和id表
#待解決問題：staff表內的重複資訊，如：Ridley Scott
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import pymysql
import time

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')
movie = ['Spotlight','The Big Short','Bridge of Spies','Brooklyn','Mad Max: Fury Road','The Martian','The Revenant','Room']
mid = {}

u = 'http://www.omdbapi.com/?t={}&y=&plot=short&r=json'
cast = 'http://www.imdb.com/title/{}/fullcredits?ref_=tt_cl_sm#cast'

#從電影名稱得到電影ID
for file in movie:
    url = urlopen(u.format('+'.join(file.split())))
    resp = json.loads(url.read().decode('utf-8'))
    mid[file] = resp['imdbID']


try:
    #staff
    with connection.cursor() as cursor:
        sql = "INSERT into staff(staff_name,staff_id,movie_name) values(\"{}\",\"{}\",\"{}\")"
        
        mv = {}
        
        for i in movie:
            mv[i] = []
        
        for i in mid:
            #print (cast.format(mid[i]))
            res = requests.get(cast.format(mid[i]))
            soup = BeautifulSoup(res.text,'lxml')

            print (i,mid[i])
            for name in soup.select('.itemprop')[::2]:
                #print (name.text.strip())
                #print (name.text.strip(),i,name.a['href'].split('/')[2])
                #print (sql.format(name.text.strip(),i))
                #print (name.text.strip(),i)
                temp = (name.text.strip(),name.a['href'].split('/')[2])
                if temp not in mv[i]:
                    mv[i].append(temp)
                #cursor.execute(sql.format(name.text.strip(),i))
                
            for name in soup.select('.name > a'):
                #print (name.prettify())
                #print (name.text.strip(),i,name['href'].split('/')[2])
                #print (name.text.strip(),i)
                temp = (name.text.strip(),name['href'].split('/')[2])
                if temp not in mv[i]:
                    mv[i].append(temp)
                #cursor.execute(sql.format(name.text.strip(),i))
                             
        for i in mv:
            for j in mv[i]:
                #print (sql.format(j[0],j[1],i))
                cursor.execute(sql.format(j[0],j[1],i))
                #time.sleep(0.5)
    
    #movie
    '''with connection.cursor() as cursor:
        sql = "INSERT into movie(movie_name,movie_id) values(\"{}\",\"{}\")"
        for i in mid:           
            cursor.execute(sql.format(i,mid[i]))'''
    
    #id
    '''with connection.cursor() as cursor:
        sql = "INSERT into id(staff_name,staff_id) values(\"{}\",\"{}\")"
          
        idd = {}    
            
        for i in mid:
            #print (cast.format(mid[i]))
            res = requests.get(cast.format(mid[i]))
            soup = BeautifulSoup(res.text,'lxml')
            
            print (i,mid[i])
            for name in soup.select('.itemprop')[::2]:
                nid = name.a['href'].split('/')[2]
                n = name.text.strip()
                
                if n not in idd:
                    idd[n] = [nid]
                elif nid not in idd[n]:
                    idd[n].append(nid)
                #cursor.execute(sql.format(name.text.strip(),name.a['href'].split('/')[2]))
                
            for name in soup.select('.name > a'):
                nid = name['href'].split('/')[2]
                n = name.text.strip()
                
                if n not in idd:
                    idd[n] = [nid]
                elif nid not in idd[n]:
                    idd[n].append(nid)
                #cursor.execute(sql.format(name.text.strip(),name['href'].split('/')[2]))
        
        gg = 0
        for j in idd:
            gg = gg + len(idd[j])
            #if len(idd[j]) > 1:
            #    print (len(idd[j]),j,idd[j])
            for k in idd[j]:
                #print (j,k)
                cursor.execute(sql.format(j,k))
                #time.sleep(0.5)'''
                
        #print (len(idd)) #5787
        #print (gg) #5795
    connection.commit()
    
finally:
    connection.close()


# In[38]:

#建立oscar的node
import pymysql
import codecs

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')

try:
    with codecs.open('oscar_node.txt','r','utf8') as f:
        with connection.cursor() as cursor:
            sql = "select `id`,`staff_name` from `staff`"
            cursor.execute(sql)
            
            for i in cursor:
                print (i)
            
            f.write("id\tnode\n")
            
            temp = []
            con = 0
            for name in cursor:
                try:
                    if name[1] in temp:
                        print (name[1])
                        con = con + 1
                    else:
                        temp.append(name[1])
                        f.write("{}\t{}\n".format(name[0]-con,name[1]))
                except:
                    print (name)
                    continue
finally:
    connection.close()


# In[36]:

#建立oscar的link
import pymysql
import codecs
import time

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')

try:
    with codecs.open('oscar_link.txt','w','utf8') as f:
        with connection.cursor() as cursor:
            sql = "select `id`,`staff_name` from `staff`"
            cursor.execute(sql)
            
            dic = {}
            con = 0
            for i in cursor:
                if i[1] not in dic:
                    dic[i[1]] = i[0] - con
                else:
                    con = con + 1
                    
            sql = "select `staff_name`,`movie_name` from `staff`"
            cursor.execute(sql)
            
            movie = {}
            for i in cursor:
                if i[1] in movie:
                    movie[i[1]].append(dic[i[0]])
                else:
                    movie[i[1]] = [dic[i[0]]]
                    
            link = {}
            for file in movie:
                l = len(movie[file])
                n = sorted(movie[file])
                for i in range(l):
                    for j in range(l-i-1):
                        c = j + i + 1
                        temp = (n[i],n[c])
                        if temp in link:
                            link[temp] = link[temp] + 1
                        else:
                            link[temp] = 1
            

            f.write("source\ttarget\ttype\tweight\n")
            for idd in link:
                try:
                    f.write("{}\t{}\t{}\t{}\n".format(idd[0],idd[1],'Undirected',link[idd]))
                except:
                    print (name)
                    continue
finally:
    connection.close()


# In[3]:

import requests
from bs4 import BeautifulSoup

url = 'http://www.imdb.com/title/tt1596363/fullcredits?ref_=tt_cl_sm#cast'

res = requests.get(url)
soup = BeautifulSoup(res.text,'lxml')

for name in soup.select('.name > a'):
    #print (name.prettify())
    print (name.text.strip(),name['href'].split('/')[2])
    print ()


# In[28]:

import pymysql
import codecs
import time

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')

try:
    with connection.cursor() as cursor:
        sql = "select distinct `staff_id` from `{}`"
    
        sst = []
        idd = []
        
        cursor.execute(sql.format('staff'))
        
        for i in cursor:
            sst.append(i[0])
        
        cursor.execute(sql.format('id'))
        
        for i in cursor:
            if i[0] not in sst:
                print (i[0])

        
    
finally:
    connection.close()


# In[28]:

#包含職位的IMDB資料提取
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import pymysql
import time

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')

movie = ['Spotlight','The Big Short','Bridge of Spies','Brooklyn','Mad Max: Fury Road','The Martian','The Revenant','Room']
mid = {}

u = 'http://www.omdbapi.com/?t={}&y=&plot=short&r=json'
member = 'http://www.imdb.com/title/{}/fullcredits?ref_=tt_cl_sm#cast'

job = []
g = []

#從電影名稱得到電影ID
for file in movie:
    url = urlopen(u.format('+'.join(file.split())))
    resp = json.loads(url.read().decode('utf-8'))
    mid[file] = resp['imdbID']

try:
    with connection.cursor() as cursor:

        sql = "INSERT into staff(staff_name,staff_id,movie_id,job) values(\"{}\",\"{}\",\"{}\",\"{}\")"

        for file in mid:
            res = requests.get(member.format(mid[file]))
            soup = BeautifulSoup(res.text,'lxml')

            term = ''

            print (file,mid[file])
            
            #針對不同位置作抓取調整
            for i in soup.select('#fullcredits_content'):
                for j in i.find_all(class_=['dataHeaderWithBorder','simpleTable','cast_list']):
                    #print (j.get_text(strip=True))
                    #print (j['class'])

                    if j['class'][0] == 'dataHeaderWithBorder':
                        temp = j.get_text(strip=True)
                        if temp.split()[-1] != 'by' and temp.split()[-1] != 'By':
                            #print (temp)
                            term = temp
                        else:
                            #print (' '.join(temp.split()[:-1]))
                            term = ' '.join(temp.split()[:-1])
                        if term not in job:
                            job.append(term)
                    elif j['class'][0] == 'simpleTable':
                        for l in j.select('.name'):
                            #print (l.get_text(strip=True),l.a['href'].split('/')[2],term)
                            cursor.execute(sql.format(l.get_text(strip=True),l.a['href'].split('/')[2],mid[file],term))

                    elif j['class'][0] == 'cast_list':
                        '''for k in j.select('.itemprop')[::2]:
                            print (k.get_text(strip=True),k.a['href'].split('/')[2],'cast')
                            #cursor.execute(sql.format(k.get_text(strip=True),k.a['href'].split('/')[2],mid[file],'cast'))
                            pass'''
                        for k in j.find_all(class_=['itemprop','castlist_label']):
                            if k['class'][0] == 'castlist_label':
                                if k.get_text() != '':
                                    #print (k.get_text(strip=True))
                                    term = 'Rest of cast'
                                else:
                                    term = 'cast'
                                
                                if term not in job:
                                    job.append(term)
                            elif k['itemprop'] == 'actor':
                                #print (k.get_text(strip=True),k.a['href'].split('/')[2],mid[file],term)
                                cursor.execute(sql.format(k.get_text(strip=True),k.a['href'].split('/')[2],mid[file],term))

                                    
            print ()
        print (job)
        
    connection.commit()
finally:
    connection.close()

