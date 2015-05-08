import codecs
from bs4 import BeautifulSoup
import urllib2
import re
import json
import pymongo

urls=[]
for i in range(0,10):
    u ="http://en.wikipedia.org/wiki/List_of_American_films_of_200"+str(i)
    urls.append(u)
for i in range(10,16):
    u ="http://en.wikipedia.org/wiki/List_of_American_films_of_20"+str(i)
    urls.append(u)

#file = codecs.open("wikimovies2000_2015.txt", "a")
try:
    conn= pymongo.MongoClient()
    print "Connected successfully!!!"
    db = conn["mock"]
    seq = {'Title','Country','Writer','imdbRating',
           'Director','Actors','Year','Genre',
           'Awards','imdbVotes','imdbID'}
    for url in urls:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        searchObj = re.search(r'\d{4}', url)
        year = searchObj.group()
        for node in soup.findAll('i'):
            for no in node.findAll('a'):
                movie = ''.join(no.findAll(text=True))
                mov = movie.encode('utf-8')
                if ":" or "?" or "," or "/"in mov:
                    mov = str(mov.replace(":","%3A"))
                    mov = str(mov.replace("?","%3F"))
                    mov = str(mov.replace(",","%2C"))
                    mov = str(mov.replace("/","%2F"))
                mov = mov.replace(" ","+")
                try:
                    req = urllib2.urlopen("http://www.omdbapi.com/?t="+str(mov)+"&y="+str(year)+"&plot=short&r=json")
                    res = json.load(req)
                    if res["Response"] == "True":
                        movie = { your_key: res[your_key] for your_key in seq }
                        db.movies.insert(movie)
                except:
                    None
    print list(db.movies.find())
    #print "########################"
    conn.close()
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e

