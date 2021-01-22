from flask import Flask
from math import cos, asin, sqrt, pi
import json
from functools import cmp_to_key
from resturant import Resturant
app = Flask(__name__)
#export FLASK_ENV=development
#export FLASK_APP=app.py
# flask run
restaurants = []

#TODO calculate the listo fresturant just the first time 
@app.route('/')
def comp():
    latUsr = 60.1709
    lonUsr = 24.941 


    #----------------------------------------populating list
   # global restaurants
    with open("restaurants.json") as jsonFile:
        jsonResturants = json.load(jsonFile)        #return a dictionary
        jsonFile.close()

    # Iterating through the json 
    # list
    for jsonResturant in jsonResturants["restaurants"]:
        location = jsonResturant["location"]
        objResturant =  Resturant(lat =  location[0], lon = location[1], online = jsonResturant['online'], popularity = jsonResturant['popularity'], launchDate = jsonResturant['launch_date'], name = jsonResturant['name'] )

        restaurants.append((objResturant, objResturant.distance(latUsr, lonUsr)))
        ##restaurants.append((objResturant, 3))
        
    #----------------------------------------end 

    

    # or i can use sorted if i want to return the sorted list, without changing the original
    # most popular first
    restaurants.sort(key=(lambda resturant: resturant[0].popularity ), reverse = True)
    # for resturant in restaurants:
    #     if resturant.dis
    #newest first
    restaurants.sort(key=(lambda resturant: resturant[0].launchDate), reverse = True)
    #nearby first
    restaurants.sort(key= (lambda resturant : resturant[1] ), reverse = True)

    

    str = ""
    for resturant in restaurants:
        str += resturant[0].__str__()
    return str
#import all object from json and create the list
    

if __name__ == '__main__':
    app.run()
    

    
        
        
        
    
    #2 strategies or import all the file and create a List of object or import just near our location