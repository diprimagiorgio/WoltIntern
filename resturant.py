from datetime import date

class Resturant:

    distance = -1
    def __init__(self, lat, lon, online, popularity, launchDate, name):
        self.lat = lat
        self.lon = lon
        self.online = online
        self.popularity = popularity
        self.launchDate = date.fromisoformat(launchDate)
        self.name = name
        

    def prova(lat1, lon1, lat2, lon2):
        p = pi/180
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
        return 12742 * asin(sqrt(a)) #2*R*asin...
    
    def distance(self, lat, lon):
        return prova(self.lat, self.lon, lat, lon)

    
    def __str__(self):
        return "\n\nI'm resturant {name} situated in {lat}, {lon} I'm {popularity:.2f} popular I'm open since {launchDate} and now I'm online = {online}!\n".format(lat = self.lat, lon = self.lon, online = self.online, popularity = self.popularity, launchDate = self.launchDate, name = self.name )