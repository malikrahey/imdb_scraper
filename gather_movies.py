import imdb_scraper

links = ["https://www.imdb.com/chart/moviemeter?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=7QB9366JRY71EJARBQT5&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=moviemeter&ref_=chtmvm_ql_2",
"https://www.imdb.com/chart/top?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=6HJG53TA8ZTF9ARB7P9T&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=moviemeter&ref_=chtmvm_ql_3",
"https://www.imdb.com/chart/top-english-movies?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=T39S0KCQMTBJPW15FJAN&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_ql_4",
"https://www.imdb.com/chart/bottom?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=NJN70E3E2AFDJNH7JX0A&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=topenglish&ref_=chttentp_ql_8"
]

detail_links =["https://www.imdb.com/search/title/?genres=action&sort=boxoffice_gross_us,desc&explore=title_type,genres&ref_=adv_prv",
"https://www.imdb.com/search/title/?genres=action&sort=boxoffice_gross_us,desc&start=51&explore=title_type,genres&ref_=adv_nxt",
"https://www.imdb.com/search/title/?genres=action,comedy,fantasy&sort=boxoffice_gross_us,desc&explore=title_type,genres",
"https://www.imdb.com/search/title/?genres=action,comedy&sort=boxoffice_gross_us,desc&explore=title_type,genres",
]

list_links = ["https://www.imdb.com/search/title/?genres=action,comedy&sort=boxoffice_gross_us,desc&start=51&explore=title_type,genres&ref_=adv_nxt",
"https://www.imdb.com/search/title/?genres=action,comedy&sort=boxoffice_gross_us,desc&start=51&explore=title_type,genres&ref_=adv_nxt",
"https://www.imdb.com/search/title/?genres=action,comedy,fantasy&sort=boxoffice_gross_us,desc&start=51&explore=title_type,genres&ref_=adv_nxt",
"https://www.imdb.com/search/title/?genres=action,comedy,fantasy,animation&sort=boxoffice_gross_us,asc&start=51&explore=title_type,genres&ref_=adv_nxt",
"https://www.imdb.com/search/title/?genres=action,comedy,fantasy,animation,family&sort=boxoffice_gross_us,asc&start=51&explore=title_type,genres&ref_=adv_nxt"
]

total_movies = []
for link in links:
    link_movies = imdb_scraper.get_movies_from_list_page_url(link)
    total_movies = total_movies + link_movies

for link in detail_links:
    link_movies = imdb_scraper.get_movies_from_compact_list_page(link)
    total_movies = total_movies + link_movies

for link in list_links:
    link_movies = imdb_scraper.get_movies_from_detailed_list_pages_increasing_offset(link, 1000)
    total_movies = total_movies + link_movies

movies = []
for movie in total_movies:
    if movie.name not in [mv.name for mv in movies]:
        movies.append(movie)
    else:
        print("duplicate movie " + movie.name)



with open("moviesv2-1.json","w") as f:
    f.write('{\n"movies": [')
    for movie in movies:
        f.write(movie.to_json())
        f.write(",\n")
    f.write("]\n}")


