import sys
import csv

csv.field_size_limit(sys.maxsize)

'''
ACTORS AND DIRECTORS
'''

'''
actors_data = []
directors_data = []

with open("name.basics.tsv") as people_tsvfile:
	people_tsvreader = csv.reader(people_tsvfile, delimiter="\t")
	next(people_tsvreader, None)
	for line in people_tsvreader:
		if (line[4].find("actor") == 0
		or line[4].find("actress") == 0):
			actors_data.append([line[0], line[1]])
		if line[4].find("director") == 0:
			directors_data.append([line[0], line[1]])

print("Actors data")
print("Size: {0: d}".format(len(actors_data)))
print("Sample:")
for l in actors_data[0:5]:
	print(l)
print("\n")

print("Directors data")
print("Size: {0: d}".format(len(directors_data)))
print("Sample:")
for l in directors_data[0:5]:
	print(l)
print("\n")
'''

'''
TITLE BASIC DATA
'''

basics_data = []

with open("title.basics.tsv") as basics_tsvfile:
	basics_tsvreader = csv.reader(basics_tsvfile, delimiter="\t")
	next(basics_tsvreader, None)
	for line in basics_tsvreader:
		if (line[1] == 'movie' and (line[2] == line[3]) and line[4] == '0' and line[5] != '\N' and line[7] != '\N'):
			line[5] = int(line[5])
			line[7] = int(line[7])
			if line[5] > 2005:
				basics_data.append([int(line[0][2:]), int(line[5]), int(line[7]), line[8]])
			
print("Basics data")  
print("Size: {0: d}".format(len(basics_data)))
print("Sample:")
for l in basics_data[0:5]:
	print(l)
print("\n")

selected_titles = set()
for basics_data_item in basics_data:
	selected_titles.add(basics_data_item[0])

'''
TITLE CAST
'''

cast_data = []

with open("title.principals.tsv") as cast_tsvfile:
	cast_tsvreader = csv.reader(cast_tsvfile, delimiter="\t")
	next(cast_tsvreader, None)
	for line in cast_tsvreader:
		if int(line[0][2:]) in selected_titles:
			if (line[3] == "actor" or line[3] == "actress"):
				cast_data.append([int(line[0][2:]), int(line[2][2:])])
			
print("Cast data")  
print("Size: {0: d}".format(len(cast_data)))
print("Sample:")
for l in cast_data[0:5]:
	print(l)
print("\n")


'''
TITLE DIRECTORS AND WRITERS
'''

crew_data = []

with open("title.crew.tsv") as crew_tsvfile:
	crew_tsvreader = csv.reader(crew_tsvfile, delimiter="\t")
	next(crew_tsvreader, None)
	for line in crew_tsvreader:
		if line[1] == '\N':
			line[1] = ''
		crew_data.append([int(line[0][2:]), line[1]])
			
print("Crew data")  
print("Size: {0: d}".format(len(crew_data)))
print("Sample:")
for l in crew_data[0:5]:
	print(l)
print("\n")

rating_data = []

'''
TITLE RATING
'''

with open("title.ratings.tsv") as rating_tsvfile:
    rating_tsvreader = csv.reader(rating_tsvfile, delimiter="\t")
    next(rating_tsvreader, None)
    for line in rating_tsvreader:
        rating_data.append([int(line[0][2:]), float(line[1]), int(line[2])])
      
print("Rating data")  
print("Size: {0: d}".format(len(rating_data)))
print("Sample:")
for l in rating_data[0:5]:
	print(l)
print("\n")
