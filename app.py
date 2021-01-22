from flask import Flask
from math import cos, asin, sqrt, pi
import json
app = Flask(__name__)
#export FLASK_ENV=development
#export FLASK_APP=app.py
# flask run

@app.route('/')
def comp():
#import all object from json and create the list
    with open("restaurants.json") as jsonFile:
        jsonResturants = json.load(jsonFile)        #return a dictionary
        jsonFile.close()

    # Iterating through the json 
    # list 
    myPrint = ""
    for i in jsonResturants["restaurants"]: 
        myPrint += i["name"] + "\n" 
    return myPrint

if __name__ == '__main__':
    app.run()
    

    
        
        
        
    
    #2 strategies or import all the file and create a List of object or import just near our location