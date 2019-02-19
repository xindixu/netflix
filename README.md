# cs329e-netflix
This document provides the description of the pre-built caches to help with your project.

You can use any (or none if you want to make your own).

The purpose of the caches is to make it easier to access the data you need without having to read all the project's files (because they're rather large).

The idea is similar to if you're trying to pick a new car. You could spend some time and research every review ever made of a new car. However, that would probably take a very long time because there are so many reviews. Instead, what if you aggregated all the reviews and just looked at the average review. You'd save time by not having to read all the reviews and you'd get the information you need. You could then use this information to decide if you should buy the car.

Now, instead of aggregating car reviews for yourself, you're aggregating movie reviews and you're using these aggregations to predict a user's rating.

# Available caches
cache-averageMovieRating.pickle

This is a dictionary with movie_id as keys (int) and average movie rating as values (float) .


cache-averageCustomerRating.pickle

This is a dictionary with customer_id (int) as keys (int) and their average rating as values (float).


cache-actualCustomerRating.pickle

This is a dictionary of (customer_id, movie_id) as keys (int, int) and their actual rating as values (int).


cache-customerAverageRatingByYear.pickle

This is a cache of (customerId, year) as keys (int, int) and then a float of their average rating for the year as the value (float).


cache-movieAverageByYear.pickle

This is a cache of (movieId, year) as keys (int, int) and it's average rating for that year as values (float).


cache-yearCustomerRatedMovie.pickle

This is a cache of (customerId, movieId ) as keys (int, int) and the year the movie was rated by that customer as a value (int).

Note:
Values are rounded to 3 decimal places.
Also, the actualCustomerRating cache contains only data corresponding to probe data

# Variables used:

cID: customerID, type: int

mID: movieID, type: int

yr: year, type: int

rt: rating, type: int/float



cache-actualCustomerRating.pickle

a dictionary of elements below:

(cID, mID): rt

# mID rated cID as rt.


cache-averageCustomerRating.pickle

a dictionary of elements below:

cID: rt

# The avg rating of cID is rt.

cache-averageMovieRating.pickle

a dictionary of elements below:

mID: rt

# The avg rating of mID is rt

cache-customerAverageRatingByYear.pickle

a dictionary of elements below:

(cID, yr): rt

# The avg rating of cID in year yr is rt.

cache-movieAverageByYear.pickle

a dictionary of elements below:

(mID, yr): rt

# The avg rating of mID in year yr is rt.

cache-yearCustomerRatedMovie.pickle

a dictionary of elements below:

(cID, mID): yr

# cID rated mID in year yr.

