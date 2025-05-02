import base64 #Googled: decode API key for a user ID, sorry. Wanted to know.
from flask import Blueprint, request, jsonify # Cocaine line of tools: handling requests and mutch more
from ..db import get_connection # db connection
 
auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # blueprint for auth... but what. Not sure.
 
# route to register a new user
@auth_bp.post('/register') 
def register():
    try: # try 
        # GET a JSON body from request
        data = request.get_json() 
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        # Basic input validation | Dennis: not my comment
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        conn = get_connection()
        cur = conn.cursor()
        # Check if the email already exists | Dennis: not my comment
        cur.execute("SELECT id FROM users WHERE email = %s", (email,)) # Tuple. :D
        existing_user = cur.fetchone()
        if existing_user:
            cur.close()
            conn.close()
            return jsonify({'error': 'Email is already registered'}), 409 # error handler, conflict user is already married
        
        # Insert the new user | Dennis: not my comment
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING *",
            (username, email, password)
        )
        user = cur.fetchone() # return one row SQL request
        conn.commit() # git save it! 
        cur.close() # close the cursor.class
        conn.close() # close connection
        # return user information, but no password. Hmmm... basic info?
        return jsonify({
                'id': user[0],
                'username': user[1],
                'email': user[2]
                }), 201
    except Exception as e: # error handler and catch them all exception
        return jsonify({'error': str(e)}), 500
    
# route to log in a user and return API key
@auth_bp.post('/login')
def login():
    try: # TRY!
        data = request.get_json() # Request: email and password
        email = data.get('email')
        password = data.get('password')
        
        # Basic input validation | Dennis: not my comment
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        conn = get_connection()
        cur = conn.cursor()
        
        # Check for the user | Dennis: not my comment
        # get that Tuple party running again. This time we need no user, but their (email, password)
        cur.execute(
            "SELECT id, username FROM users WHERE email = %s AND password = %s",
            (email, password)
        )
        user = cur.fetchone() # return one row from the SQL request
        cur.close() # close that class
        conn.close() # close that connection
        print(user) # print that ab'user!
        
        if user:
            # ah, here we encode the API-KEY and return it in YSON'NY BOY.
            return jsonify({
               'X-API-Key': base64.b64encode(str(user[0]).encode()).decode()
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401 # error handler. Something's wong, mr Wabbit!
    except Exception as e:
        return jsonify({'error': 'Server error', 'details': str(e)}), 500 # Crash Bandicoot. 