#!/usr/bin/env python3

# -------
# imports
# -------

from math import sqrt
import pickle
from requests import get
from os import path
from numpy import sqrt, square, mean, subtract


def create_cache(filename):
    """
    filename is the name of the cache file to load
    returns a dictionary after loading the file or pulling the file from the public_html page
    """
    cache = {}
    filePath = "/u/fares/public_html/netflix-caches/" + filename

    if path.isfile(filePath):
        with open(filePath, "rb") as f:
            cache = pickle.load(f)
    else:
        webAddress = "http://www.cs.utexas.edu/users/fares/netflix-caches/" + \
            filename
        bytes = get(webAddress).content
        cache = pickle.loads(bytes)

    return cache


AVERAGE_RATING = 3.60428996442


ACTUAL_CUSTOMER_RATING = create_cache("cache-actualCustomerRating.pickle")

# cID: rt
AVERAGE_CUSTOMER_RATING = create_cache("cache-averageCustomerRating.pickle")

# mID: rt
AVERAGE_MOVIE_RATING = create_cache("cache-averageMovieRating.pickle")

# (cID, yr): rt
AVERAGE_CUSTOMER_RATING_PER_YEAR = create_cache("cache-customerAverageRatingByYear.pickle")

# (mID, yr): rt
AVERAGE_MOVIE_RATING_PER_YEAR = create_cache("cache-movieAverageByYear.pickle")

# (cID, mID): yr
YEAR_OF_RATING = create_cache("cache-yearCustomerRatedMovie.pickle")

# (cID, mID): rt
ACTUAL_CUSTOMER_RATING = create_cache("cache-actualCustomerRating.pickle")

actual_scores_cache = {10040: {2417853: 1, 1207062: 2, 2487973: 3}}
movie_year_cache = {10040: 1990}
decade_avg_cache = {1990: 2.4}

# ------------
# netflix_eval
# ------------

# Toughts
# 1. weighting: time & cunstomer record number
# if the customer has previously commented the movie, we will use that rating combined with customer average rating of that year and moive rating of that year
# cache used (cID, mID): yr, (cID, yr): rt and (mID, yr): rt
# if the customer has not commented that movie before, we will use the average rating of that customer, average rating of that movie
# cache used (cID): rt, (mID): rt

def netflix_eval(reader, writer) :
    predictions = []
    actual = []
    mID = 0
    # iterate throught the file reader line by line
    for line in reader:
    # need to get rid of the '\n' by the end of the line
        line = line.strip()
        # check if the line ends with a ":", i.e., it's a movie title
        if line[-1] == ':':
		# It's a movie
            mID = int(line.rstrip(':'))
            avg_movie_rating = AVERAGE_MOVIE_RATING[mID]
            writer.write(line)
            writer.write('\n')
        else:
		# It's a customer
            cID = int(line)
            if mID in YEAR_OF_RATING[cID]:
                yr = YEAR_OF_RATING[cID][mID]
                movie_rating = AVERAGE_MOVIE_RATING_PER_YEAR[mID][yr]
                customer_rating = AVERAGE_CUSTOMER_RATING_PER_YEAR[cID][yr]
                # movie_customer_rating = ACTUAL_CUSTOMER_RATING[cID][mID]

                pred = (movie_rating + customer_rating)/2
                predictions.append(prediction)

            predictions.append(prediction)
            actual.append(ACTUAL_CUSTOMER_RATING[mID][cID])
            writer.write(str(prediction))
            writer.write('\n')

    # calculate rmse for predications and actuals
    # TODO: format: need to 2 decimal places
    rmse = sqrt(mean(square(subtract(predictions, actual))))
    writer.write(str(rmse)[:4] + '\n')
