from flask import Flask, jsonify, request
import json             # necessary for loading the json
from api.resturant import Resturant


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False #otherwise flask change orger of json

                
#take the first 10 element if they are closer than 1.5 km, and the populate the list wiht online first
def getTop(restaurants, numElem, maxDistance):
    result = []
    offline = []
    for (resturant, distance) in restaurants:
        if len(result) < numElem and distance < maxDistance: # I need to find only 10 resturants, Only resturant closer than 1.5Km can be included in the result 
            if resturant.online:
                result.append(resturant)
            else:
                offline.append(resturant)
    x = 0
    while len(result) < numElem and x < len(offline) :  # if i have not found the necessay elements i can include the offline one
            result.append(offline[x])
            x += 1
    return result


# Tries to typecast string to float, returns None failure
def transcribe_float(str_nb):
	try:
		nb = float(str_nb)
	except:
		nb = None
	return nb

# Validates parametres, make it pretty TODO
def validate_params(lat, lon):
	if not (-90 <= lat <= 90):
		return False
	elif not (-180 <= lon <= 180):
		return False
	else:
		return True

#TODO calculate the listo fresturant just the first time 
@app.route('/discovery')
def discovery():
    numElem = 10
    maxDistance = 1.5
    #-------------------------------------reading and validating input value
    if request.args.get('lat') and request.args.get('lon') :    
        latUsr = transcribe_float(request.args.get('lat'))
        lonUsr = transcribe_float(request.args.get('lon'))
        if not validate_params(latUsr, lonUsr):
            return "Bad Request, the values are not correct!", 400
    else:
        return "Bad Request, you must insert the  lat (latitude) and lon (longitude) values!", 400

    #----------------------------------------reading json and populating list of resturants
    restaurants = []
   # from json to dictionary
    with open("restaurants.json") as jsonFile:
        jsonResturants = json.load(jsonFile)        
        jsonFile.close()

    # from dictionary to list of Resturants 
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
        
    #---------------------------------------- sorting 

    

    # i sort the same list, with different comparison method, without creating a new one

    # most popular first
    restaurants.sort(key=(lambda resturant: resturant[0].popularity ), reverse = True)
    popularResturants = getTop(restaurants, numElem, maxDistance )
    
    # newest first
    restaurants.sort(key=(lambda resturant: resturant[0].launchDate), reverse = True)
    newestResturants = getTop(restaurants, numElem, maxDistance)
    
    # closest first
    restaurants.sort(key= (lambda resturant : resturant[1] ), reverse = True)
    closestResturant = getTop(restaurants, numElem, maxDistance)

    #---------------------------------------- Enveloping result 

    
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

    #2 strategies or import all the file and create a List of object or import just near our location