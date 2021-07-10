import imdb_scraper


list_link = "https://www.imdb.com/search/title/?genres=action,comedy&sort=boxoffice_gross_us,desc&start=101&explore=title_type,genres&ref_=adv_nxt"

movies = imdb_scraper.get_movies_from_detailed_list_pages_increasing_offset(list_link, 1000)

for movie in movies:
    if movie.poster_url == "":
        movies.remove(movie)
    elif movie.name in [mv.name for mv in movies]:
        movies.remove(movie)


with open("movies3.json","w") as f:
    f.write('{\n"movies": [')
    for movie in movies:
        f.write(movie.to_json())
        f.write(",\n")
    f.write("]\n}")
