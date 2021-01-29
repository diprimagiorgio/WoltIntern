from datetime import date
from geopy import distance

class Restaurant:

    def __init__(self, lat, lon, online, popularity, launchDate, name, blurhash):
        self.blurhash = blurhash
        self.lat = lat
        self.lon = lon
        self.online = online
        self.popularity = popularity
        self.launchDate = date.fromisoformat(launchDate)
        self.name = name
        
    
    
    def distance(self, lat, lon):
        coordsPtA = (self.lat, self.lon)
        coordsPtB = (lat,lon)
        return distance.distance(coordsPtA, coordsPtB).km

    # Used for debugging
    def __str__(self):
        return "\n\nI'm restaurant {name} situated in {lat}, {lon} I'm {popularity:.2f} popular I'm open since {launchDate} and now I'm online = {online}!\n".\
            format(lat = self.lat, lon = self.lon, online = self.online, popularity = self.popularity, launchDate = self.launchDate, name = self.name )


    def getDict(self):
        res = { 
                "blurhash" : self.blurhash,
                "launch_date" : self.launchDate.isoformat(),
                "location" : (self.lat, self.lon),
                "name" : self.name,
                "online" : self.online,
                "popularity" : self.popularity

        }
        return res


                