from time import sleep
import htmlScraper 
import pandas as pd
from dataclasses import dataclass

@dataclass
class House:
    listing_name: str
    location : str
    price: int
    bedrooms: int
    bathrooms: float

@dataclass
class Listing:
    title: str
    price: str
    location: str
    description: str
    link: str

def scrape_number_of_pages_from_search(start_url,number_of_paes_to_scrape):
    page_counter = 0
    current_url = start_url
    phones = []
    while page_counter <= number_of_paes_to_scrape:
        page_counter += 1
        current_url = get_next_url_from_url(current_url,page_counter)
    return page_counter



def get_next_url(page):
    next_button = htmlScraper.get_button_by_title(page,"Next")
    link = htmlScraper.get_link(next_button)
    page_link = "https://www.kijiji.ca{}".format(link)
    return page_link

def get_next_url_from_url(url, next_page_number):
    parts = url.split('/')
    next_page = "page-{}".format(next_page_number)
    if next_page_number > 2:
        parts[5] = next_page
    else:
        next_page = "page-{}".format(next_page_number)
        parts.insert(5,next_page)
    next_url = ''
    for part in parts:
        next_url += part + '/'
    
    return next_url[:-1]  #accounts for trailing slash

def get_listing_page(page_url):
    page = htmlScraper.scrape_page(page_url)
    return page

def get_listings_from_page_url(page_url):
    listing_page = get_listing_page(page_url)
    return get_listings_from_page(listing_page)

def get_listings_from_page(listing_page):
    listing_divs = htmlScraper.get_all_divs_by_class(listing_page, 'info-container')
    listings = []
    for listing in listing_divs:
        price = htmlScraper.get_div_text_by_class(listing, 'price', contains_div=True)
        price = price.strip()
        title = htmlScraper.get_div_text_by_class(listing, 'title', 'a')
        title = title.strip()
        location = htmlScraper.get_div_by_class(listing, 'location')
        location = htmlScraper.get_div_text_by_class(location,"","span")
        location = location.strip()
        title_div = htmlScraper.get_div_by_class(listing,'title')
        link = htmlScraper.get_link(title_div)
        full_link = "https://kijiji.ca{}".format(link)
        description = htmlScraper.get_div_text_by_class(listing, 'description', contains_div = True)
        description = description.strip()
        listings.append(Listing(title,price,location,description,full_link))
    if len(listings) == 0:
        print("No listings found on page")
        with open("pageoutput.txt","w") as f:
            f.write(listing_page)
    return listings 


def get_house_from_listing(listing: Listing):
    house_page = htmlScraper.scrape_page(listing.link)
    attributes = htmlScraper.get_all_divs_by_class(house_page,"attributeValue-2574930263","dd")
    bedrooms = 0
    bathrooms = 0

    if len(attributes) > 0:
        try:
            bedrooms = htmlScraper.get_div_text(attributes[0],"dd")
            bathrooms = htmlScraper.get_div_text(attributes[1],"dd")

            if bedrooms == "6+" or bedrooms == "6 chambres ou plus":
                bedrooms = 7
            elif "chambre" in bedrooms:
                bedrooms = bedrooms[0]
                bedrooms = int(bedrooms)
            else:
                bedrooms = int(bedrooms)

            if bathrooms == "6+" or bathrooms == "6 ou plus":
                bathrooms = 7
            else:
                bathrooms = float(bathrooms)

        except ValueError:
            print("Value error on page {}".format(listing.link))

    price = convert_price_to_int(listing.price)
    house = House(listing.title,listing.location,price,bedrooms,bathrooms)
    return house

def is_investment_property(house: House):
    return  "plex" in house.listing_name.lower()

def get_houses_from_url(url):
    listings = get_listings_from_page_url(url)
    houses = [get_house_from_listing(listing) for listing in listings]
    return houses

def get_next_url_from_url(url, next_page_number):
    parts = url.split('/')
    next_page = "page-{}".format(next_page_number)
    if next_page_number > 2:
        parts[5] = next_page
    else:
        next_page = "page-{}".format(next_page_number)
        parts.insert(5,next_page)
    next_url = ''
    for part in parts:
        next_url += part + '/'
    
    return next_url[:-1]  #accounts for trailing slash

def scrape_number_of_pages_from_search(start_url,number_of_pages_to_scrape):
    page_counter = 1
    current_url = start_url
    houses = []
    while page_counter <= number_of_pages_to_scrape:
        print(current_url)
        page = get_listing_page(current_url)
        page_listings = get_listings_from_page(page)
        page_houses = [get_house_from_listing(listing) for listing in page_listings]
        if len(page_houses) == 0:
            print("no houses found, retry once")
            sleep(90)
            
            page_houses = get_houses_from_url(current_url)
        houses = houses + page_houses
        page_counter += 1
        current_url = get_next_url_from_url(current_url,page_counter)
    return houses

def scrape_from_file_links(path: str, number_of_pages: int = 1):
    with open(path, "r") as f:
        links = f.readlines()
        links = [link.strip() for link in links]
        link_houses = [scrape_number_of_pages_from_search(link, number_of_pages) for link in links]
        houses = []
        for lst in link_houses:
            houses = houses + lst

        return houses

def print_houses_to_csv(path: str,houses: list[House]):
    master_df = pd.DataFrame()
    first_run = True
    for house in houses:
        df = pd.DataFrame([[house.location,house.price,house.bedrooms,house.bathrooms,house.listing_name]],columns=['Location','Price','Bedrooms','Bathrooms','Listing Name'])
        if first_run:
            master_df = df
            first_run = False
        else:
            master_df = pd.concat([master_df,df])
    
    master_df.to_csv("{}.csv".format(path),index=False)
    
def get_csv_from_file_links(path: str, output: str):
    houses = scrape_from_file_links(path, 10)
    print_houses_to_csv(output,houses)


def convert_price_to_int(price: str):
    try:
        price.strip()
        if '$' not in price:
            return -1
        elif price.find('$') == 0:
            price = price.replace("$","")
            price = price.replace(",","")
            if "." in price:
                price = price[:-3]
            return int(price)
        else:
            n_price = ""
            for char in price:
                if char.isdigit():
                    n_price += char
                elif char == ',':
                    break
            return int(n_price)
    except ValueError:
        print("Value error on price: {}".format(price))
        

    
        