from flask import jsonify, request
from json import load                                
from api.restaurant import Restaurant
from api import app

#returns the first 10 elements if they are closer than 1.5 km. Opened restaurants are inserted first
def getTop(restaurants, numElem, maxDistance):
    result = []
    offline = []
    for (restaurant, distance) in restaurants:
        if len(result) < numElem and distance < maxDistance: # I need to find only 10 restaurants, Only restaurant closer than 1.5Km can be included in the result 
            if restaurant.online:
                result.append(restaurant)
            else:
                offline.append(restaurant)
    x = 0
    while len(result) < numElem and x < len(offline) :  # if I have not found the necessary elements I can include the offline one
            result.append(offline[x])
            x += 1
    return result


# Tries to typecast string to float
def transcribe_float(str_nb):
	try:
		nb = float(str_nb)
	except:
		nb = None
	return nb

# Validates parametres
def validate_params(lat, lon):
    return -90 <= lat <= 90 and -180 <= lon <= 180 

@app.route('/discovery')
def discovery():
    numElem = 10
    maxDistance = 1.5
    #------------------------------------- Reading and validating input value
    if request.args.get('lat') and request.args.get('lon') :    
        latUsr = transcribe_float(request.args.get('lat'))
        lonUsr = transcribe_float(request.args.get('lon'))
        if not validate_params(latUsr, lonUsr):
            return "Bad Request, the values are not correct!", 400
    else:
        return "Bad Request, you must insert the  lat (latitude) and lon (longitude) values!", 400

    #------------------------------------- Reading JSON and populating the list of: (restaurants, the distance between the user location and the resturant)
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
        distance = objRestaurant.distance(latUsr, lonUsr)
        if  distance < maxDistance:
            restaurants.append((objRestaurant, distance))
        
    #------------------------------------- Sorting 
    
    # most popular first
    restaurants.sort(key=(lambda restaurant: restaurant[0].popularity ), reverse = True)
    popularRestaurants = getTop(restaurants, numElem, maxDistance )
    
    # newest first
    restaurants.sort(key=(lambda restaurant: restaurant[0].launchDate), reverse = True)
    newestRestaurants = getTop(restaurants, numElem, maxDistance)
    
    # closest first
    restaurants.sort(key= (lambda restaurant : restaurant[1] ), reverse = True)
    closestRestaurants = getTop(restaurants, numElem, maxDistance)

    #------------------------------------- Enveloping result 

    
    result = {
        "sections" : [
            {
                "title" : "Popular Restaurants",
                "restaurants" : [ restaurant.getDict() for restaurant in popularRestaurants]
            },
            {
                "title" : "New Restaurants",
                "restaurants" : [ restaurant.getDict() for restaurant in newestRestaurants]
            },
            {
                "title" : "Nearby Restaurants",
                "restaurants" : [ restaurant.getDict() for restaurant in closestRestaurants]
            }
        ]
    }

    return jsonify(result)