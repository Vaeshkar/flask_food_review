import psycopg2
# It is an Python API adapter for working with PostgreSQL
from config import BaseConfig # grabbing the BaseConfig from the config.py
 
def get_connection(): 
    # making a little function to return a connected BaseConfig + URI that now can communicate via the imported API adapter for PostgreSQL
    return psycopg2.connect(BaseConfig.PG_URI)