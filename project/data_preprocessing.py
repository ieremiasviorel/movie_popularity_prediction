import sys
import csv
import gc

csv.field_size_limit(sys.maxsize)

'''
TITLE BASIC DATA
'''

titles_data = {}
genres = set()

with open("title.basics.tsv") as basics_tsvfile:
	basics_tsvreader = csv.reader(basics_tsvfile, delimiter="\t")
	next(basics_tsvreader, None)
	for line in basics_tsvreader:
		# selection criterias:
		#	- movie (not short, documentary, etc.)
		#	- of American or English production
		#	- is produced after 1980
		#	- has a duration of at least 60 minutes and maximum 210 minutes
		if (line[1] == 'movie' and (line[2] == line[3]) and line[4] == '0' and line[5] != '\N' and line[7] != '\N' and line[8] != '\N'):
			line[5] = int(line[5])
			line[7] = int(line[7])
			if line[5] > 1998 and line[7] > 59 and line [7] < 211:
				titles_data[int(line[0][2:])] = [line[2], int(line[5]), int(line[7]), line[8], [], [], 0, 0]
			genre_list = line[8].split(',')
			for genre in genre_list:
				genres.add(genre)

selected_titles = set()
for k, v in titles_data.items():
	selected_titles.add(k)

'''
TITLE RATING
'''

selected_titles_filtered = set()

with open("title.ratings.tsv") as rating_tsvfile:
    rating_tsvreader = csv.reader(rating_tsvfile, delimiter="\t")
    next(rating_tsvreader, None)
    for line in rating_tsvreader:
    	if int(line[0][2:]) in selected_titles and int(line[2]) > 999:
			titles_data[int(line[0][2:])][6] = float(line[1])
			titles_data[int(line[0][2:])][7] = int(line[2])
			selected_titles_filtered.add(int(line[0][2:]))

for k,v in titles_data.items():
	if v[7] == 0:
		del titles_data[k]

'''
TITLE CAST
'''

with open("title.principals.tsv") as cast_tsvfile:
	cast_tsvreader = csv.reader(cast_tsvfile, delimiter="\t")
	next(cast_tsvreader, None)
	for line in cast_tsvreader:
		if int(line[0][2:]) in selected_titles_filtered:
			if (line[3].find("actor") > -1 or line[3].find("actress") > -1):
				titles_data[int(line[0][2:])][4].append(int(line[2][2:]))
			if (line[3].find("director") > -1):
				titles_data[int(line[0][2:])][5].append(int(line[2][2:]))
				
for k,v in titles_data.items():
	if v[4] == [] or v[5] == []:
		del titles_data[k]
		selected_titles_filtered.discard(k)
				
print("Titles data: {0: d}".format(len(titles_data)))
print("Initial nr.: {0: d}".format(len(selected_titles)))
print("Filtered nr.: {0: d}\n".format(len(selected_titles_filtered)))

				
selected_actors = set()
for k, v in titles_data.items():
	actors_list = v[4]
	for actor in actors_list:
		selected_actors.add(actor)
print("Nr. dist actors {0: d}\n".format(len(selected_actors)))

selected_directors = set()
for k, v in titles_data.items():
	directors_list = v[5]
	for director in directors_list:
		selected_directors.add(director)
print("Nr. dist directors {0: d}\n".format(len(selected_directors)))

print("Nr. dist genres {0: d}\n".format(len(genres)))

with open('filtered_data.tsv', 'w') as tsvfile:
	writer = csv.writer(tsvfile, delimiter='\t')
	for k, v in titles_data.items():
		writer.writerow([k] + v)

with open('selected_movies.csv', 'w') as csvfile:
    for movie in selected_titles_filtered:
 		csvfile.write(str(movie) + '\n')

with open('selected_actors.csv', 'w') as csvfile:
    for actor in selected_actors:
 		csvfile.write(str(actor) + '\n')
 		
with open('selected_directors.csv', 'w') as csvfile:
    for director in selected_directors:
 		csvfile.write(str(director) + '\n')
 		
with open('selected_genres.csv', 'w') as csvfile:
    for genre in genres:
 		csvfile.write(genre + '\n')

'''
TITLE CAST AND DIRECTORS
'''

'''
actors_data = {}
directors_data = {}

with open("name.basics.tsv") as people_tsvfile:
	people_tsvreader = csv.reader(people_tsvfile, delimiter="\t")
	next(people_tsvreader, None)
	for line in people_tsvreader:
		if (line[4].find("actor") != -1 or line[4].find("actress") != -1):
			if int(line[0][2:]) in selected_actors:
				actors_data[int(line[0][2:])] = line[1]
		if line[4].find("director") != -1:
			if int(line[0][2:]) in selected_directors:
				directors_data[int(line[0][2:])] = line[1]
				
movie_name = "The Shawshank Redemption"
for k, v in titles_data.items():
	if v[0] == movie_name:
		movie_id = k
		data_line = v
print("################\n");
print(data_line[0])
print(data_line[1])
print(data_line[2])
print(data_line[3])
for actor_id in data_line[4]:
	print(actors_data[actor_id])
for director_id in data_line[5]:
	print(directors_data[director_id])
print(data_line[6])
print(data_line[7])
print("\n################\n");
'''

