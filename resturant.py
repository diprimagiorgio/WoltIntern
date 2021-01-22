class Resturant:

    distance = -1
    def __init__(self, lat, lon, online, populaty, openingDate):
        self.lat = lat
        self.lon = lon
        self.online = online
        self.populaty = populaty
        self.openingDate = openingDate
        

    def distance(self, lat, lon):
        distnce = foodistance(self.lat, self.lon, lat, lon)

    def foodistance(lat1, lon1, lat2, lon2):
        p = pi/180
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
        return 12742 * asin(sqrt(a)) #2*R*asin...
    