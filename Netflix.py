#!/usr/bin/env python3

# -------
# imports
# -------

from math import sqrt
import pickle
from requests import get
from os import path
from numpy import sqrt, square, mean, subtract
import operator
import functools


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
        file = get(webAddress).content
        cache = pickle.load(file)

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
# YEAR_OF_RATING = create_cache("cache-yearCustomerRatedMovie.pickle")

# (cID, mID): rt
ACTUAL_CUSTOMER_RATING = create_cache("cache-actualCustomerRating.pickle")

# mID : yr
MOVIE_RELEASE_YEAR = create_cache("yz8896-movie_year_cache.pickle")

# ------------
# netflix_eval
# ------------

# Toughts
# 1. weighting: time & cunstomer record number
# if the customer has previously commented the movie, we will use that rating combined with customer average rating of that year and moive rating of that year
# cache used (cID, mID): yr, (cID, yr): rt and (mID, yr): rt
# if the customer has not commented that movie before, we will use the average rating of that customer, average rating of that movie
# cache used (cID): rt, (mID): rt

def netflix_eval(reader, writer):
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
            assert 1<=mID<=17770
            assert isinstance(mID,int)
            writer.write(line)
            writer.write('\n')
        else:
        # It's a customer
            cID = int(line)
            assert 1<=cID<=2649429
            assert isinstance(cID,int)

            customer_rating = AVERAGE_CUSTOMER_RATING[cID]
            movie_rating = AVERAGE_MOVIE_RATING[mID]

            yr = MOVIE_RELEASE_YEAR[mID]

            movie_rating_year_sum = []
            customer_rating_year_sum = []


            # for i in range(1):
            #     if (mID,2005 - i) in AVERAGE_MOVIE_RATING_PER_YEAR:
            #         movie_rating_year_sum += [AVERAGE_MOVIE_RATING_PER_YEAR[(mID,2005 - i)]]

            # if len(movie_rating_year_sum) == 0:
            #     avg_movie_rating = movie_rating
            # else:
            #     avg_movie_rating = sum(movie_rating_year_sum)/len(movie_rating_year_sum)

            i = 0
            while (len(movie_rating_year_sum) <= 0) and (i <= 8):
                if (mID,2005 - i) in AVERAGE_MOVIE_RATING_PER_YEAR:
                    movie_rating_year_sum += [AVERAGE_MOVIE_RATING_PER_YEAR[(mID,2005 - i)]]
                i += 1
            avg_movie_rating = sum(movie_rating_year_sum)/len(movie_rating_year_sum)
                

            # for j in range(2005,2006):
            #     if (cID,j) in AVERAGE_CUSTOMER_RATING_PER_YEAR:
            #         customer_rating_year_sum += [AVERAGE_CUSTOMER_RATING_PER_YEAR[(cID,j)]]

            # if len(customer_rating_year_sum) == 0:
            #     avg_customer_rating = customer_rating
            # else:
            #     avg_customer_rating = sum(customer_rating_year_sum)/len(customer_rating_year_sum)

            j = 0
            while (len(customer_rating_year_sum) <= 0) and (j <= 8):
                if (cID,2005 - j) in AVERAGE_CUSTOMER_RATING_PER_YEAR:
                    customer_rating_year_sum += [AVERAGE_CUSTOMER_RATING_PER_YEAR[(cID,2005 - j)]] 
                j += 1  
            avg_customer_rating = sum(customer_rating_year_sum)/len(customer_rating_year_sum)           
               
            #pred = min(round((avg_customer_rating**0.6 * avg_movie_rating**0.4),1),5.0)
            pred = min(round((avg_customer_rating*5.5 + avg_movie_rating*4.5)/10,1),5.0)
            assert 1<=pred<=5

            predictions.append(pred)
            actual.append(ACTUAL_CUSTOMER_RATING[(cID,mID)])
            writer.write(str(pred))
            writer.write('\n')

    # calculate rmse for predications and actuals
    # TODO: format: need to 2 decimal places
    rmse = sqrt(mean(square(subtract(predictions, actual))))
    print('rmse:',rmse)
    assert rmse >0

    writer.write(str(rmse)[:4] + '\n')
