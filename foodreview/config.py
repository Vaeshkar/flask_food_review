import os 
# import = is the gateway to a vast ecosystem of pre-written code that can save devs both time and effort.
# os = lets the user interact with the native OS Python that is currenty running. It is an easier way to interact with several os functions for day to day programming. Still no idea what is is, but reading on.getenv down there only means for me: get environment
 
class BaseConfig: # I think a base configuration class that saved a linked URI to this file.
    PG_URI = os.getenv('PG_URI') # this set a variable to the configured Uniform Resourse Identifier (URI) used to specify the connection details for a PostgresSQL Databas. 