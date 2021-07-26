

from bs4 import BeautifulSoup
from epicstore_api import EpicGamesStoreAPI
import lxml
import requests



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
    #pulls the summary text for the top result
    summary_raw=soup.find("div",class_="game_description_snippet")
    try: 
        summary=summary_raw.text
    except Exception:
        summary="No summary found"
    else:
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
    #found an interface made to interact with EpicGamesStore due to the use of javascript to make the pages that 
    #negatated using beautiful soup
 
    api = EpicGamesStoreAPI()
    game_raw=api.fetch_store_games(count=5,keywords=title)
    game_list=game_raw['data']['Catalog']['searchStore']['elements']
    games=[]
    prices=[]
    if not game_list:
       return "No games with title "+title+" where found :("
    else:
        for game in game_list:
            games.append(game['title'])
        index=0
        
        for price in game_list:
            games[index]=games[index]+"\nOrignal Price: "+price['price']['totalPrice']['fmtPrice']['originalPrice']+"\nDiscount Price: "+price['price']['totalPrice']['fmtPrice']['discountPrice']
            prices.append(price['price']['totalPrice']['fmtPrice']['intermediatePrice'])
            index+=1
        return games,prices
    
def ebay_grab(title):
    title=title.lower().replace(" ","+")
    search_url="https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw="+title+"&_sacat=1249&LH_TitleDesc=0"
    print("->",search_url)
    #pulls the html from the site
    r=requests.get(search_url).text
    soup = BeautifulSoup(r, 'lxml')
    game_list=soup.find("ul",id="srp-results")
    
    
    
    price_raw=game_list.find_all("span",class_="s-item__price")
    li_list=soup.find_all("div",class_="s-item__wrapper")
    li_list.pop(0)
    listings=[]
    
    for li in li_list:
    
         title=li.find("h3",class_="s-item__title")
         title=title.text   
         print(title)
         price=li.find("span",class_="s-item__price")
         price=price.text   
         print(price)
         listings.append(title+"----"+price)
         
        
            
    url_list=[]
    
    for a in li_list:
        link=a.find("a",class_="s-item__link")
        url_list.append(link["href"])
    #first url pulled is always a dead link with the second item in the list the first item for sale
    del url_list[0]
    format_raw=game_list.find_all("span",class_="s-item__purchase-options-with-icon")
    shipping_raw=game_list.find_all("span",class_="s-item__shipping")
    #print(title_raw)
    title_list=[]
    index=0
    #takes only the text within the tags and creates a list that has the title and price in each index
    for title in title_raw:
        
        title_list.append(title.text)
        title_list[index]=title_list[index].lower()
        index+=1

    index=0
    print(len(title_raw))
    print(len(price_raw))
    #repeats above for different info adding to it the title
    for price in price_raw:
        cost=price.text
        title_list[index]=title_list[index]+"-------"+cost
        index+=1
    index=0
    for formats in format_raw:
        format=formats.text
        title_list[index]=title_list[index]+"-------"+format
        index+=1
    index=0
    for price in shipping_raw:
        cost=price.text
        title_list[index]=title_list[index]+"-------"+cost
        index+=1 
    #return title_list,url_list
    

ebay_grab("destroy all humans")
