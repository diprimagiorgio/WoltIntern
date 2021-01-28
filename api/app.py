from flask import Flask, jsonify, request
from json import load                                
from api.resturant import Resturant


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False #otherwise flask changes the sorting in the output

                
#returns the first 10 elements if they are closer than 1.5 km. Opened restaurants are inserted first
def getTop(restaurants, numElem, maxDistance):
    result = []
    offline = []
    for (resturant, distance) in restaurants:
        if len(result) < numElem and distance < maxDistance: # I need to find only 10 restaurants, Only restaurant closer than 1.5Km can be included in the result 
            if resturant.online:
                result.append(resturant)
            else:
                offline.append(resturant)
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

    #------------------------------------- Reading JSON and populating the list of restaurants
    restaurants = []
   # from JSON to dictionary
    with open("restaurants.json") as jsonFile:
        jsonResturants = load(jsonFile)        
        jsonFile.close()

    # from dictionary to list of Restaurants 
    for jsonResturant in jsonResturants["restaurants"]:
        location = jsonResturant["location"]
        objResturant =  Resturant(lon =  location[0], lat = location[1],
                                  online = jsonResturant['online'],
                                  popularity = jsonResturant['popularity'],
                                  launchDate = jsonResturant['launch_date'],
                                  name = jsonResturant['name'],
                                  blurhash = jsonResturant['blurhash']
                                )
        distance = objResturant.distance(latUsr, lonUsr)
        if  distance < maxDistance:
            restaurants.append((objResturant, distance))
        
    #------------------------------------- Sorting 
    
    # most popular first
    restaurants.sort(key=(lambda resturant: resturant[0].popularity ), reverse = True)
    popularResturants = getTop(restaurants, numElem, maxDistance )
    
    # newest first
    restaurants.sort(key=(lambda resturant: resturant[0].launchDate), reverse = True)
    newestResturants = getTop(restaurants, numElem, maxDistance)
    
    # closest first
    restaurants.sort(key= (lambda resturant : resturant[1] ), reverse = True)
    closestResturant = getTop(restaurants, numElem, maxDistance)

    #------------------------------------- Enveloping result 

    
    result = {
        "sections" : [
            {
                "title" : "Popular Restaurants",
                "restaurants" : [ resturant.getDict() for resturant in popularResturants]
            },
            {
                "title" : "New Restaurants",
                "restaurants" : [ resturant.getDict() for resturant in newestResturants]
            },
            {
                "title" : "Nearby Restaurants",
                "restaurants" : [ resturant.getDict() for resturant in closestResturant]
            }
        ]
    }

    return jsonify(result)

    