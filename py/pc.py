import requests
from bs4 import BeautifulSoup

url = 'http://wlj.nanjing.gov.cn/whyw/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 获取新闻列表
news_list = soup.select('.list-right-con li')

# 遍历新闻列表，获取每篇新闻的标题和链接
with open('C:\\Users\\10675\\Desktop\\news1.txt', 'w', encoding='utf-8') as f:
    for news in news_list:
        news_url = news.select_one('a')['href']
        news_response = requests.get(url+news_url[1:])
        news_response.encoding = 'utf-8'
        news_soup = BeautifulSoup(news_response.text, 'html.parser')
        news_content = news_soup.select_one('view TRS_UEDITOR trs_paper_default trs_web').get_text().strip()
        f.write(news_content + '\n\n')