import os
from eve import Eve

# AWS lambda, sensible DB connection settings are stored in environment variables.
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
#MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
#MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_DBNAME = 'EtherBase'

# AWS
api_settings = {
      'MONGO_HOST': MONGO_HOST,
      'MONGO_PORT': MONGO_PORT,
      #'MONGO_USERNAME' : MONGO_USERNAME,
      #'MONGO_PASSWORD' : MONGO_PASSWORD,
      'MONGO_DBNAME': MONGO_DBNAME,
      'RESOURCE_METHODS' : ['GET', 'POST', 'DELETE'],
      'ITEM_METHODS' : ['GET', 'PATCH', 'DELETE'],
      'EXTENDED_MEDIA_INFO' : ['content_type', 'name', 'length'],
      'RETURN_MEDIA_AS_BASE64_STRING' : False,
      'RETURN_MEDIA_AS_URL': True,
      'CACHE_CONTROL' : 'max-age=20',
      'CACHE_EXPIRES' : 20,
      'DOMAIN' : {
                    'people': {
                        'item_title': 'person',
                    #    'resource_methods': ['GET', 'POST'],
                    'item_methods': ['GET', 'PATCH','PUT', 'DELETE'],
                    'RESOURCE_METHODS' : ['GET', 'POST', 'DELETE'],
                    #'ITEM_METHODS' : ['GET', 'PATCH', 'DELETE'],
                  'additional_lookup':
                      {
                          'url': 'regex("[\w]+")',
                          'field': 'lastName'
                      },
                  'schema':
                      {
                          'firstName': {
                              'type': 'string',
                              'minlength': 1,
                              'maxlength': 10,
                              'required': True,
                              #'unique': True,
                          },
                          'lastName': {
                              'type': 'string',
                              'minlength': 1,
                              'maxlength': 15,
                              'required': True,
                              #'unique': True,
                          },
                      }
                  }
              }
}
app = Eve()
#app = Eve(settings=api_settings)
app.run()
