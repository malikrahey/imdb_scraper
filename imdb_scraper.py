from time import sleep
import htmlScraper
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class BoxOffice:
    budget: int
    opening_weekend: int
    gross_usa: int
    gross_world: int

@dataclass_json
@dataclass
class Movie:
    name: str
    poster_url: str
    rating: float
    box_office: BoxOffice


def get_movies_from_detailed_list_pages_increasing_offset(list_page_url, end, offset=50):
    start_index = list_page_url.find('start=') + 6
    end_index = list_page_url.find('&',start_index)
    begin = int(list_page_url[start_index:end_index])
    offset = begin
    movies = []
    while offset < end:
        print("Current offset: " + str(offset))
        start_index = list_page_url.find('start=') + 6
        end_index = list_page_url.find('&',start_index)
        list_page_url = list_page_url[:start_index] + str(offset) + list_page_url[end_index:]
        print(list_page_url)
        page_movies = get_movies_from_compact_list_page(list_page_url)
        movies = movies + page_movies
        offset = offset + 50
    return movies

def get_movies_from_list_page_url(list_page_url):
    movies = []
    list_page = htmlScraper.scrape_page(list_page_url)
    list_items = get_movie_list_page_items(list_page)
    filtered_list_items = filter_movie_list_items(list_items)
    print(len(filtered_list_items))
    for item in filtered_list_items:
        url = get_movie_url_from_list_page_item(item)
        movie_page = htmlScraper.scrape_page(url)
        movie = get_movie_from_page(movie_page)
        movies.append(movie)
    return movies

def get_movies_from_compact_list_page(list_page_url):
    movies = []
    list_page = htmlScraper.scrape_page(list_page_url)
    list_items = get_compact_list_page_items(list_page)
    print(len(list_items))
    for item in list_items:
        url = get_movie_url_from_compact_list_item(item)
        movie_page = htmlScraper.scrape_page(url)
        movie = get_movie_from_page(movie_page)
        movies.append(movie)
    return movies

def get_movie(movie_url):
    movie_page = htmlScraper.scrape_page(movie_url)
    return get_movie_from_page(movie_page)

def get_movie_list_page_items(list_page):
    list_div = htmlScraper.get_div_by_class(list_page,'lister-list','tbody')
    list_items = htmlScraper.get_sections_in_div(list_div,'tr')
    return list_items

def get_compact_list_page_items(list_page):
   list_items = htmlScraper.get_all_divs_by_class(list_page,'lister-item mode-advanced')
   return list_items

def get_compact_movie_list_item_links(list_items):
    links = [get_movie_url_from_compact_list_item(link) for link in list_items]
    return links

def get_movie_url_from_compact_list_item(list_item):
    header = htmlScraper.get_div_by_class(list_item,'lister-item-header','h3')
    route = htmlScraper.get_link(header)
    url = "https://www.imdb.com{}".format(route)
    return url

def filter_movie_list_items(list_items):
    filtered_list_items = [item for item in list_items if not list_item_rating_is_empty(item)]
    return filtered_list_items

def get_movie_list_items_links(list_items):
    links = [get_movie_url_from_list_page_item(link) for link in list_items]
    return links

def list_item_rating_is_empty(list_item):
    rating_div = htmlScraper.get_div_by_class(list_item,'ratingColumn imdbRating','td')
    return not 'based on' in rating_div

def list_item_has_box_office(list_item):
    url = get_movie_url_from_list_page_item(list_item)
    movie_page = htmlScraper.scrape_page(url)
    return "Box Office" in movie_page

def get_movie_url_from_list_page_item(list_page_item):
    link_route = htmlScraper.get_link(list_page_item)
    movie_url = "https://www.imdb.com{}".format(link_route)
    return movie_url

def get_movie_from_page(movie_page):
    title = get_movie_title(movie_page)
    poster_url = get_movie_poster_src(movie_page)
    box_office = get_box_office(movie_page)
    rating = get_movie_rating(movie_page)
    movie = Movie(title,poster_url,rating, box_office)
    return movie

def get_movie_title(movie_page):
    title_div = htmlScraper.get_div_by_class(movie_page,"title_wrapper")
    header_index = title_div.find('<h1') + 13
    end_title_index = title_div.find('<',header_index)
    title = title_div[header_index:end_title_index]
    title = title.strip()
    return title


def get_box_office(movie_page):
    box_office_index = movie_page.find('<h3 class="subheading">Box Office')
    movie_page = movie_page[box_office_index:]
    text_boxes = htmlScraper.get_all_divs_by_class(movie_page,'txt-block')

    if len(text_boxes) == 0:
        return BoxOffice(0,0,0,0)

    budget_int = 0
    opening_weekend_us_int = 0
    gross_us_int = 0
    gross_world_int = 0

    try:
        budget = get_box_office_budget(text_boxes[0])
        budget_int = get_dollar_amount_as_int(budget)

        opening_weekend_us = get_dollar_amount_from_text_box(text_boxes[1])
        opening_weekend_us_int = get_dollar_amount_as_int(opening_weekend_us)

        gross_us = get_dollar_amount_from_text_box(text_boxes[2])
        gross_us_int = get_dollar_amount_as_int(gross_us)

        gross_world = get_dollar_amount_from_text_box(text_boxes[3])
        gross_world_int = get_dollar_amount_as_int(gross_world)
    except IndexError:
        print("Index error")
    finally:
        box_office = BoxOffice(budget_int,opening_weekend_us_int,gross_us_int,gross_world_int)
        return box_office


    
    
def get_box_office_budget(text_box):
    dollar_index = text_box.find('$')
    end_dollar_index = text_box.find('<',dollar_index)
    budget = text_box[dollar_index:end_dollar_index]
    budget = budget.strip()
    return budget
        

def get_dollar_amount_from_text_box(text_box):
    dollar_index = text_box.find('$')
    end_dollar_index = text_box.find('\n',dollar_index)
    budget = text_box[dollar_index:end_dollar_index]
    budget = budget.strip()
    return budget


def get_dollar_amount_as_int(amount):
    if amount == '':
        return 0
    amount = amount[1:]
    amount = amount.replace(',','')
    return int(amount)

def get_movie_poster_src(movie_page):
    poster_div = htmlScraper.get_div_by_class(movie_page,'poster')
    src = htmlScraper.get_img_src(poster_div)
    return src

def get_movie_rating(movie_page, recur_count = 0):
    rating_str = htmlScraper.get_div_text_by_class(movie_page,'AggregateRatingButton__RatingScore-sc-1il8omz-1 fhMjqK','span')
    if(rating_str == ''):
        print("rating string error")
        if recur_count < 5:
            sleep(1)
            return get_movie_rating(movie_page, recur_count + 1)
        else:
            return 0
    rating = float(rating_str)
    return rating