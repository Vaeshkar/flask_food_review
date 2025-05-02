import base64 #Googled: decode API key for a user ID, sorry. Wanted to know.
from functools import wraps # Makes lovely wraps to eat? Hehe. Googled: Preserves functions metadata when wrapping it
from flask import request, jsonify, g # oh no, not again. request data, send JSON and get or it stores user info
from ..db import get_connection # db connection from utils

# the function needed to auth
def require_auth(func):
    @wraps(func) # update wrapper function, lot of info in the DocString
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'You need to log in'}), 401 # error handler, missing key = no entry, NEXT!
        try: # yeehaa try!
            # Decode the Base64-encoded user ID | Dennis: not my comment
            decoded_id = base64.b64decode(api_key).decode() 
            user_id = int(decoded_id) # convert into integer
        except Exception: # except party
            return jsonify({'error': 'Invalid X-API-Key'}), 401 # error handler, invalid something...
        try:
            # Check if user exists in DB | Dennis: not my comment
            conn = get_connection() # my friends again
            cur = conn.cursor() # this one too.
            cur.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
            user = cur.fetchone() # Googled: cursor method, GET one row result from a SQL query, our Tuple in this case.
            cur.close() # close class
            conn.close() # close connection
            
            if not user:
                return jsonify({'error': 'Invalid user'}), 401 
                # error handler, jedi waves his hand: "not the user you are looking for."
            
            # Store user info in Flask's global context (g) | Dennis: not my comment
            # Get the global user data and unpackt it into the user tuple query forom the db. 
            # Line 24 is a cursor.execute with a tuple in the end. Explains the index undpacking.
            g.user_id = user[0]
            g.username = user[1]
            return func(*args, **kwargs) # run a function with our lovely args and kwargs
        except Exception as e: # except error with 500, Googled: Crash
            return jsonify({'error': 'Server error', 'details': str(e)}), 500
    return wrapper # return the function but wrapped, as I understand it with the auth included. 