import re
import requests
import time
import urllib.request
import random
from bs4 import BeautifulSoup
import pymysql

dbconfig={
	'host':'localhost',
	'port':3306,
	'user':'root',
	'password':'11325454',
	'db':'ct',
	'charset':'utf8'
}

def getUrllist(urllist,keyword,pagenum,option,cursor):
	kw=urllib.request.quote(keyword)
	if option==1:		
		for i in range(1,pagenum):
			url='http://weixin.sogou.com/weixin?type=2&query='+kw+'&page='+str(i)
			data1=requests.get(url).text
			urllist.append(re.compile(r'<div class="txt-box">.*?(http://.*?)"',re.S).findall(data1))
		return urllist
	if option==2:
		for i in range(1,pagenum):
			url='http://weixin.sogou.com/weixin?type=1&query='+kw+'&page='+str(i)
			data1=requests.get(url).text
			urllist.append(re.compile(r'<div class="txt-box">.*?(http://.*?)"',re.S).findall(data1))
		return urllist

def getpage(soup,k,cursor,no,url):
	imgurllist=[]
	print('No.'+str(k)+' '+str(soup.title.string)+'\n')
	#print('img src:\n')
	img_urllist=soup.find_all('img')
	imgurl_pattern=re.compile(r'data-src="(.*?)"')
	for s in img_urllist:
		match=imgurl_pattern.search(str(s))
		if match:
			imgurl=match.group(1)
			imgurllist.append(imgurl)
	imgurlstr=",".join(imgurllist)
	[s.decompose() for s in soup.find_all('script')]
	[s.decompose() for s in soup.find_all('style')]
	posttime=soup.find(id="post-date",class_="rich_media_meta rich_media_meta_text")
	postuser=soup.find(id="post-user",class_="rich_media_meta rich_media_meta_link rich_media_meta_nickname")
	# print('post-time:'+posttime.string)
	# print('post-user:'+postuser.string)
	sql=''
	sql="INSERT INTO "+"`"+str(no)+"`"+" (No, title, posttime, postuser, content, url, imgurl) VALUES('"+str(k)+"','"+soup.title.string+"','"+posttime.string+"','"+postuser.string+"','"+soup.get_text()+"','"+url+"','"+imgurlstr+"')"
	# print(sql)
	cursor.execute(sql)
	db.commit()
	print('Successfully Insert', cursor.rowcount, ' Pieces Of Data!')
	return k



def getContent(urllist,option,cursor,k,keyword):
	i=j=k=1
	for i in range(0,len(urllist)):
		for j in range(0,len(urllist[i])):
			if urllist[i][j]:
				url=urllist[i][j]
				url=url.replace("amp;","")
				# print(url)
				time.sleep(random.randint(3,5))
				soup=BeautifulSoup(requests.get(url).text,"lxml")
				if option==1:
					try:
						getpage(soup,k,cursor,keyword,url)
						k=k+1
					except:
						print('ERROR!!!')
						j=j-1
				if option==2:
					articalList=[]
					accountname=soup.find(class_="a")
					print('Account Name: '+soup.title.string)
					temp=soup.find_all('script')[len(soup.find_all('script'))-2]
					articalList.append(re.compile(r'"app_msg_ext_info":{(.*?)}',re.S).findall(str(temp)))					
					for m in range(0,len(articalList[0])):
						try:
							thisArtical=articalList[0][m]
							author=re.search(r'author":"(.*?)"',thisArtical).group(1)
							contenturl=re.search(r'content_url":"(.*?)"',thisArtical).group(1)
							completeUrl='https://mp.weixin.qq.com'+re.search(r'content_url":"(.*?)"',thisArtical).group(1)
							completeUrl=completeUrl.replace("amp;","")
							coverimgurl=re.search(r'"cover":"(.*?)"',thisArtical).group(1)
							title=re.search(r'title":"(.*?)"',thisArtical).group(1)
							digest=re.search(r'digest":"(.*?)"',thisArtical).group(1)
							page=BeautifulSoup(requests.get(completeUrl).text,'lxml')
							time.sleep(random.randint(3,5))
							getpage(page,k,cursor,keyword,completeUrl)
							k=k+1
						except:
							print('ERROR!!!')
							m=m-1

if __name__=='__main__':
	no=1
	option=int(input('please choose a function--1 for theme search--2 for public account search:\n'))
	while option==1 or option==2:
		urllist=[]
		keyword=''
		pagenum=1
		k=1
		db=pymysql.connect(**dbconfig)
		cursor=db.cursor()
		if option==1:
			keyword=input('please enter a keyword:\n')
			if keyword!='':
				print('successfully enter the keyword')
				pagenum=int(input('please enter the number of page you want to search:\n'))+1
				sql1='DROP TABLE IF EXISTS '+'`'+str(keyword)+'`; '
				sql2='CREATE TABLE '+'`'+str(keyword)+'`'+ '(`No` varchar(100) DEFAULT NULL, `title` varchar(100) DEFAULT NULL,`posttime` varchar(100) DEFAULT NULL,`postuser` varchar(100) DEFAULT NULL,`content` longtext,`url` longtext,`imgurl` longtext) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; '
				cursor.execute(sql1)
				cursor.execute(sql2)
		elif option==2:
			keyword=input('please enter a account number:\n')
			if keyword!='':
				print('successfully enter the account\n')
				pagenum=int(input('please enter the number of page you want to search:\n'))+1
				sql1='DROP TABLE IF EXISTS '+'`'+str(keyword)+'`; '
				sql2='CREATE TABLE '+'`'+str(keyword)+'`'+ '(`No` varchar(100) DEFAULT NULL, `title` varchar(100) DEFAULT NULL,`posttime` varchar(100) DEFAULT NULL,`postuser` varchar(100) DEFAULT NULL,`content` longtext,`url` longtext,`imgurl` longtext) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; '
				cursor.execute(sql1)
				cursor.execute(sql2)
		getUrllist(urllist,keyword,pagenum,option,cursor)
		getContent(urllist,option,cursor,k,keyword)
		print('\n!!!!!!!!!!!!!!!!!![[SEARCH IS OVER]]!!!!!!!!!!!!!!!!!!\n')
		no=no+1
		option=''
		option=int(input('please choose a function--1 for theme search--2 for public account search--3 for quit:\n'))	
	db.close()
	print('##############[[Application Quit Successfully]]##############')
