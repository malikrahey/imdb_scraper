import htmlScraper, sys, getopt, argparse
import pandas as pd
from dataclasses import dataclass

@dataclass
class IPhone:
    model: str
    storage: str
    price: str
    description: str
    link: str

@dataclass
class Listing:
    title: str
    price: str
    description: str
    link: str

options = "lno"

long_options = ['link', 'number', 'output']

arguments_list = sys.argv[1:]
parser = argparse.ArgumentParser()

parser.add_argument('-l','--link', dest="link", default='nolink',help="Start Link")
parser.add_argument('-n','--number',dest="number",default=1,help="number of pages to scrape")
parser.add_argument('-o','--output',dest="output",default='result',help='Output filename')

args = parser.parse_args()

def main():
    print("Starting")
    link = args.link
    number = int(args.number)
    output = args.output
    
    if link is None:
        print("We need a link to get started, pass in a link using -l or --link")
        exit()
    print("Starting link: " + link)
    print("Number of pages to scrape " + str(number))
    print("Output file: {}.csv".format(str(output)))
    phones = scrape_number_of_pages_from_search(link,number)

    print('Scraped ' + str(len(phones)) + ' phones')
    master_df = pd.DataFrame()
    first_run = True
    for phone in phones:
        df = pd.DataFrame([[phone.model,phone.storage,phone.price,phone.description,phone.link]],columns=['Model','Storage','Price','Description','Link'])
        print('Combining phone: ' + phone.model)
        if first_run:
            master_df = df
            first_run = False
        else:
            master_df = pd.concat([master_df,df])
    
    master_df.to_csv("{}.csv".format(output),index=False)
    
    
        

    

def scrape_number_of_pages_from_search(start_url,number_of_paes_to_scrape):
    page_counter = 1
    current_url = start_url
    phones = []
    while page_counter <= number_of_paes_to_scrape:
        print(current_url)
        page = get_listing_page(current_url)
        page_phones = get_iphones_from_listing_page(page)
        phones = phones + page_phones
        page_counter += 1
        current_url = get_next_url_from_url(current_url,page_counter)
    return phones



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
        title_div = htmlScraper.get_div_by_class(listing,'title')
        link = htmlScraper.get_link(title_div)
        full_link = "https://kijiji.ca{}".format(link)
        description = htmlScraper.get_div_text_by_class(listing, 'description', contains_div = True)
        description = description.strip()
        listings.append(Listing(title,price,description,full_link))
    iphone_listings = [listing for listing in listings if is_iphone_listing(listing)]
    return iphone_listings       

def is_iphone_listing(listing):
    title = listing.title.lower()
    return ("iphone" in title
    or "i phone" in title)  #need to ignore caps 

def get_model_from_title(title):
    start = title.lower().find('iphone')
    if start == -1:
        start = title.lower().find("i phone")
    first_space = title.find(' ', start)
    second_space = title.find(' ', first_space + 1)
    model = title[start:first_space] if len(title[start:first_space]) > 6 else title[start:second_space]
    return model 

def get_iphone_from_listing(listing):
    model = get_model_from_title(listing.title)
    storage = get_storage_for_iphone(listing.description)
    return IPhone(model,storage,listing.price.strip(),listing.description,listing.link)

def get_iphones_from_listing_page(url):
    listings = get_listings_from_page(url)
    phones =  [get_iphone_from_listing(listing) for listing in listings]
    return phones

def get_storage_for_iphone(description):
    words = description.split()
    for i in range(len(words)):
        word = words[i].lower()
        if 'gb' in word:
            if word == 'gb':
                return words[i-1] + word
            return word
    return ' '

if __name__ == '__main__':
    main()
    