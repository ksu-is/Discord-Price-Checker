from bs4 import BeautifulSoup

import requests
import os


def steam_grab(title):
    title=title.lower().replace(" ","+")
    #print(title)
    base_steam_url="https://store.steampowered.com/search/?term="
    search_url=base_steam_url+title
    
    print("->",base_steam_url+title)
   #search_result_row ds_collapse_flag app_impression_tracked
    r=requests.get(search_url).text
    soup = BeautifulSoup(r, 'lxml')
    exception_raw=soup.find("div",id="search_results_filtered_warning_persistent")
    exception=exception_raw.text
    
    game_list=soup.find("div",id="search_resultsRows")
    summary_url=game_list.find("a").attrs['href']
    r=requests.get(summary_url).text
    soup = BeautifulSoup(r, 'lxml')
    summary_raw=soup.find("div",class_="game_description_snippet")
    summary=summary_raw.text
    summary.strip()
    summary=summary.strip("\r\n\t")
    title_raw=game_list.find_all("span",class_="title")
    price_raw=game_list.find_all("div",class_="search_price")
    title_list=[]
    index=0
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
    
    #return title_list,summary,summary_url
    print(exception_raw)
        

steam_grab("star wars")

