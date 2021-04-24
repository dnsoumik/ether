#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .build_config import *


# Mongo Database Connection Class
class MongoMixin(object):
    # serviceDb = None

    '''
    try:
        #USER_DBPOOL = txmongo.MongoConnection(
        #        CONFIG['database'][0]['host'],
        #        CONFIG['database'][0]['port'],
        #    )
        #USER_DATABASE = getattr(USER_DBPOOL, CONFIG['database'][0]['key'])
        Log.i('MONGO', 'User Database Service has been Initialized!')
    except:
        Log.i('MONGO', 'User Database Service has been Initialization Failed!')

    '''

    # def initUserDb():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            CONFIG['database'][0]['host'],
            CONFIG['database'][0]['port'],
        )

        # options = {'async': True}
        # await client.fsync(**options)
        # MongoMixin.userDb = client[CONFIG['database'][0]['key']]

        userDb = client[CONFIG['database'][0]['key']]
        client = None
        # Log.i(userDb)

        Log.i('MONGO', 'User Database has been Initialized!')
    except:
        userDb = None
        Log.i('MONGO', 'User Database has been Initialization Failed!')

    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            CONFIG['database'][1]['host'],
            CONFIG['database'][1]['port'],
        )

        # options = {'async': True}
        # await client.fsync(**options)
        # MongoMixin.userDb = client[CONFIG['database'][0]['key']]

        serviceDb = client[CONFIG['database'][1]['key']]
        client = None
        # Log.i(userDb)

        Log.i('MONGO', 'Service Database has been Initialized!')
    except:
        userDb = None
        Log.i('MONGO', 'Service Database has been Initialization Failed!')


    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            CONFIG['database'][2]['host'],
            CONFIG['database'][2]['port'],
        )

        # options = {'async': True}
        # await client.fsync(**options)
        # MongoMixin.userDb = client[CONFIG['database'][0]['key']]

        reportDb = client[CONFIG['database'][2]['key']]
        client = None
        # Log.i(userDb)

        Log.i('MONGO', 'Report Database has been Initialized!')
    except:
        reportDb = None
        Log.i('MONGO', 'Report Database has been Initialization Failed!')


# Firebase Connection Class
class FirebaseMixin(object):
    # serviceDb = None

    fb = None
    try:
        TAG = 'Firebase'
        import firebase_admin
        from firebase_admin import credentials
        credPath = CONFIG['database'][4]['cred']

        cred = credentials.Certificate(credPath)
        fb = firebase_admin.initialize_app(cred)

        Log.i('Firebase', 'has been Initialized! {}'.format(fb.name))

        #client = motor.motor_asyncio.AsyncIOMotorClient(
        #    CONFIG['database'][1]['host'],
        #    CONFIG['database'][1]['port'],
        #)

    except Exception as e:
        fb = None
        Log.i('Firebase', 'has been Initialization Failed! {}'.format(e))

