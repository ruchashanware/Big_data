import pymongo
import numpy as np
import matplotlib.pyplot as plt
import csv

# a_rating=[]
# d_rating=[]
# w_rating=[]

act = raw_input("Enter Actor/s in this movie (seperate with commas): ")
actors = act.split(",")

wri = raw_input("Enter Writer/s in this movie (seperate with commas): ")
writer =wri.split(",")

di = raw_input("Enter Director/s in this movie (seperate with commas): ")
director =di.split(",")

# actors = ['Angelina Jolie']
# writer = ['Dan Gilroy']
# director = ['Steven Sebring']

with open('crew.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerow([actors[0],director[0],writer[0]])
    


print "Actors are %s"% actors
print "Directors are %s"% director
print "Writers are %s"% writer

try:
    conn = pymongo.MongoClient()
    if (conn != None):
        print "Connected successfully!!!"
    db = conn["mock"]

    def weighted_rating(cur):
        i=0
        q=0.0
        sum=0
        for a in cur:
            qi = a['imdbRating']
            if(qi == "N/A"):
                print 'NAWR'
                continue
            i=i+1
            sum=sum+i
            s= float(qi)
            q=(q+(s*i))
        if(sum==0):
            # print '0' , 'weighted_rating'
            return 0.0

        # print q/sum , 'weighted_rating'
       
        return q/sum

    
    
    actor_movies = db.movies.find({'Actors': {'$regex': actors[0]}})
    director_movies = db.movies.find({'Director': {'$regex': director[0]}})
    writer_movies =db.movies.find({'Writer': {'$regex': writer[0]}})

    

    #director_movies = db.movies.find({'Actors': {'$regex': actors[0]}},{'Director': {'$regex': director[0]}})
    def combination_movies(mov1, mov2):
        combi_movies=[]
        for ac in mov1:
            mov2.rewind()
            for di in mov2:
                if (ac['_id'] == di['_id']):
                    combi_movies.append(di)
        return combi_movies    
        
    actor_director_movies = combination_movies(actor_movies.rewind(),director_movies.rewind())        
    actor_writer_movies = combination_movies(actor_movies.rewind(),writer_movies.rewind())
    director_writer_movies = combination_movies(director_movies.rewind(),writer_movies.rewind())
    actor_director_writer_movies = combination_movies(actor_director_movies,writer_movies.rewind())

    # print actor_director_movies , 'ac-dir'
    # print actor_director_writer_movies, 'ac-dir-wri'


    
    def predict_rating(arr,new_warr,countarr):
        earr = []
        earr.append(arr[0]*new_warr[0])
        earr.append(arr[1]*new_warr[1])
        earr.append(arr[2]*new_warr[2])
        if(countarr[0]*new_warr[0]+countarr[1]*new_warr[1]+countarr[2]*new_warr[2] == 0):
            return 0.0
        predicted_rating = (earr[0]+ earr[1]+ earr[2])/(countarr[0]*new_warr[0]+countarr[1]*new_warr[1]+countarr[2]*new_warr[2])
        print predicted_rating ,'rating'
        return predicted_rating

   
    def movies_till(movie, movieset):
        movies = []
        for mov in movieset:
            if(mov['_id'] == movie['_id']):
                break
            movies.append(mov)
        return movies

        # for Each actor_director_writer_movies find the weighted moving average of 
        #     i) actor, writer, director individually for the movies till that combination movie(actor_director_writer_movie)
        #     ii) actor_writer, director_writer , actor_director combination movies 
        #     iii) actor_director_writer combintion weighted_rating
    
    def sortarr(arr,warr,arr1,countarr):
        return_arr = []
        narr1 =[]
        xi=[]
        # print arr1 , 'arr1'
        for i in range(0,len(arr)):
            for j in range(i+1, len(arr)):
                if(arr[i]<arr[j]):
                    temp1=arr1[i]
                    temp2= warr[i]
                    temp3 = countarr[i]
                    arr1[i] = arr1[j]
                    warr[i] = warr[j]
                    countarr[i] = countarr[j]
                    arr1[j]=temp1
                    warr[j] = temp2
                    countarr[j]=temp3
        for i in arr1:
                # print i , 'i'
            p=i[1:]
            narr1.append(float(p))
            xi.append(i[0:1])
            # print narr1, 'narr1'
        return_arr.append(narr1)
        return_arr.append(warr)
        return_arr.append(countarr)
        return_arr.append(xi)
        # print return_arr , 'return_arr'
        return return_arr


    def average(arr):
        i=0
        sum = 0.0
        for val in arr:
            if(val==0):
                continue
            sum = sum + val
            i=i+1
        if(i==0):
            return [0 , 0]
        return [sum/i , i] 

    # print predicted_rating, 'rating'
    Wxarr =[]
    Wyarr =[]
    Wzarr =[]

    def weight_tuning(comb_movies, exclude):


        for movie in comb_movies:
            actual_rating = (movie['imdbRating'])
            print actual_rating , 'actual_rating'
            if(actual_rating =='N/A'):
                print 'next movie'
                continue
            Wx=300
            Wy=600
            Wz=1000

            act_movies =[]
            wri_movies =[]
            dir_movies =[]
            act_wri_movies =[]
            act_dir_movies = []
            dir_wri_movies = []
            act_dir_wri_movies = []

            act_movies =movies_till(movie, actor_movies.rewind())
            wri_movies = movies_till(movie, writer_movies.rewind())
            dir_movies = movies_till(movie, director_movies.rewind())
            act_wri_movies = movies_till(movie, actor_writer_movies)
            act_dir_movies = movies_till(movie, actor_director_movies)
            dir_wri_movies = movies_till(movie, director_writer_movies)
            act_dir_wri_movies = movies_till(movie, actor_director_writer_movies)

            if(exclude == 'Actor'):
                act_movies =[]
                act_wri_movies =[]
                act_dir_movies = []
                act_dir_wri_movies = []

            if(exclude == 'Director'):
                act_dir_movies = []
                act_dir_wri_movies = []
                dir_movies =[]
                dir_wri_movies = []

            if(exclude == 'Writer'):
                dir_wri_movies = []
                wri_movies =[]
                dir_wri_movies = []
                act_dir_wri_movies = []



            print len(dir_movies) , 'dir_movies'

            
            actor_weightrating = weighted_rating(act_movies)
            director_weightrating = weighted_rating(dir_movies)
            writer_weightrating = weighted_rating(wri_movies)

            
            actor_director_wrating = weighted_rating(act_dir_movies)
            actor_writer_wrating = weighted_rating(act_wri_movies)
            director_writer_wrating = weighted_rating(dir_wri_movies)

            actor_director_writer_wrating = weighted_rating(act_dir_wri_movies)

            a= average([actor_weightrating,director_weightrating,writer_weightrating])
            # print [actor_weightrating,director_weightrating,writer_weightrating]
            # print a , 'a'
            b= average([actor_writer_wrating,actor_director_wrating,actor_writer_wrating])
            # print b , 'b'
            c= average([actor_director_writer_wrating])
            # print c, 'c'

            # print exclude , 'exclude'
            x= a[0]*Wx
            y= b[0]*Wy
            z= c[0]*Wz

            countarr= [a[1],b[1],c[1]]
            # print z, 'z'

            if(x == 0.0):
                Wx=0
            if(y == 0.0):
                Wy=0
            if(z==0.0):
                Wz = 0
            arr = [x,y,z]
            # print Wx, 'Wx'
            # print arr , 'arr iniial'
            new_warr=[Wx,Wy,Wz]
            arr1 = [actor_weightrating+director_weightrating+writer_weightrating , actor_writer_wrating+actor_director_wrating+actor_writer_wrating , actor_director_writer_wrating]
            arr1i = ['x'+str(actor_weightrating+director_weightrating+writer_weightrating) ,'y'+str(actor_writer_wrating+actor_director_wrating+actor_writer_wrating) , 'z'+str(actor_director_writer_wrating)]
            # print arr1 , 'abc'
            actual_rating = float(movie['imdbRating'])
            predicted_rating = predict_rating(arr1,new_warr,countarr)
            print arr1 , new_warr , countarr ,'arr1 , new_warr , countarr '
            print predicted_rating,'predicted_rating'
            diff = actual_rating - predicted_rating
            print diff , 'diff'
            if(diff == actual_rating):
                print 'NOT  ENOUGH DATA'
                continue
            if(diff == 0):
                Wxarr.append(Wx)
                Wyarr.append(Wy)
                Wzarr.append(Wz)
                continue

            il=0
            while(diff >0.2 or diff < -0.2):
                # print arr, 'orig'
                
                return_arr = sortarr(arr,new_warr,arr1i,countarr)
                new_warr = return_arr[1]
                arr1 = return_arr[0]
                countarr = return_arr[2]
                indice = return_arr[3]
                # print arr1 ,'arr1'
                # print new_warr ,'warr', arr1 ,'abc' , countarr, 'countarr'
                if(diff > 0.2):
                    new_warr[0] = new_warr[0]-0.1*new_warr[0]
                    new_warr[2] = new_warr[2]+0.08*new_warr[2]
                    new_warr[1] = new_warr[1]+0.02*new_warr[1]
                    print 'diff>0.5'
                    # print new_warr , 'weight array'
                if(diff <-0.2):
                    new_warr[0] = new_warr[0]+0.1*new_warr[0]
                    new_warr[2] = new_warr[2]-0.08*new_warr[2]
                    new_warr[1] = new_warr[1]-0.02*new_warr[1]
                    print 'diff<-0.5'
                    # print new_warr , 'weight array'
                # diff = 0.1
                il = il+1
                prev_diff = diff
                    
                predicted_rating = predict_rating(arr1,new_warr,countarr)
                print arr1 , new_warr , countarr ,'arr1 , new_warr , countarr '
                diff =  actual_rating - predicted_rating
                print predicted_rating , 'predicted_rating'
                print actual_rating, 'actual_rating'
                print diff , 'diff'
                if(diff ==prev_diff):
                    break
                if(il>4):
                    break
                    
            
            print predicted_rating , 'predicted-final' ,movie['Title'], movie['_id']
            print actual_rating , 'actual_rating', movie['Title']
            Wxarr.append(new_warr[indice.index('x')]) 
            Wyarr.append(new_warr[indice.index('y')])
            Wzarr.append(new_warr[indice.index('z')])

    print 'abcd'        
    weight_tuning(actor_director_writer_movies,'None')
    # print Wxarr
    if(len(Wxarr) == 0 and len(Wyarr)==0 and len(Wzarr)==0):
       print 'abc'
       print 'actor_director'
       weight_tuning(actor_director_movies , 'Writer')
       print 'abc'
       print 'actor_writer'
       weight_tuning(actor_writer_movies, 'Director')
       print 'abc'
       print 'director_writer'
       weight_tuning(director_writer_movies , 'Actor')


    actor_weightrating = weighted_rating(actor_movies.rewind())
    print actor_weightrating , 'actor_weightrating'
    director_weightrating = weighted_rating(director_movies.rewind())
    print director_weightrating , 'director_weightrating'
    writer_weightrating = weighted_rating(writer_movies.rewind())
    print writer_weightrating , 'writer_weightrating'

    actor_director_wrating = weighted_rating(actor_director_movies)
    print actor_director_wrating ,'actor_director_wrating'
    actor_writer_wrating = weighted_rating(actor_writer_movies)
    print actor_writer_wrating , 'actor_writer_wrating '
    director_writer_wrating = weighted_rating(director_writer_movies)
    print director_writer_wrating, 'director_writer_wrating'

    actor_director_writer_wrating = weighted_rating(actor_director_writer_movies)
    print actor_director_writer_wrating , 'actor_director_writer_wrating'
    print len(Wxarr) , len(Wyarr) , len(Wzarr) , 'Lenghths'
    if(len(Wxarr) == 0 and len(Wyarr)==0 and len(Wzarr)==0):
        Wxarr.append(300)
        Wyarr.append(600)
        Wzarr.append(1000)


    Wx = average(Wxarr)
    Wy = average(Wyarr)
    Wz = average(Wzarr)

    print Wx , Wy, Wz , 'WXYZ'


    x= average([actor_weightrating,director_weightrating,writer_weightrating])
    y= average([actor_writer_wrating,actor_director_wrating,director_writer_wrating])
    z= average([actor_director_writer_wrating])

    print x, y,z ,'xyz'
    print '(',x[0],'*',x[1],'*',Wx[0],'+', y[0],'*',y[1],'*',Wy[0] ,'+', z,'*',Wz[0],')','/','(',x[1],'*',Wx[0], '+', y[1],'*',Wy[0] ,'+',z[1] , '*', Wz[0],')'

    final_rating = (x[0]*x[1]*Wx[0] + y[0]*y[1]*Wy[0] + z[0]*Wz[0])/(x[1]*Wx[0] + y[1]*Wy[0] + z[1]*Wz[0])

    print final_rating, 'final_rating'



    conn.close()

except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e
