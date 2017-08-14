# interative_map_based_visiualization_tool
Creating an interactive map based visualization tool for data that is spread out across time and space.

In this project I have made shown the trend of African football over last seven year.
The main challenge was to work on mapbox(Map location, navigation sdk)

Features:
1) the view is divided into three zoom level.
    * initial zoom shows the top four country and their scores
    * the Second zoom shows the stadium locations
    * the Third zoom shows the players location

2) Each player, stadium, country has details attached to it, a pop will be displayed on click

3) Each pop up are editable.

4) A slider showing different games information in a dashboard


 link to the app:   
 https://interative-map-based-visiualiz.herokuapp.com/
 

 ![Web app](static/css/web_app.gif)  
 ___
 
# Thinking to know

postgresql
* heroku ps:psql
* \dt : use only see a tables
* \dt schema_name.* : if you want to see specific schema tables
* \l  : if want to see schema tables

# Problem faced

**I am unable to understand how postgresql is storing the rows corresponding to the table**  
I am not understand that though the values are getting stored in the postgresql but I am  not getting the name of the table
. For that I tried to search what are the available tables, to this I came to know 
only available public table is user and it shows the currrent user.
But still unable to know where all the data are getting saved.


**problem in json parsing**

I thought that instead of keeping a geojson on the server I will generate the files dynamically but I am not able to make it work. So forcefully I am keeping the static file in the server. But I will think over this problem and review it.


**problem in understanding data driven style**
Unable to understand the functioning of stops(getting a idea its a count to colour mapping but not understanding its use with circle radius) when adding dynamic layer.

**Faced problem while installing Lxml file**
Came to know that sudo is not supported in heroku. So finally created a egg file in own system that is compatible with python-2.7-13, hope it works now.

**This was a unique problem which took the whole day**  
I was unable to parse unicode values. I checked my regex it was fine
but it was unable to detect. I encoded the whole webpage to utf-8, still it was not working

Error:
* UnicodeEncodeError: 'ascii' codec can't encode character u'\xe7' in position 7982: ordinal not in range(128)

So on repeated hit and trial I came to a conclusion if I can encode each word to ascii and see it works
and voila it works...!! 

**Confusion in deciding the project flow and the table structure**  
Finally I have 7 table structure

* AFRICAN_CUP
* COUNTRY
* PLAYER
* STADIUM
* RELATION_CUP_COUNTRY : stores the score,position by each country in each year 
* RELATION_CUP_STADIUM : stores the list of stadiums where matches were held each year
* RELATION_CUP_COUNTRY_PLAYER : stores the list of players who made highest goals or named best player on each year


**Faced problem in deploying the app in heroku**   
This was interesting problem, so flask renders html webpages from templates and static files(js, css) from static
So it is required to make the folder structure that meets criteria of flask.
Finally deployed after defining os path to the folders as it was not detecting from the root.

**Problem with lower version of firefox**  
The webkit used in the css is not working in lower versions of firefox.
Need to be fixed.
