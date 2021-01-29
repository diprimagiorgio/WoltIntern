from flask import redirect
from json import load                                
from api.restaurant import Restaurant
from api import app
from random import randint
from geopy import distance, Point

# generate a random point near one of the restaurants, and it calls the discovery function
@app.route('/testRandomPoint')
def testRandomPoint():
    #------------------------------------- Reading JSON and populating the list of: restaurants
    restaurants = []
    # from JSON to dictionary
    with open("restaurants.json") as jsonFile:
        jsonRestaurants = load(jsonFile)        
        jsonFile.close()

    # from dictionary to list of Restaurants 
    for jsonRestaurant in jsonRestaurants["restaurants"]:
        location = jsonRestaurant["location"]
        objRestaurant =  Restaurant(lon =  location[0], lat = location[1],
                                online = jsonRestaurant['online'],
                                popularity = jsonRestaurant['popularity'],
                                launchDate = jsonRestaurant['launch_date'],
                                name = jsonRestaurant['name'],
                                blurhash = jsonRestaurant['blurhash']
                                )
        restaurants.append(objRestaurant)
    
    #take a random restaurant
    rst = restaurants[randint(0,len(restaurants) - 1)]
    # Define a starting point.
    start = Point(rst.lat, rst.lon)

    # Define a general distance object, initialized with a distance between 1.5 km to 3km.
    d = distance.distance(kilometers = randint(1500, 3000) / 1000.)

    # Use the `destination` method with a bearing of random degrees (0 =  north 180 = south)
    
    # in order to go from point `start` to another random point
    destination = d.destination(point=start, bearing= randint(0, 360) )
    
    return redirect("/discovery?lat={lat}&lon={lon}".format(lat = destination.latitude, lon =  destination.longitude))