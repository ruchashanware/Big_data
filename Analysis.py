import pymongo
import re
import numpy as np

crew=[]
imdb_ratings=[]

act = raw_input("Enter Actor/s in this movie (seperate with commas): ")
actors = act.split(",")
crew =crew + actors

wri = raw_input("Enter Writer/s in this movie (seperate with commas): ")
writer =wri.split(",")
crew = crew + writer

di = raw_input("Enter Director/s in this movie (seperate with commas): ")
director =di.split(",")
crew = crew + director

print crew

try:
    conn = pymongo.MongoClient()
    if (conn != None):
        print "Connected successfully!!!"
    db = conn["moviesDB"]

    for j in actors:
        print "Actor : %s"%j
        cur = db.movies.find({'Actors': {'$regex': j}})
        for a in cur:
            imdb_ratings.append(a['imdbRating'])
            #T2 = [map(int, x) for x in imdb_ratings]
            #x = np.array(imdb_ratings)
            #y = x.astype(np.float)
        print "##############  ACTORS  #############"
    #print y

    for j in writer:
        print "Writer: %s"%j
        cur = db.movies.find({'Writer': {'$regex': j}})
        for a in cur:
            imdb_ratings.append(a['imdbRating'])
            #T2 = [map(int, x) for x in imdb_ratings]
            #x = np.array(imdb_ratings)
            #y = x.astype(np.float)
        print "############## WRITERS #################"

    for j in director:
        print "Director %s"%j
        cur = db.movies.find({'Writer': {'$regex': j}})
        for a in cur:
            imdb_ratings.append(a['imdbRating'])
            #T2 = [map(int, x) for x in imdb_ratings]
            #x = np.array(imdb_ratings)
            #y = x.astype(np.float)
        print "############## DIRECTORS #################"
    x = np.array(imdb_ratings)
    y = x.astype(np.float)
    print y
    #e  = np.asarray(imdb_ratings)
    mean =  np.mean(y)
    print mean
    #print "Avg imdbRating go" mean
    conn.close()

except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e
