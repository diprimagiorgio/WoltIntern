from flask import Flask, jsonify, request, redirect
from json import load                                
from api.restaurant import Restaurant

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False #otherwise flask changes the sorting in the output

from api import test
from api import discovery