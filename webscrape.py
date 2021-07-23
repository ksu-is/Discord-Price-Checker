from bs4 import BeautifulSoup
from epicstore_api import EpicGamesStoreAPI
import requests
import os


def steam_grab(title):
    title=title.lower().replace(" ","+")
    #print(title)
    base_steam_url="https://store.steampowered.com/search/?term="
    search_url=base_steam_url+title
    
    print("->",base_steam_url+title)
    #pulls the html from the site
    r=requests.get(search_url).text
    soup = BeautifulSoup(r, 'lxml')

    #filters html down to the list of games and other information
    game_list=soup.find("div",id="search_resultsRows")
    #pull the url for the first game of the list and pulls the summary from that page
    summary_url=game_list.find("a").attrs['href']
    r=requests.get(summary_url).text
    soup = BeautifulSoup(r, 'lxml')
    summary_raw=soup.find("div",class_="game_description_snippet")
    summary=summary_raw.text
    summary.strip()
    summary=summary.strip("\r\n\t")
    #pulls the titles and prices for all games on the page
    title_raw=game_list.find_all("span",class_="title")
    price_raw=game_list.find_all("div",class_="search_price")
    title_list=[]
    index=0
    #takes only the text within the tags and creates a list that has the title and price in each index
    for title in title_raw:
        
        title_list.append(title.text)
        title_list[index]=title_list[index].replace('™',"").lower()
        index+=1
    index=0
    for price in price_raw:
        cost=price.text
        cost=cost.strip()
        cost=cost.strip("\r\n")
        title_list[index]=title_list[index]+"-------"+cost
        index+=1
    
    return title_list,summary,summary_url

def epic_grab(title):
    title=title.lower().replace(" ","%20")
    #print(title)
    search_url="https://www.epicgames.com/store/en-US/browse?q="+title+"&sortBy=relevance&sortDir=DESC&count=40&start=0"
    print("->",search_url)
    #pulls the html from the site
    r=requests.get(search_url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'})
    print(r.content)
    soup = BeautifulSoup(r, 'lxml')

    game_list=soup.find_all("div",class_="css-zgal9t-DiscoverCardLayout__component")
    #title_raw=game_list.find_all("span",class_="css-2ucwu")
    #price_raw=game_list.find_all("span",class_="css-1mc6sjq")
    #title_list=[]
    #for title in title_raw:
        
        #title_list.append(title.text)
       # title_list[index]=title_list[index].lower()
        #index+=1
   # index=0
    #for price in price_raw:
     #   cost=price.text
      #  cost=cost.strip()
       # title_list[index]=title_list[index]+"-------"+cost
        #index+=1
    
    
def ebay_grab(title):
    title=title.lower().replace(" ","+")
    search_url="https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw="+title+"&_sacat=1249&LH_TitleDesc=0"
    print("->",search_url)
    #pulls the html from the site
    r=requests.get(search_url).text
    soup = BeautifulSoup(r, 'lxml')
    game_list=soup.find("div",id="srp-river-main")
    title_raw=game_list.find_all("h3",class_="s-item__title")
    price_raw=game_list.find_all("span",class_="s-item__price")
    #print(title_raw)
    title_list=[]
    index=0
    #takes only the text within the tags and creates a list that has the title and price in each index
    for title in title_raw:
        
        title_list.append(title.text)
        title_list[index]=title_list[index].lower()
        index+=1
    index=0
    for price in price_raw:
        cost=price.text
        title_list[index]=title_list[index]+"-------"+cost
        index+=1
    for title in title_list:
        print(title)


ebay_grab("frostpunk")