import csv
import pdb

#process film
with open('./data/film.csv', 'w',newline='') as film, open('tns.csv', newline='') as tns:
	fieldnames = ['id', 'name', 'alter_name', 'copyright_year', 'description', 'duration', 'img']
	
	reader = csv.DictReader(tns)
	writer = csv.DictWriter(film, fieldnames=fieldnames)
	writer.writeheader()

	for line in reader:
		writer.writerow({ fieldname: line[fieldname] for fieldname in fieldnames})

#process link film
with open('./data/link_film.csv', 'w',newline='') as link_film, open('tns.csv', newline='') as tns:
	fieldnames = ['id_film', 'link', 'quality']
	qualities = ['high', 'low', 'medium']
	
	reader = csv.DictReader(tns)
	writer = csv.DictWriter(link_film, fieldnames=fieldnames)
	
	writer.writeheader()

	for line in reader:
		for quality in qualities:
			if len(line[quality]) != 0:
				writer.writerow({'id_film': line['id'], 'link': line[quality], 'quality': quality})


#process genres
genres = set()

with open('tns.csv', newline='') as f:
	reader = csv.DictReader(f)
	for line in reader:
		for genre in line['genre'].split(','):
			genres.add(genre)

genres.remove('')
genres = list(genres)
genres_dict = dict()

for i in range(len(genres)):
	genres_dict[genres[i]] = i + 1
	
with open('./data/genres.csv', 'w', newline='') as csvfile:
	fieldnames = ['id', 'genre_name']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for genre, idx in genres_dict.items():
		writer.writerow({'id': idx, 'genre_name': genre})

with open('./data/film_genre.csv', 'w',newline='') as film_genre, open('tns.csv', newline='') as tns:
	fieldnames = ['id_film', 'id_genre']
	
	reader = csv.DictReader(tns)
	writer = csv.DictWriter(film_genre, fieldnames=fieldnames)
	writer.writeheader()

	for line in reader:
		for genre in line['genre'].split(','):
			if genre != '':
				writer.writerow({'id_film': line['id'], 'id_genre': genres_dict[genre]})

#process origin
origins = set()

with open('tns.csv', newline='') as f:
	reader = csv.DictReader(f)
	for line in reader:
		for origin in line['origin'].split(','):
			origins.add(origin)

origins.remove('')
origins = list(origins)
origins_dict = dict()

for i in range(len(origins)):
	origins_dict[origins[i]] = i + 1
	
with open('./data/origins.csv', 'w', newline='') as csvfile:
	fieldnames = ['id', 'origin_name']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for origin, idx in origins_dict.items():
		writer.writerow({'id': idx, 'origin_name': origin})

with open('./data/film_origin.csv', 'w', newline='') as film_origin, open('tns.csv', newline='') as tns:
	fieldnames = ['id_film', 'id_origin']
	
	reader = csv.DictReader(tns)
	writer = csv.DictWriter(film_origin, fieldnames=fieldnames)
	writer.writeheader()

	for line in reader:
		for origin in line['origin'].split(','):
			if origin != '':
				writer.writerow({'id_film': line['id'], 'id_origin': origins_dict[origin]})

#sumary
film_idx = set()

with open('./data/link_film.csv', newline='') as link_film:
	reader = csv.DictReader(link_film)
	for line in reader:
		film_idx.add(line['id_film'])

print(len(film_idx))
