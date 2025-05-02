from flask import Blueprint, request, jsonify, g # Import Blueprint, request, jsonify, g from flask.  
from ..utils.auth_utils import require_auth # This will add the require_auth function, cool: two levels deep
from ..db import get_connection # this will add the get_connection function

# blueprint = A blueprint is a template for generating a "section" of a web application.
# request = A method to GET, POST, PUT. Looking at the code below at the words: 'request'
# jsonify = returns json formatted information. Mostly errors with the error code.
# g = I guess it is a 'get' template, as it is connected to a .get method on line 21.
 
restaurants_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants') # new var, using the blueprint for, str, db name and url prefix.
 
# Routes for restaurant creation, listing, and reviews
# All endpoints require authentication and interact with the PostgreSQL database.

# Decorators
@restaurants_bp.post('/') # POST in the root level of the restaurants_bp, but only if:
@require_auth # Ensures the user must be logged in or authenticated to use the endpoint
# Create a new restaurant entry for the authenticated user.

# This function creates a new restaurant entry in the database.
def create():
    try:
        data = request.get_json() # Get the JSON body sent with the request
        name = data.get('name') # Try to get the restaurant name
        description = data.get('description', '') # Optional: get description or default to empty

        if not name:  # If there's no name, we can't go further
            return jsonify({'error': 'Restaurant name is required'}), 400

        user_id = g.get('user_id') # Grab user_id from the auth decorator (I guess somewhere from 'g' in flask)

        conn = get_connection() # Open a DB connection
        cur = conn.cursor() # Create a cursor to run SQL commands, need to read about cursor() class. It is for executing commands in the DB.

        # Add the new restaurant to the database
        cur.execute(
            "INSERT INTO restaurants (name, description, owner_id) VALUES (%s, %s, %s) RETURNING id",
            (name, description, user_id)
        )

        restaurant_id = cur.fetchone()[0] # Get the new ID from the RETURNING part
        conn.commit() # Commit the connection in the DB
        cur.close() # Close the cursor
        conn.close() # Close the DB connection

        # Return the new restaurant info with HTTP status 201 (Created)
        return jsonify({
            'id': restaurant_id,
            'name': name,
            'description': description,
            'owner_id': user_id,
        }), 201

    except Exception as e:  # Catch errors and return server message
        return jsonify({'error': 'Server error', 'details': str(e)}), 500


@restaurants_bp.get('/') # GET request to /
@require_auth
# Return a list of all restaurants with total reviews and average rating.
def get_restaurants():
    try:
        conn = get_connection() # starting a connection again and setting it to a var
        cur = conn.cursor() # adding the cursor() class to the connection
        # Single query with LEFT JOIN and GROUP BY | Dennis: not my comment
        # looks like a query, I see SELECT, FROM, etc. Execute is fetching restaurant information
        cur.execute("""
            SELECT 
                r.id,
                r.name,
                r.description,
                r.owner_id,
                COUNT(rv.id) AS total_reviews,
                COALESCE(ROUND(AVG(rv.rating)::numeric, 2), 0) AS average_rating
            FROM restaurants r
            LEFT JOIN reviews rv ON rv.restaurant_id = r.id
            GROUP BY r.id, r.name, r.description, r.owner_id
        """)
        rows = cur.fetchall() # fetch-all, means grab all (rows, as the var is called rows) from the connection.cursor (the executor class).
        restaurants = [] # make an empty list
        base_url = request.host_url.rstrip('/') # strip? change the base url with out the slash
        for row in rows:
            restaurant_id = row[0] # set id from row position 0.
            restaurants.append({ # insert new dict restaurant
                'id': restaurant_id,
                'name': row[1],
                'description': row[2],
                'owner_id': row[3],
                'total_reviews': row[4],
                'average_rating': float(row[5]),
                'reviews_url': f"{base_url}/restaurants/{restaurant_id}/reviews"
            })
            restaurants.sort(key=lambda x: x['id']) # looks inefficient to sort on each append. Maybe an indent, typo?
        cur.close() 
        conn.close()
        return jsonify(restaurants), 200 # return full JSON list
    except Exception as e:
        return jsonify({'error': 'Server error', 'details': str(e)}), 500 # error handler

    
@restaurants_bp.post('/<int:restaurant_id>/reviews') # POST request to / (integer)id/reviews
@require_auth
# Add a review to a restaurant by the authenticated user
def create_review(restaurant_id):
    try: # our friend try
        data = request.get_json()
        rating = data.get('rating')
        comment = data.get('comment', '')
        # check rating range between 1 to 5
        if not rating or not (1 <= int(rating) <= 5):
            return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400 # error handling
        
        user_id = g.get('user_id') # get user id
        conn = get_connection() # same same
        cur = conn.cursor() # same same same. :)
        
        # Optional: check if restaurant exists before inserting review | Dennis: not my comment
        cur.execute("SELECT id FROM restaurants WHERE id = %s", (restaurant_id,))
        restaurant = cur.fetchone()
        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404
        
        # Insert the review | Dennis: not my comment
        # looks like a query again to execute true the cursor connection
        cur.execute(
            """
            INSERT INTO reviews (user_id, restaurant_id, rating, comment) # db new row
            VALUES (%s, %s, %s, %s) # I googled, are placeholders to the row set above
            RETURNING id # return the id of the new insert?
            """,
            (user_id, restaurant_id, rating, comment)
        )
        review_id = cur.fetchone()[0] # save the id we got from the insert
        conn.commit() # save it, like git!
        cur.close() # close cursor
        conn.close() # close connection
        # return the newly created review in JSON with the 201 code
        return jsonify({
            'id': review_id,
            'restaurant_id': restaurant_id,
            'user_id': user_id,
            'rating': rating,
            'comment': comment
        }), 201
    except Exception as e: # catch them all as e, also nice.
        return jsonify({'error': 'Server error', 'details': str(e)}), 500 # error handler with details


# t. I get it now. GET restaurants reviews
@restaurants_bp.get('/<int:restaurant_id>/reviews') 
@require_auth
# Retrieve all reviews for a given restaurant
def get_reviews(restaurant_id):
    try:
        conn = get_connection() # same
        cur = conn.cursor() # same same with cursor() class
        # Optional: check if restaurant exists | Dennis: no my comment
        cur.execute("SELECT id, name FROM restaurants WHERE id = %s", (restaurant_id,))
        restaurant = cur.fetchone()
        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404
        
        # Fetch reviews and join with users table to get reviewer names | Dennis: not my comment
        cur.execute("""
            SELECT r.id, r.rating, r.comment, u.username
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.restaurant_id = %s
            ORDER BY r.id DESC
        """, (restaurant_id,))
        
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        reviews = [] # create empty review list
        for row in rows: # create the review information into a dict that is in a list
            reviews.append({
                'review_id': row[0],
                'rating': row[1],
                'comment': row[2],
                'reviewed_by': row[3]
            })
        # I know what I see, but cannot grasp the scope of it! :o
        return jsonify({ # returns it as Jason's SON. 
            'restaurant_id': restaurant[0], #
            'restaurant_name': restaurant[1],
            'total_reviews': len(reviews),
            'average_rating': sum([r['rating'] for r in reviews]) / len(reviews) if reviews else 0, 
            
            'reviews': reviews
        }), 200
    except Exception as e: # catching them errors again, with a 500! 
        return jsonify({'error': 'Server error', 'details': str(e)}), 500
