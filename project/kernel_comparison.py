import sys
import csv
from sklearn import preprocessing

import random

import numpy as np
from sklearn.svm import SVR

titles_data = []

movie_ids = []
with open("selected_movies.csv") as selected_movies_file:
	selected_movies_reader = csv.reader(selected_movies_file, delimiter='\t')
	for line in selected_movies_reader:
		movie_ids.append(int(line[0]))
movie_ids.sort()

actor_ids = []
with open("selected_actors.csv") as selected_actors_file:
	selected_actors_reader = csv.reader(selected_actors_file, delimiter='\t')
	for line in selected_actors_reader:
		actor_ids.append(int(line[0]))
actor_ids.sort()

director_ids = []
with open("selected_directors.csv") as selected_directors_file:
	selected_directors_reader = csv.reader(selected_directors_file, delimiter='\t')
	for line in selected_directors_reader:
		director_ids.append(int(line[0]))
director_ids.sort()

genres = []
with open("selected_genres.csv") as selected_genres_file:
	selected_genres_reader = csv.reader(selected_genres_file, delimiter='\t')
	for line in selected_genres_reader:
		genres.append(line[0])
genres.sort()

year_min = 2050
year_max = 1950
duration_min = 300
duration_max = 0
sum_year = 0.0
sum_duration = 0.0

with open("filtered_data.tsv") as filered_data_file:
	filered_data_reader = csv.reader(filered_data_file, delimiter='\t')
	for line in filered_data_reader:
		
		line[0] = int(line[0])
		line[2] = int(line[2])
		if year_min > line[2]:
			year_min = line[2]
		if year_max < line[2]:
			year_max = line[2]
		sum_year += line[2]
		line[3] = int(line[3])
		if duration_min > line[3]:
			duration_min = line[3]
		if duration_max < line[3]:
			duration_max = line[3]
		sum_duration += line[3]
		line[4] = line[4].split(',')
		actors_l = []
		for a in line[5][1 : -1].split(', '):
			if a != "":
				actors_l.append(int(a))
		line[5] = actors_l
		directors_l = []
		for d in line[6][1 : -1].split(', '):
			if d != "":
				directors_l.append(int(d))
		line[6] = directors_l
		
		line[7] = float(line[7])
		line[8] = int(line[8])
		
		if line[5] != [] and line [6] != []:
			titles_data.append(line)

titles_data.sort(key=lambda x: x[0])

print('\n')
print("Filtered titles data")
print("Size: {0: d}".format(len(titles_data)))
print("Sameple:")
for title in titles_data[0 : 5]:
	print(title)

print("\n")
print("Movies: {0: d}.".format(len(movie_ids)))
print("Actors: {0: d}.".format(len(actor_ids)))
print("Directors: {0: d}.".format(len(director_ids)))
print("Genres: {0: d}.".format(len(genres)))

nr_movies = len(movie_ids)
nr_actors = len(actor_ids)
nr_directors = len(director_ids)
nr_genres = len(genres)

average_year = sum_year / nr_movies
average_duration = sum_duration / nr_movies

print('\n')
print("Min and Max year: {0: d} {1: d}".format(year_min, year_max))
print("Average year: {0: .2f}.".format(average_year))
print("Min and Max duration: {0: d} {1: d}".format(duration_min, duration_max))
print("Average duration: {0: .2f}.".format(average_duration))

for title in titles_data:
	title[2] = (title[2] - average_year) / (year_max - year_min)
	title[3] = (title[3] - average_duration) / (80)

print('\n')
print("Filtered titles data with normalized and scaled features")
print("Size: {0: d}".format(len(titles_data)))
print("Sample:")
for title in titles_data[0 : 5]:
	print(title)

movie_id_mapping = preprocessing.LabelEncoder()
movie_id_mapping.fit(movie_ids)

actor_id_mapping = preprocessing.LabelEncoder()
actor_id_mapping.fit(actor_ids)

director_id_mapping = preprocessing.LabelEncoder()
director_id_mapping.fit(director_ids)

genre_id_mapping = preprocessing.LabelEncoder()
genre_id_mapping.fit(genres)


dataset_X = []
dataset_Y = []

random.shuffle(titles_data)

for title_data in titles_data:
	movie_line = []
	movie_line.append(title_data[2])
	movie_line.append(title_data[3])

	genres_vector = [0] * nr_genres
	genres_id_transformed = genre_id_mapping.transform(title_data[4])
	for g in genres_id_transformed:
		genres_vector[g] = 1
		
	actors_vector = [0] * nr_actors
	actors_id_transformed = actor_id_mapping.transform(title_data[5])
	for a in actors_id_transformed:
		actors_vector[a] = 1
		
	directors_vector = [0] * nr_directors
	directors_id_transformed = director_id_mapping.transform(title_data[6])
	for d in directors_id_transformed:
		directors_vector[d] = 1
		
	movie_line = [title_data[2], title_data[3]] + genres_vector + actors_vector + directors_vector
	
	dataset_X.append(movie_line)
	
	dataset_Y.append(title_data[7])

train_size = 8000
test_size = 2578

y_train_predict = []
y_test_predict = []
total_error = 0.0
index = 0
train_mean_error = 0.0
test_mean_error = 0.0

kernel_type_file = open("kernel_type", "w")

for kernel_type in ['linear', 'poly', 'rbf']:
	print("kernel type: " + kernel_type)
	kernel_type_file.write("kernel type: " + kernel_type + "\n")
	print("training")
	svr = SVR(kernel=kernel_type, C=1e3, max_iter=1000)
	svr.fit(dataset_X[0 : train_size], dataset_Y[0 : train_size])
	print("predicting")
	y_train_predict = svr.predict(dataset_X[0 : train_size])
	y_test_predict = svr.predict(dataset_X[train_size : train_size + test_size])
	total_error = 0
	index = 0
	while index < train_size:
		total_error += abs(y_train_predict[index] - dataset_Y[index])
		index += 1
	train_mean_error = total_error / train_size
	total_error = 0
	index = 0
	while index < test_size:
		total_error += abs(y_test_predict[index] - dataset_Y[index + train_size])
		index += 1
	test_mean_error = total_error / test_size
	total_error = 0
	index = 0

	print("train error: {0: .2f}".format(train_mean_error))
	print("test error: {0: .2f}\n".format(test_mean_error))	
	kernel_type_file.write("train error: {0: .2f}\n".format(train_mean_error))
	kernel_type_file.write("test error: {0: .2f}\n".format(test_mean_error))	
	
