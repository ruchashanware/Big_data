import codecs
import urllib
from bs4 import BeautifulSoup
import urllib2
import os
import re
import json

if not os.path.exists("wikimovies2010_2015.txt"):
#    print "%%%%%%%%%%%%%%%%%% in path exists or not"
    file = codecs.open("wikimovies2010_2015.txt", "a")
    if os.stat("wikimovies2010_2015.txt").st_size==0:
        urls = ["http://en.wikipedia.org/wiki/List_of_American_films_of_2010",
            "http://en.wikipedia.org/wiki/List_of_American_films_of_2011",
            "http://en.wikipedia.org/wiki/List_of_American_films_of_2012",
            "http://en.wikipedia.org/wiki/List_of_American_films_of_2013",
            "http://en.wikipedia.org/wiki/List_of_American_films_of_2014",
            "http://en.wikipedia.org/wiki/List_of_American_films_of_2015"]

        for url in urls:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page.read())
            if url != None:
                yr=[]
                yr = url.split('_')
                year = yr[len(yr)-1]

            file = codecs.open("wikimovies2010_2015.txt", "a")

            for node in soup.findAll('i'):
                for no in node.findAll('a'):
                    movie = ''.join(no.findAll(text=True))
                    mov = movie.encode('utf-8')
                   # print mov
                    file.writelines(str(mov)+" Year:"+str(year)+"\n")
            file.close()

elif os.path.exists("wikimovies2010_2015.txt"):
    print "in else"
    i=0
    filemovies = open("wikimovies2010_2015.txt").read()
    movielist = filemovies.split("\n")


    #req = urllib.urlopen("http://www.omdbapi.com/?t=B.O.O.%3A+Bureau+of+Otherworldly+Operations&y=2015&plot=short&r=json")
    #res = json.load(req)


    for i in range(0,len(movielist)):
        title_yr = movielist[i].split(" Year:")

        t = str(title_yr[0])
        #print t
        if ":" in t:
            t = str(t.replace(":","%3A"))
        title = t.replace(" ","+")
        print str(title)
        req = urllib.urlopen("http://www.omdbapi.com/?t="+title+"&y="+str(title_yr[1])+"&plot=short&r=json")
        res = json.load(req)
        if res != None:
           print res

