# Wolt Summer 2021 Internships

This is my solution for the [assignment](https://github.com/woltapp/summer2021-internship)

## Analysis
If n is equal to the number of restaurants in the JSON file My solution has a time complexity of O(n * log(n)), because after importing the restaurants in a list I use a function for sorting a space complexity of O(n) because I import the restaurants in a list, each restaurant has a space occupation θ(1), in the worst case all the restaurants are closer than 1.5 km, so I'm going to import all the restaurants in a list

## Requirements
All the packages needed are in the file  ```requirements.txt```.
```console
(env) user@user:~$ pip install -r requirements.txt  
```
## Discussion solution
I have defined a class ```Restaurant``` with all the properties necessaries to represent a restaurant. I have imported all the restaurants from the JSON file, that are closer than 1.5 Km, to create a List of object ```Restaurant```. I have sorted the list, with the proper value, and returned the best matching restaurants, according to the rules defined in the assignment.
To calculate the distance I have used the function distance.distance of the library [geopy](https://en.wikipedia.org/wiki/Geodesics_on_an_ellipsoid). And it currently uses the [geodisc distance](https://en.wikipedia.org/wiki/Geodesics_on_an_ellipsoid).
The coordinates received as input are validated before using it.
## Usage
 
Activate the virtual environment
```console
user@user:~/<path>/WoltIntern$ source "<path>/env/bin/activate" 
```
start the flask app
```console
(env) user@user:~/<path>/WoltIntern$ export FLASK_ENV=development; export FLASK_APP=api/__init__.py; flask run
```
Do a request. Visit the page [localhost:5000/discovery?lat=60.1709&lon=24.941](http://localhost:5000/discovery?lat=60.1709&lon=24.941)

## Test
There is a test function that can generate some random coordinates, near one of the restaurants, between 1.5km to 3km far away from the restaurant. The result list can be empty. 
[localhost:5000/testRandomPoint](http://localhost:5000/testRandomPoint) 
