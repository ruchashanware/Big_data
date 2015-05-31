import csv
import pymongo
import numpy as np
import matplotlib.pyplot as plt

actors = ['Russell Crowe']
director= ['Ridley Scott']
writer = ['David Franzoni']

with open('crew.csv', 'rb') as csvfile:
	data = csv.reader(csvfile, delimiter=',')
	for row in data:
		actors = row[0]
		director = row[1]
		writer = row[2]


print "Actors are %s"% actors
print "Directors are %s"% director
print "Writers are %s"% writer

try:
    conn = pymongo.MongoClient()
    if (conn != None):
        print "Connected successfully!!!"
    db = conn["mock"]
    def rating(crew):
	    w_rating= []
	    print 'a'  
	    for a in crew:
	        qi = a['imdbRating']
	        if(qi == "N/A"):
	            qi = '0.0'
	        w_rating.append(qi)
	        # print w_rating ,'k'
	    return  w_rating   

	

    
    def rate_grouping(ay):
        eight=0
        six=0
        four=0
        other=0
        for y in ay:
            if(y>=8):
                eight= eight+1
            if(y>6 and y<8):
                six= six+1
            if(y<6 and y>4):
                four= four+1
            if(y<4):  
                other = other+1
        # print len(ay)
        return [float(eight*100)/float(len(ay)),float(six*100)/float(len(ay)),float(four*100)/float(len(ay)),float(other*100)/float(len(ay))]


    def plot_graph(percent, name):
        colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
        labels=['8-10','6-8','4-6','< 4']
        plt.pie(percent, labels=labels, colors=colors,
        autopct='%1.1f%%', startangle=0)
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        fig =plt.gcf()
        # plt.show()
        fig.set_size_inches(8, 6)
        fig.savefig(name+'.png', dpi = 600)

    def graph_data(percent,name):
    	data = [
            [name,'Rating 8-10'+'    '+ str(round(percent[0])) +'%', str(percent[0])],
            [name,'Rating 6-8'+'    '+str(round(percent[1]))+'%', str(percent[1])],
            [name,'Rating 4-6'+'     '+str(round(percent[2]))+'%', str(percent[2])],
            [name,'Rating <4'+'     '+str(round(percent[3]))+'%', str(percent[3])]]
        return data

    actor_movies = db.movies.find({'Actors': {'$regex': actors[0]}})
    director_movies = db.movies.find({'Director': {'$regex': director[0]}})
    writer_movies =db.movies.find({'Writer': {'$regex': writer[0]}})

    ab_rating = rating(actor_movies.rewind())
    ax = np.array(ab_rating)
    ay = ax.astype(np.float)
    actor_mean =  np.mean(ay)   
    percent_act = rate_grouping(ay)
    plot_graph(percent_act, 'Actor')
        
            
    print "Average performance of Actors %s"%actors+" is %f"%actor_mean

    d_rating = rating(director_movies.rewind())
    dx = np.array(d_rating)
    dy = dx.astype(np.float)
    percent_dir = rate_grouping(dy)
    plot_graph(percent_dir, 'Director')
    director_mean = np.mean(dy)
    print "Average performance of Directors %s"%director+" is %f"%director_mean

    w_rating = rating(writer_movies.rewind())
    wx = np.array(w_rating)
    wy = wx.astype(np.float)
    percent_wri = rate_grouping(wy)
    plot_graph(percent_wri,'Writer')
    writer_mean =np.mean(wy)
    print "Average performance of Writers %s"%writer+"is %f"%writer_mean

    with open('mean.csv', 'wb') as fp:
	    a = csv.writer(fp, delimiter=',')
	    a.writerow(['State','Actor','Director','Writer'])
	    data = [' Average',actor_mean,director_mean,writer_mean]
	    a.writerow(data)

    with open('rating.csv', 'wb') as fp:
	    a = csv.writer(fp, delimiter=',')
	    a.writerow(['origin','carrier','count'])
	    data = graph_data(percent_act, 'Actor')
	    a.writerows(data)

    with open('rating.csv', 'ab') as fp:
	    a = csv.writer(fp, delimiter=',')
	    data = graph_data(percent_dir , 'Director')
	    a.writerows(data)

    with open('rating.csv', 'ab') as fp:
	    a = csv.writer(fp, delimiter=',')
	    data = graph_data(percent_wri , 'Writer')
	    a.writerows(data)

	

    conn.close()

except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e