import requests
import re
import MySQLdb
from bs4 import BeautifulSoup
import time

class IpeenCrawlwr():
    def __init__(self,root):
        self.ROOT_URL=root
    
    def download_page(self,url):
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
        }
        data = requests.get(url,headers=headers).content
        return data

    def parse_html(self,html):
        # 找到有包含下一頁的標籤直到沒有        
        #soup=BeautifulSoup(html,"html.parser")方式一
        soup=BeautifulSoup(html,"lxml")#方式二           
        next_page =soup.find('div', attrs={'class': 'page-block'}).find('a',attrs={"data-label": "下一頁"})   
        if next_page:
            return self.ROOT_URL + next_page['href']
        return None

    def get_all_article_link(self,list):
        # 分析各頁面內文章內容
        for i in list:
            Request_list = requests.get(i)
            #if Request_list.status_code == requests.codes.ok:
                #soup = BeautifulSoup(Request_list.content, "html.parser")方式一
            soup = BeautifulSoup(Request_list.content, "lxml")#方式二
            all_article_link_tag = soup.find_all('a', attrs={'data-label': '文章標題'})        
            for link in all_article_link_tag:
                page_link = self.ROOT_URL + link['href']                            
                self.all_article_information(page_link)#呼叫獲取評論的方法
                time.sleep(1)

    def all_article_information(self,page_link):
        PATH = 'comment/'
        id = re.sub(re.compile(r'^.*/' + PATH), '', page_link).split('/')[0]
        print(id)
        intid=int(id)        
        req = requests.get(page_link)
        #if req.status_code == requests.codes.ok:
        soup = BeautifulSoup(req.content, "html.parser")
        title=soup.find('h1',itemprop="headline").text
        share=int(soup.find('a', attrs={'data-label': '給予評價的網友數'}).find('b').text)
        all_article_tag = soup.find('div', class_="description").text           
        all_article_score_tag = soup.find('div', class_="scalar")
        score=int(all_article_score_tag.meter['value'])
        db = MySQLdb.connect(host="localhost", user="han", passwd="123456789",db="ipeen")
        db.set_character_set('utf8')
        cursor = db.cursor()
        cursor.execute('SET NAMES utf8;')
        #sql = "INSERT IGNORE INTO data2 (id,URL,Comment,Score) VALUES ({},'{}','{}',{}) ".format(int(id),page_link,all_article_tag,int(all_article_score_tag.meter['value']) )          
        sql="INSERT IGNORE INTO newdata3(id,URL,Comment,Score,Title,Share)VALUES(%s,%s,%s,%s,%s,%s)" #略過重複資料 
        cursor.execute(sql,(intid,page_link,all_article_tag,score,title,share))
        cursor.close()
        db.commit()
        db.close()             

class IpeenCrawlwr2():
    #用來更新資料
    def __init__(self):
        pass

    def getURL(self,id2,URL):
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
        }    
        data = requests.get(URL,headers=headers)
        soup = BeautifulSoup(data.content,"lxml")
        title=soup.find('h1',itemprop="headline").text
        share=int(soup.find('a', attrs={'data-label': '給予評價的網友數'}).find('b').text)
        db = MySQLdb.connect(host="localhost", user="han", passwd="123456789",db="ipeen")
        db.set_character_set('utf8')
        cursor = db.cursor()
        cursor.execute('SET NAMES utf8;')        
        cursor.execute("""
        UPDATE  newdata3
        SET Title=%s, Share=%s
        WHERE id=%s
        """, (title, share,id2))               
        db.commit()
        db.close()       
        #print(title,share)
        
    



        


