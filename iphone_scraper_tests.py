import kijiji_iphone_scraper


def get_listing_page_test():
    url = "https://www.kijiji.ca/b-cell-phone/cape-breton/c760l1700011?ll=46.136790%2C-60.194224&address=Sydney%2C+NS&radius=50.0"
    listings = kijiji_iphone_scraper.get_listings_from_page(url)
    print(len(listings))

def get_iphones_test():
    url = "https://www.kijiji.ca/b-cell-phone/cape-breton/c760l1700011?ll=46.136790%2C-60.194224&address=Sydney%2C+NS&radius=50.0"
    listings = kijiji_iphone_scraper.get_listings_from_page(url)
    phones =  [kijiji_iphone_scraper.get_iphone_from_listing(listing) for listing in listings]
    print(phones[0])

def get_iphones_multiple_pages():
    url = "https://www.kijiji.ca/b-cell-phone/cape-breton/c760l1700011?ll=46.136790%2C-60.194224&address=Sydney%2C+NS&radius=50.0"
    phones = kijiji_iphone_scraper.scrape_number_of_pages_from_search(url, 5)
    print(len(phones))

get_iphones_multiple_pages()

