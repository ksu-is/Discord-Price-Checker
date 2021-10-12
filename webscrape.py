
from bs4 import BeautifulSoup
from epicstore_api import EpicGamesStoreAPI
import requests
from requests_html import *




def steam_grab(title):
    title=title.lower().replace(" ","+")
    #print(title)
    base_steam_url="https://store.steampowered.com/search/?term="
    search_url=base_steam_url+title
    
    print("->",base_steam_url+title)
    #pulls the html from the site
    r=requests.get(search_url).text
    soup = BeautifulSoup(r, 'lxml')
    #will pull the 0 results text on the page if there are no results
    results=soup.find("div",class_="search_results_count")
    
    #filters html down to the list of games and other information
    game_list=soup.find("div",id="search_resultsRows")
    #if nothing is found the game_list is empty and evaluates to false
    if not game_list:
        return results.text
    else:
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
    game_raw=api.fetch_store_games(count=3,keywords=title)
    #creates a huge dictionary list with elements holding the different listings
    game_list=game_raw['data']['Catalog']['searchStore']['elements']
    games=[]
    prices=[]
    #execption if for when no games with the title are found
    if not game_list:
       return "No games with title \""+title+"\" were found :frowning2:"
    else:
        for game in game_list:
            games.append(game['title'])
        index=0
        #filters the needed data out of the dictionary with many catagories of info within it
        for price in game_list:
            games[index]=games[index]+"----Orignal Price: "+price['price']['totalPrice']['fmtPrice']['originalPrice']+"----Discount Price: "+price['price']['totalPrice']['fmtPrice']['discountPrice']
            prices.append(price['price']['totalPrice']['fmtPrice']['intermediatePrice'])
            index+=1
        return games

def play_grab(title):
    title=title.lower().replace(" ","%20")
    search_url="https://store.playstation.com/en-us/search/"+title
    print(search_url)
    session=HTMLSession()
    
    r=session.get(search_url)
    r.html.render()
    soup = BeautifulSoup(r.html.html, 'lxml')
    
    game_raw=soup.find("ul",class_="ems-sdk-product-tile-list").text
    game_list=game_raw.find_all("li",class_="psw-cell")
    games=[]
    index=0
    for game in game_list:
        title=game
        title=title.find("span",class_="psw-body-2 psw-truncate-text-2 psw-p-t-2xs").text
        games.append(title)
        price=game
        price=price.find("span",class_="price").text
        games[index]=games[index]+"----"+price
        index+=1
    return games
    
        

def ebay_grab(title):
    title=title.lower().replace(" ","+")
    search_url="https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw="+title+"&_sacat=1249&LH_TitleDesc=0"
    print("->",search_url)
    #pulls the html from the site
    r=requests.get(search_url).text
    soup = BeautifulSoup(r, 'lxml')
    #the li on the page each hold one listing with the price, format, and shipping info within them 
    li_list=soup.find_all("div",class_="s-item__wrapper")
    li_list.pop(0)
    listings=[]
    #extracts title, price, format and shipping
    for li in li_list:
    
         title=li.find("h3",class_="s-item__title")
         title=title.text   
         
         price=li.find("span",class_="s-item__price")
         price=price.text   

         format=li.find("span",class_="s-item__purchase-options-with-icon")
         if not format:
             format=li.find("span",class_="s-item__bids")
         format=format.text
# shipping can have threee forms with the normal shipping info or sepcial shipping either with X amount of days within a span
#or special shipping without the extra span
         shipping=li.find("span",class_="s-item__shipping")
         #print(shipping)
         if not shipping:
             shipping=li.find("span",class_="s-item__dynamic")
             shipping=shipping.contents[0]
         #print(shipping)
         try:
             shipping=shipping.text
         except:
            pass
         listings.append(title+"----"+price+"----"+format+"----"+shipping)
                
    url_list=[]
    
    for a in li_list:
        link=a.find("a",class_="s-item__link")
        url_list.append(link["href"])
    #first url pulled is always a dead link with the second item in the list the first item for sale
    del url_list[0]
    
    return listings,url_list

print(play_grab("portal"))