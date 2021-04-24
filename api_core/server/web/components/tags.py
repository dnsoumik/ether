#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    1.  VtsVehicleHandler
        Type: Class
        Methods:
            A.GET:
                Get all vehicle  details under that entity
                Line: 39
            B.POST:
                Will create new row vehicles
                Line: 162
            C.PUT:
                Update Vehicle details on vehicles.
                Line: 335
            D:DELETE:
                Delete the Vehicle from Vehicles.
                Line: 523
'''

from __future__ import division
from ..lib.lib import *
from PIL import Image
#from datetime import timezone
#from datetime import date
#import datetime
import requests
import http.client


@xenSecureV1
class MtimeWebTagsHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ('GET','POST','PUT','OPTIONS','DELETE')

    account = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][0]['name']
                ]

    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]

    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]

    entity = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][5]['name']
                ]

    serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][0]['name']
                ]

    bookingCategory = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][1]['name']
                ]

    vehicle = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][4]['name']
                ]

    vehicleType = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][2]['name']
                ]

    booking = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][10]['name']
                ]

    coupon = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][11]['name']
                ]
    testBooking = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][12]['name']
                ]
    touristKyc = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][16]['name']
                ]
    subTourist = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][17]['name']
                ]
    imgWrite = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][18]['name']
                ]
    touristBook = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][19]['name']
                ]
    touristPass = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][20]['name']
                ]
    touristSpotBook = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][27]['name']
                ]
    bookingSession = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][28]['name']
                ]
    tags = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][31]['name']
                ]


    fu = FileUtil()
    def options(self):
        self.set_status(200)
        self.write({})
        self.finish()
        return

    async def get(self):

        status = False
        code = 4000
        result = []
        message = ''
        try:
            # TODO: this need to be moved in a global class
            profileQ = self.profile.find(
                            {
                                'closed': False,
                                'entityId': self.entityId,
                                'accountId': self.accountId,
                                'applicationId': self.applicationId
                            },
                            {
                                '_id': 1
                            },
                            limit=1
                        )
            profile = []
            async for i in profileQ:
                profile.append(i)
            if len(profile):
                try:
                    self.serviceAccountId = FN_DECRYPT(self.request.headers.get('service-Account-Key')).decode()
                    if not len(self.serviceAccountId):
                        raise Exception
                    self.serviceAccountId = ObjectId(self.serviceAccountId)
                except Exception as e:
                    self.serviceAccountId = None
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                appQ = self.applications.find(
                            {
                                '_id': self.applicationId
                            },
                            {
                                '_id': 0,
                                'apiId': 1
                            },
                            limit=1
                        )
                app = []
                async for i in appQ:
                    app.append(i)
                if len(app):
                    self.apiId = app[0]['apiId']
                    if app[0]['apiId'] in [ 402020, 402021, 402022, 402023]: # TODO: till here
                        if self.apiId == 402020:
                            code = 2000
                            status = True
                            message = "Tourist API not done"
                        elif self.apiId in [402022,402023]:
                            tagsFindQ = self.tags.find({"disabled":False})
                            tagsFind = []
                            async for i in tagsFindQ:
                                tagsFind.append(i)
                            for res in tagsFind:
                                v = {
                                        "id":str(res['_id']),
                                        "tagName":res['tagName'],
                                        "primary":res['primary'],
                                        "blocked":res['blocked'],
                                        "reference":res['reference']
                                    }
                                result.append(v)
                            if len(result):
                                result.reverse()
                                code = 2000
                                status = True
                                message = "List of tags"
                            else:
                                code = 4004
                                status = False
                                message = "No Data Found"
                        else:
                            code = 4003
                            self.set_status(401)
                            message = 'You are not authorized.'
                    else:
                        code = 4003
                        self.set_status(401)
                        message = 'You are not authorized.'
                else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not authorized.'
            else:
                code = 4003
                self.set_status(401)
                message = 'You are not authorized.'
        except Exception as e:
            status = False
            result = []
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.w('EXC', iMessage)
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            result = []
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return

    async def post(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:

            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments = json.loads(self.request.body.decode())
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
            # TODO: this need to be moved in a global class, from here
            profileQ = self.profile.find(
                            {
                                'closed': False,
                                'entityId': self.entityId,
                                'accountId': self.accountId,
                                'applicationId': self.applicationId
                            },
                            {
                                '_id': 1
                            },
                            limit=1
                        )
            profile = []
            async for i in profileQ:
                profile.append(i)
            if len(profile):
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                appQ = self.applications.find(
                            {
                                '_id': self.applicationId
                            },
                            {
                                '_id': 1,
                                'apiId': 1
                            },
                            limit=1
                        )
                app = []
                async for i in appQ:
                    app.append(i)
                if len(app):
                    self.apiId = app[0]['apiId']
                    if self.apiId in [ 402020, 402021, 402022]:
                        if self.apiId == 402022:
                            tagId = self.request.arguments.get('id')
                            if tagId == None:
                                tagName = self.request.arguments.get('tagName')
                                if tagName == None:
                                    code = 8329
                                    status = False
                                    message = "Please enter the tag"
                                    raise Exception
                                if len(str(tagName)) > 100:
                                    code = 7842
                                    status = False
                                    message = "Tag name cannot be more than 100 characters"
                                    raise Exception
                                tagName = tagName.lower()
                                try:
                                    tagsInsert = await self.tags.insert_one(
                                                {
                                                    'tagName':tagName.lower(),
                                                    'type':0,
                                                    'primary':True,
                                                    'entityId':self.entityId,
                                                    'profileId':self.profileId,
                                                    'applicationId':self.applicationId,
                                                    'blocked':False,
                                                    'disabled':False,
                                                    'verified':False,
                                                    'reference':0,
                                                    'location': [
                                                                    {
                                                                        'type': 'Point',
                                                                        'coordinates': []
                                                                    }
                                                                ],
                                                }
                                            )
                                    code = 2000
                                    status = True
                                    message = "Tag has been submitted"
                                except Exception as e:
                                    Log.i(str(e))
                                    if "duplicate" in str(e):
                                        code = 5600
                                        status = False
                                        message = "Tag name already exists"
                                        raise Exception
                                    else:
                                        code = 5600
                                        status = False
                                        message = "Internal Error in submitting tag. Please contact Support"
                                        raise Exception
                            else:
                                try:
                                    tagId = ObjectId(tagId)
                                except:
                                    code = 8938
                                    status = False
                                    message = "Invalid Tag Id"
                                    raise Exception
                                tagFindQ = self.tags.find(
                                                            {
                                                                '_id':tagId
                                                            }
                                                        )
                                tagFind = []
                                async for i in tagFindQ:
                                    tagFind.append(i)
                                if not len(tagFind):
                                    code = 9439
                                    status = False
                                    message = "Tag Not Found"
                                    raise Exception
                                if tagFind[0]['blocked'] == True:
                                    blocked = False
                                    blockedMessage = "Tag has been unblocked"
                                elif tagFind[0]['blocked'] == False:
                                    blocked = True
                                    blockedMessage = "Tag has been blocked"

                                tagUpdate = await self.tags.update_one(
                                        {
                                            '_id':tagId
                                        },
                                        {
                                            '$set':{
                                                        'blocked':blocked
                                                    }
                                        }
                                    )
                                if tagUpdate.modified_count != None:
                                    code = 2000
                                    status = True
                                    message = blockedMessage
                                else:
                                    code = 4500
                                    status = False
                                    message = "Internal Error in blocking/unblocking tag"
                                    raise Exception
                        else:
                            code = 4003
                            self.set_status(401)
                            message = 'You are not Authorized.'
                    else:
                        code = 4003
                        self.set_status(401)
                        message = 'You are not Authorized.'
                else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not Authorized.'

            else:
                code = 4003
                self.set_status(401)
                message = 'You are not Authorized.'
        except Exception as e:
            status = False
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return

    async def delete(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:


            # TODO: this need to be moved in a global class, from here
            profileQ = self.profile.find(
                            {
                                'closed': False,
                                'entityId': self.entityId,
                                'accountId': self.accountId,
                                'applicationId': self.applicationId
                            },
                            {
                                '_id': 1
                            },
                            limit=1
                        )
            profile = []
            async for i in profileQ:
                profile.append(i)
            if len(profile):
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                appQ = self.applications.find(
                            {
                                '_id': self.applicationId
                            },
                            {
                                '_id': 1,
                                'apiId': 1
                            },
                            limit=1
                        )
                app = []
                async for i in appQ:
                    app.append(i)
                if len(app):
                    self.apiId = app[0]['apiId']
                    if self.apiId in [ 402020, 402021, 402022]:
                        if self.apiId == 402022:
                            try:
                                tagId = self.request.arguments['id'][0].decode()
                            except:
                                code = 7483
                                status = False
                                message = "Missing Tag Id - ['id']"
                                raise Exception
                            try:
                                tagId = ObjectId(tagId)
                            except:
                                code = 7493
                                status = False
                                message = "Invalid Argument - ['id']"
                                raise Exception
                            tagFindQ = self.tags.find(
                                                            {
                                                                '_id':tagId
                                                            }
                                                        )
                            tagFind = []
                            async for i in tagFindQ:
                                tagFind.append(i)
                            if not len(tagFind):
                                code = 9439
                                status = False
                                message = "Tag Not Found"
                                raise Exception

                            tagDelete = await self.tags.delete_one(
                                        {
                                            '_id':tagId
                                        }
                                    )
                            code = 2000
                            status = True
                            message = "Tag has been deleted"
                        else:
                            code = 4003
                            self.set_status(401)
                            message = 'You are not Authorized.'
                    else:
                        code = 4003
                        self.set_status(401)
                        message = 'You are not Authorized.'
                else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not Authorized.'

            else:
                code = 4003
                self.set_status(401)
                message = 'You are not Authorized.'
        except Exception as e:
            status = False
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return

