# Crawl_tam_nhin_so.info
This repo contains Scrapy project to crawl 1-epsisode film from tamnhinso.info

Installation
- python
- scrapy
- docker
- splash

How to run: 
- sudo docker run -p 8050:8050 scrapinghub/splash --max-timeout 3600
- scrapy crawl tns -o tns.csv
- python handle_data.py

Usage: 
- All data crawled will be saved to tns.csv
- Run handle_data to process data
- Each film has the following attributes (id, name, alter_name, img, copyright_year, description, img) in film.csv
- Each film contains several link in link_film.csv(id_film, link, quality) (Foreign key: id_film)
- Each film has many origins, each origins contains many films(film_origin.csv(id_film(FK), id_origin(FK)))
- Each film has many genres, each genres contains many films(film_genre.csv)
- Origin(id, name)
- Genre(id, name)

Still need to refactor :))))
