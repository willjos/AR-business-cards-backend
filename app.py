import psycopg2
import psycopg2.extras as pse
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import bcrypt 

app=Flask(__name__)
CORS(app)

def get_db_connection():
    try:
        conn = psycopg2.connect(f"dbname=zofajswl user=zofajswl password=OO3MCdBFbnGQvSRqgaa6a_AXoQ3OSwa3 host=rogue.db.elephantsql.com port=5432")
        return conn
    except:
        print('Error Connecting to Database')
# {os.getenv('DB_PASSWORD')}
# OO3MCdBFbnGQvSRqgaa6a_AXoQ3OSwa3
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
    message = None
    with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
        try:
            cursor.execute(query, search_param)
            conn.commit()
            message = "success"
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            message = error
        finally:
            if conn:
                cursor.close()
            return message
    
@app.route("/getUserQR", methods=['GET'])
def getUserQR():
    args =  request.args
    if "username" in args:
        user_name = args["username"]
        qr_code = query_database(
                """WITH userQR AS ( 
                    SELECT cards.user_id,
                    cards.title, 
                    cards.id, 
                    users.username 
                    FROM cards, users WHERE users.id=cards.user_id
                ) 
                SELECT id, title from userQR WHERE username=%s""", (user_name,))
        print(qr_code)
        if(qr_code == []):
            return "404, failed: user does not exist", 404 
        else:
            return jsonify(qr_code), 200
    else:
        return "404, failed: no username provided", 404

@app.route("/view-card/<int:id>", methods=['GET'])
def view_card(id):
    cur = conn.cursor(cursor_factory=pse.RealDictCursor)
    cur.execute("SELECT * FROM cards where id=(%s);", (id, ))
    card_data = cur.fetchall()
    cur.close()
    return card_data

@app.route("/create-card", methods=['POST'])
def create_card():
    data = request.json
    user_name = data['username']
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

@app.route("/edit-card", methods=['PATCH'])
def edit_card():
    data = request.json
    title = data['title']
    colour = data['colour']
    content = data['content']
    user_name = data['username']
    query = """
    UPDATE cards
    SET title = %s,
        colour = %s,
        content = %s
    WHERE user_id = (SELECT id FROM users WHERE username=%s);
    """
    parameters = (title, colour, content, user_name)
    try:
        insert_database(query, parameters)
        return 'edited card', 200
    except:
        return 'failed to edit card', 500

@app.route("/register-user", methods=['POST'])
def register_user():
    data = request.json
    user_name = data['username']
    password = data['password'].encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt).decode('utf-8')
    query = "INSERT INTO users(username, hashedpw) VALUES (%s, %s)"
    parameters = (user_name, hashed_password)
    msg = insert_database(query, parameters)
    if msg == "success":
        return 'User Registered', 200
    else:
        return "bad", 500 

@app.route("/login", methods=['POST'])
def login_user():
    data =  request.json
    user_name = data['username']
    password = data['password']
    query = "SELECT hashedpw FROM users WHERE username = %s"
    parameters = (user_name,)    
    user_data = query_database(query, parameters) 
    if(len(user_data) == 1):
        print(user_data)
        hashed_password = user_data[0]['hashedpw']
        print(hashed_password)
        if(bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))):
            return "success", 200
        else:
            return "Password Incorrect", 403
    else:
        return "username or password incorrect", 403