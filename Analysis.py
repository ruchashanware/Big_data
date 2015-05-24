import pymongo
import numpy as np

a_rating=[]
d_rating=[]
w_rating=[]

act = raw_input("Enter Actor/s in this movie (seperate with commas): ")
actors = act.split(",")

wri = raw_input("Enter Writer/s in this movie (seperate with commas): ")
writer =wri.split(",")

di = raw_input("Enter Director/s in this movie (seperate with commas): ")
director =di.split(",")

print "Actors are %s"% actors
print "Directors are %s"% director
print "Writers are %s"% writer

try:
    conn = pymongo.MongoClient()
    if (conn != None):
        print "Connected successfully!!!"
    db = conn["moviesDB"]

    for j in actors:
        cur = db.movies.find({'Actors': {'$regex': j}})
        for a in cur:
            q = a['imdbRating']
            if(q == "N/A"):
                q = '0.0'
           # if(q == )
            a_rating.append(q)

    for j in writer:
        cur = db.movies.find({'Writer': {'$regex': j}})
        for a in cur:
            q = a['imdbRating']
            if(q == "N/A"):
                q = '0.0'
            w_rating.append(q)

    for j in director:
        cur = db.movies.find({'Director': {'$regex': j}})
        for a in cur:
            q = a['imdbRating']
            if(q == "N/A"):
                q = '0.0'
            d_rating.append(q)

    ax = np.array(a_rating)
    ay = ax.astype(np.float)
    actor_mean =  np.mean(ay)
    actor_dev = np.std(ay)
    print "Average performance of Actors %s"%actors+" is %f"%actor_mean
    #print "Std Deviation in Actor performances is %f"%actor_dev

    dx = np.array(d_rating)
    dy = dx.astype(np.float)
    director_mean = np.mean(dy)
    print "Average performance of Directors %s"%director+" is %f"%director_mean

    wx = np.array(w_rating)
    wy = wx.astype(np.float)
    writer_mean =np.mean(wy)
    print "Average performance of Writers %s"%writer+"is %f"%writer_mean

    conn.close()

except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e
