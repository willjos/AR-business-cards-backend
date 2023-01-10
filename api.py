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

@app.route("/", methods=['GET'])
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=pse.RealDictCursor)
    cur.execute("SELECT * FROM users")

    users_data = cur.fetchall()
    cur.close()

    return users_data

def query_database(query, search_param):
    conn = get_db_connection()
    with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
        try:
            cursor.execute(query, (search_param,))
            return cursor.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn:
                cursor.close()
    
@app.route("/getUserQR", methods=['GET'])
def getUserQR():
    args =  request.args
    if "userName" in args:
        userName = args["userName"]
        print(userName)
        qrCode  = query_database(
                """WITH userQR AS ( 
                    SELECT cards.user_id, 
                    cards.id, 
                    users.username 
                    FROM cards, users WHERE users.id=cards.user_id
                ) 
                SELECT id from userQR WHERE username=%s""", userName)
        print(qrCode)
        return jsonify(qrCode)
    else:
        return jsonify({status : 400, reason: "invalid"})
