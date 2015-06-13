## Calculating weighted moving average of a data set and training weights to fine tune weighted moving average for a target average

##Related Links:
Reference from [IMDb FAQ page](http://www.imdb.com/help/show_leaf?votestopfaq)
##Requirements:
•	An installation of MongoDB -- http://www.mongodb.org/downloads
##Steps:
### 1. Query data from database
In this instance, json objects are stored in our DB.  And we are fetching movies details where we find these Actors, Directors and Writers.

### 2. Analysis Logic:
2.1	Find the weighted moving average(`wma`) of director, actor, writer using movie rating say d, a, w

2.2	Find `wma` of actor- director, writer-actor, actor-writer combination say `ad`, `aw`, `wc`

2.3	Find `wma` of actor-director-writer combination, `adw`

2.4	Calculate the rating using 

`((x*d+x*w+x*a)+(y*ad+y*dw+y*aw)+(z*adw))/(3x+3y+z) where x,y,z are the weights and z>y>x so give z=1000, y= 600, x=300`

2.5	Substitute  these values in the equation and find the rating and compare with the original rating for an already existing movie with this `a-d-w` combination

2.6	Find the difference and then adjust the weights accordingly.


