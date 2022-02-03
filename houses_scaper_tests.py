import kijiji_house_scraper as hs 

TEST_URL = "https://www.kijiji.ca/b-house-for-sale/st-johns/c35l1700113"
PAGE2 = "https://www.kijiji.ca/b-house-for-sale/st-johns/page-2/c35l1700113"
URL2 = "https://www.kijiji.ca/b-house-for-sale/st-johns/c35l1700113?ll=47.561510%2C-52.712577&address=St.+John%26%2327%3Bs%2C+NL&radius=50.0"

def get_listing_page_test():
    listings = hs.get_listings_from_page_url(TEST_URL)
    print(len(listings))

def get_listings_from_url_page_test():
    listings = hs.get_listings_from_page_url(TEST_URL)
    print(listings[0])

def get_house_from_listing_test():
    listings = hs.get_listings_from_page_url(TEST_URL)
    listing = listings[0]
    house = hs.get_house_from_listing(listing)
    print(house)

def get_houses_multiple_pages_test():
    houses = hs.scrape_number_of_pages_from_search(URL2,5)
    print(len(houses))

def get_homes_from_url_test():
    houses = hs.get_houses_from_url("https://www.kijiji.ca/b-maison-a-vendre/ville-de-montreal/c35l1700281")
    print(len(houses))
    print(houses[0])

def get_csv_from_file_test():
    hs.get_csv_from_file_links('houseforsalelinks.txt','housetest2')

def convert_price_to_int_test():
    price = "$130,000.00"
    price_int = hs.convert_price_to_int(price)
    print(price_int)

get_csv_from_file_test()
