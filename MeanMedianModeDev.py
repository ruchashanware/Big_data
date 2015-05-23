import pymongo
import re
import numpy as np
from collections import Counter

imdb_ratings=[]
imdb_votes= []
yrs=[]
for i in range(2000,2016):
    p = str(i)
    yrs.append(p)
try:
    conn = pymongo.MongoClient()
    if (conn != None):
        print "Connected successfully!!!"
    db = conn["moviesDB"]
    for j in yrs:
        print j
        cur = db.movies.find({'Year': {'$regex': j}})
        for a in cur:
            s = a['imdbRating']
            d = a['imdbVotes']
            #print d
            #print s
            if(s =="N/A"):
                #print "in if s = n/a"
                s = '0.0'
            if(d =="N/A"):
                #print "in if s = n/a"
                d = "0"
            if ',' in d:
                #print "contains comma"
                a= d.split(",")
                t=a[0]+a[1]
                d=t
                #print t


            imdb_ratings.append(s)
            imdb_votes.append(d)
            #print imdb_ratings
            #T2 = [map(int, x) for x in imdb_ratings]
            x = np.array(imdb_ratings)
            y = x.astype(np.float)
            p = np.array(imdb_votes)
            q = p.astype(np.float)
        print "###############################"
    #print y
    #e  = np.asarray(imdb_ratings)
    mean =  np.mean(y)
    median = np.median(y)
    b = Counter(y)
    d = np.std(q)


    print "Avg imdbRating over 2000-2015 is %f"%mean

    print "Rating most prevalent among movies over 2000-2015 is %s"%str(b.most_common(1))

    print "Std deviation on imdbRatings is %f"%d

    print "Median over 2000-2015 is %f"%median


    conn.close()

except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e
