from tools import get_soup
import copy
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup



def get_soup(url):
    headers={
        'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) 
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'''
            }
    
    try:
        res=requests.get(url,headers=headers)
        res.encoding = 'utf-8'
    
        if res.status_code==200:
            return BeautifulSoup(res.text,'lxml') 
        else:
            return res.status_code
        
    except Exception  as e:
        print(e)
        
        return None


def get_movieinfo(url,show=False):
    soup=get_soup(url)     
    #圖片
    photo=soup.find('div',class_="movie_intro_info_l").find('img').get('src')
   
    #預告片
    video=soup.find('div',class_="color_btnbox").find('a',class_="btn_s_vedio").get('href')

    #電影資訊
    main3=soup.find('div',class_='movie_intro_info_r').find_all('span')
    date=main3[0].text.split('：')[-1]
    time=main3[1].text.split('：')[-1]
    imdb=main3[2].text.split('：')[-1]
    score=soup.find('div',class_="score_num count").text.strip()
    
    if show==True:
        print(photo,video,date,time,imdb,score)
    
    return photo,video,date,time,imdb,score


def save_pic(url,file_name):
    print(file_name)
    try:
        resp=requests.get(url)
        with open(f'{file_name}','wb') as f:
            f.write(resp.content)
        print('save.')
    except Exception as e:
        print(e)  



#=========================================================================


url='https://movies.yahoo.com.tw/chart.html'
soup=get_soup(url)
trs=soup.find(class_='rank_list table rankstyle1').find_all(class_="tr")


datas=[]
for i,tr in enumerate(trs[1:]):
    tds=[td for td in tr.find_all('div',class_='td')]
    rank=tds[0].text.strip()
    if i==0:
        title=tds[3].h2.text.strip()
    else:
        title=tds[3].text.strip()
    link=tds[3].find('a').get('href')
    datas.append([rank,title,link])
    

temp_data=copy.deepcopy(datas)
#print(temp_data)
for d in temp_data:
    info=get_movieinfo(d[2])
    d.extend(info)
    

df=pd.DataFrame(temp_data,columns=[
    'rank','title','movie_url','image_url','video_url','date','length',
    'company','score'])
df.to_csv('movie_top20.csv',encoding='utf-8-sig')


path='images/'   #images/xxx.jpg
if not os.path.exists(path):
    os.mkdir(path)
    
for title,url in df[['title','image_url']].values:
    save_pic(url,f'{path}{title}.jpg')


