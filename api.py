import psycopg2
import psycopg2.extras as pse  # We'll need this to convert SQL responses into dictionaries
from flask import Flask, current_app, request, jsonify
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

def get_db_connection():
    try:
        conn = psycopg2.connect("dbname=zofajswl user=zofajswl password=OO3MCdBFbnGQvSRqgaa6a_AXoQ3OSwa3 host=rogue.db.elephantsql.com port=5432")
        return conn
    except:
        print('Error Connecting to Database')

conn = get_db_connection()

@app.route("/", methods=['GET'])
def index():

    cur = conn.cursor(cursor_factory=pse.RealDictCursor)
    cur.execute("SELECT * FROM users")

    users_data = cur.fetchall()
    cur.close()

    return users_data

@app.route("/view-card", methods=['GET'])
def view_card():

    args = request.args
    qr_code = args.get('qr')

    cur = conn.cursor(cursor_factory=pse.RealDictCursor)
    cur.execute("SELECT * FROM cards where id=%s", qr_code)

    card_data = cur.fetchall()
    cur.close()

    return card_data
