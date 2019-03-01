#!/usr/bin/env python3


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

# (cID, yr): rt
AVERAGE_CUSTOMER_RATING_PER_YEAR = create_cache(
    "cache-customerAverageRatingByYear.pickle")

# (mID, yr): rt
AVERAGE_MOVIE_RATING_PER_YEAR = create_cache("cache-movieAverageByYear.pickle")

# (cID, mID): rt
ACTUAL_CUSTOMER_RATING = create_cache("cache-actualCustomerRating.pickle")

# mID : yr
# MOVIE_RELEASE_YEAR = create_cache("yz8896-movie_year_cache.pickle")

# ------------
# netflix_eval
# ------------


def netflix_eval(reader, writer):
    """
    1. read the file line by line
    2. if the line indicates a movie (ends with ':')
        2.1 save the mID and validate it

        2.2 get most recent year average rating from AVERAGE_CUSTOMER_RATING_PER_YEAR:

        2.3 write mID to the output file

    3. if the line indicates a customer (ends with nothing)
        3.1 save the cID and validate it

        3.2 get most recent year average rating from AVERAGE_CUSTOMER_RATING_PER_YEAR:

        3.3 make predictions with:
            pred = min(round((avg_customer_rating*5.5 + avg_movie_rating*4.5)/10,1),5.0)

        3.4 add prediction and actual score in arrays
        3.5 write predicted customer rating in file

    4. calculate RMSE with predictions[], actuals[]
    """
    predictions = []
    actual = []

    # iterate throught the file reader line by line
    for line in reader:
        # need to get rid of the '\n' by the end of the line
        line = line.strip()
        # check if the line ends with a ":", i.e., it's a movie title

        if line[-1] == ':':
                # It's a movie
            mID = int(line.rstrip(':'))
            assert 1 <= mID <= 17770
            assert isinstance(mID, int)
            movie_rating_year_sum = []

            # most recent year average rating

            i = 0
            while (len(movie_rating_year_sum) <= 0) and (i <= 8):
                if (mID, 2005 - i) in AVERAGE_MOVIE_RATING_PER_YEAR:
                    movie_rating_year_sum += [
                        AVERAGE_MOVIE_RATING_PER_YEAR[(mID, 2005 - i)]]
                i += 1
            avg_movie_rating = sum(movie_rating_year_sum) / \
                len(movie_rating_year_sum)

            writer.write(line)
            writer.write('\n')
        else:
                # It's a customer
            cID = int(line)
            assert 1 <= cID <= 2649429
            assert isinstance(cID, int)
            customer_rating_year_sum = []

            # most recent year average rating
            j = 0
            while (len(customer_rating_year_sum) <= 0) and (j <= 8):
                if (cID, 2005 - j) in AVERAGE_CUSTOMER_RATING_PER_YEAR:
                    customer_rating_year_sum += [
                        AVERAGE_CUSTOMER_RATING_PER_YEAR[(cID, 2005 - j)]]
                j += 1
            avg_customer_rating = sum(
                customer_rating_year_sum)/len(customer_rating_year_sum)

            pred = min(
                round((avg_customer_rating*5.5 + avg_movie_rating*4.5)/10, 1), 5.0)

            assert 1 <= pred <= 5

            predictions.append(pred)
            actual.append(ACTUAL_CUSTOMER_RATING[(cID, mID)])
            writer.write(str(pred))
            writer.write('\n')

    # calculate rmse for predications and actuals

    rmse = sqrt(mean(square(subtract(predictions, actual))))

    assert rmse > 0
    writer.write(str(rmse)[:4] + '\n')
