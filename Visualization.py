__author__ = 'Rucha'
import pymongo
import numpy as np
import matplotlib.pyplot as plt
from operator import add

act = raw_input("Enter Actor/s in this movie (seperate with commas): ")
actors = act.split(",")
wri = raw_input("Enter Writer/s in this movie (seperate with commas): ")
writer =wri.split(",")
di = raw_input("Enter Director/s in this movie (seperate with commas): ")
director =di.split(",")
a_awd_arr=[0, 0, 0, 0]
d_awd_arr=[0, 0, 0, 0]
w_awd_arr=[0, 0, 0, 0]

print "Actors are %s"% actors
print "Writers are %s"% writer
print "Directors are %s"% director

try:
    conn = pymongo.MongoClient()
    if (conn != None):
        print "Connected successfully!!!"
    db = conn["moviesDB"]

    def plot_graph(a_awards, w_awards, d_awards):
        n_groups=4
        index =  np.arange(n_groups)
        bar_width = 0.2
        opacity = 0.4
        ax = plt.subplots()

        plt.bar(index,a_awards,bar_width,facecolor='#777777',alpha=opacity,label="Actor")
        plt.bar(index+bar_width,d_awards,bar_width,facecolor='#7777ff',alpha=opacity,label="Director")
        plt.bar(index+2*(bar_width),w_awards,bar_width,facecolor='#00ffaa',alpha=opacity,label="Writer")
        #fig4 = plt.bar(index,a_awards,bar_width,facecolor='#7777aa',alpha=opacity)
        plt.legend()
        plt.xlabel('Awards')
        plt.title(r'$Achievments$')
        plt.xticks(index + bar_width, ('Oscar', 'Golden Globe', 'BAFTA', 'Emmy'))
        plt.legend()
        fig = plt.gcf()
        plt.show()
        fig.set_size_inches(8, 6)
        fig.savefig('Awards Won.png', dpi = 600)

    def awards_count(cur):
        achieve = {'Oscar':0,'Golden Globe':0,'BAFTA':0,'Emmy':0,'Others':0}
        for a in cur:
            r = a["Awards"]
            if(r =='N/A'):
                awards = '0'
            else:
                if 'Oscar' in r:
                    osc = r.split('Oscar')
                    for aw in osc:
                        if 'Won' in aw:
                            j = aw.split(' ')
                            o = j[1]
                            achieve['Oscar']=achieve['Oscar']+ int(o)
                        elif 'Nominated' in aw:
                            j = aw.split(' ')
                            o = j[2]
                            achieve['Oscar']=achieve['Oscar']+ int(o)
                        elif 'win' in aw:
                            winarr = aw.split(' ')
                            win = winarr[2]
                            achieve['Others']=achieve['Others']+ int(win)

                elif 'Golden Globe' in r:
                    gg = r.split('Golden Globe')
                    for aw in gg:
                        if 'Won' in aw:
                            j = aw.split(' ')
                            o = j[1]
                            achieve['Golden Globe']=achieve['Golden Globe']+ int(o)
                        elif 'Nominated' in aw:
                            j = aw.split(' ')
                            o = j[2]
                            achieve['Golden Globe']=achieve['Golden Globe']+ int(o)
                        elif 'win' in aw:
                            winarr = aw.split(' ')
                            win = winarr[2]
                            achieve['Others']=achieve['Others']+ int(win)

                elif 'BAFTA' in r:
                    gg = r.split('BAFTA')
                    for aw in gg:
                        if 'Won' in aw:
                            j = aw.split(' ')
                            o = j[1]
                            achieve['BAFTA']=achieve['BAFTA']+ int(o)
                        elif 'Nominated' in aw:
                            j = aw.split(' ')
                            o = j[2]
                            achieve['BAFTA']=achieve['BAFTA']+ int(o)
                        elif 'win' in aw:
                            winarr = aw.split(' ')
                            win = winarr[4]
                            achieve['Others']=achieve['Others']+ int(win)

                elif 'Primetime Emmy' in r:
                    gg = r.split('Emmy')
                    for aw in gg:
                        if 'Won' in aw:
                            j = aw.split(' ')
                            o = j[1]
                            achieve['Emmy']=achieve['Emmy']+ int(o)
                        elif 'Nominated' in aw:
                            j = aw.split(' ')
                            o = j[2]
                            achieve['Emmy']=achieve['Emmy']+ int(o)
                        elif 'win' in aw:
                            winarr = aw.split(' ')
                            win = winarr[2]
                            achieve['Others']=achieve['Others']+ int(win)

                elif 'win' in r:
                    winarr = r.split(' ')
                    win = winarr[0]
                    achieve['Others']=achieve['Others']+ int(win)
        return [achieve['Oscar'],achieve['Golden Globe'],achieve['BAFTA'],achieve['Emmy']]

    for j in actors:
        print "---> ACTOR :%s"%j
        cur = db.movies.find({'Actors': {'$regex': j}})
        print "in actor awards_count"
        a = awards_count(cur)
        a_awd_arr = map(add, a_awd_arr, a)
    print "Actor awards %s "%str(a_awd_arr)

    for j in writer:
        print "---> WRITER :%s"%j
        cur = db.movies.find({'Writer': {'$regex': j}})
        print "in writer awards_count"
        a = awards_count(cur)
        w_awd_arr = map(add, w_awd_arr, a)
    print "Writer awards %s "%str(w_awd_arr)

    for j in director:
        print "---> DIRECTOR:%s"%j
        cur = db.movies.find({'Director': {'$regex': j}})
        print "in director awards_count"
        a = awards_count(cur)
        d_awd_arr = map(add, d_awd_arr, a)
    print "Director awards %s "%str(d_awd_arr)

    plot_graph(a_awd_arr,w_awd_arr,d_awd_arr)
    conn.close()

except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e
