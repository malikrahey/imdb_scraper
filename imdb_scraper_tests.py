import imdb_scraper, htmlScraper

movie_link = "https://www.imdb.com/title/tt1596363/?ref_=nv_sr_srsg_0"
movie_list_page_link = "https://www.imdb.com/chart/moviemeter?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=PJJVGKTEED6EY2FXXKRB&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=topenglish&ref_=chttentp_ql_2"
movie_page = htmlScraper.scrape_page(movie_link)
movie_list_page = htmlScraper.scrape_page(movie_list_page_link)

def get_box_office_test():
    budget = imdb_scraper.get_box_office(movie_page)
    print(budget)

def get_movie_title_test():
    title = imdb_scraper.get_movie_title(movie_page)
    print(title)

def get_movie_from_page_test():
    movie = imdb_scraper.get_movie_from_page(movie_page)
    print(movie)

def get_movie_from_url_test():
    movie = imdb_scraper.get_movie(movie_link)
    print(movie)

def get_movie_url_test():
    print('url')

def get_movie_img_src_test():
    src = imdb_scraper.get_movie_poster_src(movie_page)
    print(src)

def get_movie_list_items_from_list_page_test():
    items = imdb_scraper.get_movie_list_page_items(movie_list_page)
    print(len(items))

def get_movie_urls_from_list_page_test():
    items = imdb_scraper.get_movie_list_page_items(movie_list_page)
    filtered_items = imdb_scraper.filter_movie_list_items(items)
    links = imdb_scraper.get_movie_list_items_links(filtered_items)
    print(len(links))

def get_movie_rating_test():
    rating = imdb_scraper.get_movie_rating(movie_page)
    print(rating)


get_movie_rating_test()