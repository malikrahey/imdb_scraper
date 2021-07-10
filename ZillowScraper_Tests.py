import ZillowScraper, htmlScraper

def get_listing_page_test():
    listing_url = "https://www.zillow.com/homedetails/31118-Broad-Beach-Rd-Malibu-CA-90265/20557699_zpid/?"
    listing_page = htmlScraper.scrape_page(listing_url)
    print(listing_page)

def get_price_test():
    listing_url = "https://www.zillow.com/homedetails/31118-Broad-Beach-Rd-Malibu-CA-90265/20557699_zpid/?"
    listing_page = htmlScraper.scrape_page(listing_url)
    price = ZillowScraper.get_listing_price(listing_page)
    print(price)
