from ipeenModule.CrawlerMudule import IpeenCrawlwr
import time
DOWNLOAD_URL ='http://www.ipeen.com.tw/shop/74600-P-P%E7%BE%A9%E6%B3%95%E5%89%B5%E6%84%8F%E5%BB%9A%E6%88%BF-%E8%A5%BF%E9%96%80%E5%BA%97'
root= 'http://www.ipeen.com.tw'
                
if __name__ == '__main__':
    cr=IpeenCrawlwr(root)
    url=DOWNLOAD_URL
    bc=[]#存放要抓取的總頁數
    bc.append(url)
    while url:
        html = cr.download_page(url)   
        time.sleep(1)
        url=cr.parse_html(html)#找尋下一頁如果找不到回傳None
        bc.append(url)
    cr.get_all_article_link(bc)#抓評論
    

        