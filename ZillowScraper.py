import htmlScraper

def get_listing_price(listing_page):
    price = None
    home_details = htmlScraper.get_div_by_class(listing_page,"ds-home-details-chip")
    print(listing_page)
    spans = htmlScraper.get_sections_in_div(home_details)

    for span in spans:
        print(span)
        span_text = htmlScraper.get_div_text(span,"span")
        if '$' in span_text:
            price = span_text
    return price
