import psycopg2
import psycopg2.extras as pse  # We'll need this to convert SQL responses into dictionaries
from flask import Flask, current_app, request, jsonify
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def index():
    return 'AR Business Cards Application'