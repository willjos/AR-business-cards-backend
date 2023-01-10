import psycopg2
import psycopg2.extras as pse  # We'll need this to convert SQL responses into dictionaries
from flask import Flask, current_app, request, jsonify
from flask_cors import CORS
import bcrypt
from dotenv import load_dotenv
import os


app=Flask(__name__)
CORS(app)

def configure():
    load_dotenv()

configure()

def get_db_connection():
    try:
        conn = psycopg2.connect(f"dbname=zofajswl user=zofajswl password={os.getenv('db_password')} host=rogue.db.elephantsql.com port=5432")
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

def query_database(query, search_param):
    with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
        try:
            cursor.execute(query, search_param)
            return cursor.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn:
                cursor.close()

def insert_database(query, search_param):
    with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
        try:
            cursor.execute(query, search_param)
            conn.commit()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn:
                cursor.close()
    
@app.route("/getUserQR", methods=['GET'])
def getUserQR():
    args =  request.args
    if "username" in args:
        user_name = args["username"]
        qr_code = query_database(
                """WITH userQR AS ( 
                    SELECT cards.user_id, 
                    cards.id, 
                    users.username 
                    FROM cards, users WHERE users.id=cards.user_id
                ) 
                SELECT id from userQR WHERE username=%s""", (user_name,))
        if(qr_code == []):
            return "404, failed: user does not exist", 404 
        else:
            return jsonify(qr_code), 200
    else:
        return "404, failed: no username provided", 404

@app.route("/view-card", methods=['GET'])
def view_card():

    args = request.args
    qr_code = args.get('qr')

    cur = conn.cursor(cursor_factory=pse.RealDictCursor)
    cur.execute("SELECT * FROM cards where id=%s", qr_code)

    card_data = cur.fetchall()
    cur.close()

    return card_data

@app.route("/create-card", methods=['POST'])
def create_card():
    data = request.json
    user_name = data['userName']
    title = data['title']
    colour = data['colour']
    content = data['content']
    query = """
    INSERT INTO cards(user_id, title, colour, content)
    VALUES ((SELECT id FROM users WHERE username=%s), %s, %s, %s);"""
    parameters = (user_name, title, colour, content)
    try:
        insert_database(query, parameters)
        return 'added card', 200
    except:
        return 'failed to add card', 500

@app.route("/register-user", methods=['POST'])
def register_user():
    data = request.json
    user_name = data['userName']
    password = data['password']

    query = "INSERT INTO users(username, hashedpw) VALUES (%s, %s)"
    parameters = (user_name, password)
    try:
        insert_database(query, parameters)
        return 'User Registered', 200
    except:
        return 'Failed to Register user', 500

@app.route("/login", methods=['POST'])
def login_user():
    data =  request.json
    user_name = data['username']
    password = data['password']
    
    query = "SELECT * FROM users WHERE username = %s AND hashedpw = %s"
    parameters = (user_name, password)    
    
    user_data = query_database(query, parameters)
    if(len(user_data)>= 1):
        return "success", 200
        #do something
    else:
        return "username or password incorrect", 40
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)