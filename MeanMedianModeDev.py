import pymongo
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

imdb_ratings=[]
imdb_votes= []
yrs=[]

# import matplotlib.pyplot as plt
# import numpy as np
# import plotly.plotly as py
# # Learn about API authentication here: https://plot.ly/python/getting-started
# # Find your api_key here: https://plot.ly/settings/api
#
# n = 50
# x, y, z, s, ew = np.random.rand(5, n)
# c, ec = np.random.rand(2, n, 4)
# area_scale, width_scale = 500, 5
#
# fig, ax = plt.subplots()
# sc = ax.scatter(x, y, s=np.square(s)*area_scale, c=c, edgecolor=ec, linewidth=ew*width_scale)
# ax.grid()
#
# plot_url = py.plot_mpl(fig, filename='mpl-7d-bubble')

def plot_graph(mean, median, mode, std):
        n_groups = 1
        index =  np.arange(n_groups)
        bar_width = 0.2
        opacity = 0.4
        ax = plt.subplot()

        # ax.scatter(mean, mean,facecolor='#777777',alpha=opacity,label="Mean")
        # ax.scatter(median, median,facecolor='#7777ff',alpha=opacity,label="Median")
        # ax.scatter(mode, mode,facecolor='#00ffaa',alpha=opacity,label="Mode")
        # ax.scatter(std, std,facecolor='#7777aa',alpha=opacity,label="Std dev")

        plt.bar(index,mean,bar_width,facecolor='#777777',alpha=opacity,label="Mean")
        plt.bar(index+bar_width,median,bar_width,facecolor='#7777ff',alpha=opacity,label="Median")
        plt.bar(index+2*(bar_width),mode,bar_width,facecolor='#00ffaa',alpha=opacity,label="Mode")
        plt.bar(index+3*(bar_width),std,bar_width,facecolor='#7777aa',alpha=opacity,label="Std dev")

        plt.legend()
        plt.xlabel('MeanMedianModeStdDev')
        plt.title(r'$Statistical Analysis$')
        plt.xticks(index,'Group1')
        plt.xticks(index + bar_width, ('statistics'))
        plt.legend()
        fig = plt.gcf()
        plt.show()
        fig.set_size_inches(8, 6)
        #fig.savefig('Awards Won.png', dpi = 600)

area_scale, width_scale = 500, 5
for i in range(2000,2016):
    p = str(i)
    yrs.append(p)
print yrs
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
            if(s =="N/A"):
                s = '0.0'
            if(d =="N/A"):
                d = "0"
            if ',' in d:
                a= d.split(",")
                t=a[0]+a[1]
                d=t
            imdb_ratings.append(s)
            imdb_votes.append(d)
            x = np.array(imdb_ratings)
            y = x.astype(np.float)
            p = np.array(imdb_votes)
            q = p.astype(np.float)
    mean =  np.mean(y)
    median = np.median(y)
    std = np.std(y)
    b = Counter(y)
    mode = b.most_common(1)
    print "Avg imdbRating over 2000-2015 is %f"%mean
    print "Rating most prevalent among movies over 2000-2015 is %s"%str(mode[0])
    print "Std deviation on imdbVotes is %f"%std
    print "Median over 2000-2015 is %f"%median
    statistics = [mean,median,std]
    print statistics

    conn.close()

except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e
