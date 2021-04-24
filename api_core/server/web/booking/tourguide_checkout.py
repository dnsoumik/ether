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
from datetime import timezone
import datetime


@xenSecureV1
class MtimeWebTourGuideCheckOutHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ('GET','POST','PUT','OPTIONS')

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
    tourGuideBook = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][37]['name']
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
            activityId = int(self.request.arguments['activityId'][0])
        except Exception as e:
            activityId = None

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
                    if app[0]['apiId'] in [ 402020, 402021, 402022]: # TODO: till here
                        if self.apiId == 402020:
                            if activityId in [0,1,8]:
                                bookInfoQ = self.touristSpotBook.find(
                                            {
                                                'touristId':self.profileId,
                                                '$where': 'this.activity[this.activity.length - 1].id =='+str(activityId)
                                            },
                                            {
                                                'id': 1,
                                                'time': 1,
                                                'activity': 1,
                                                'inventory': 1,
                                                'payment': 1,
                                                'bookType':1,
                                                'serviceAccountId':1,
                                                'touristId':1,
                                                'ticketId':1
                                            }
                                        )
                                bookInfo = []
                                async for i in bookInfoQ:
                                    bookInfo.append(i)
                                if len(bookInfo):
                                    for res in bookInfo:
                                        touristspotdetails = []
                                        touristSpotAccQ = self.serviceAccount.find(
                                                {
                                                    '_id':res['serviceAccountId']
                                                },
                                                {
                                                    '_id':0,
                                                    'basicInfo':1,
                                                    'serviceInfo':1,
                                                    'profileId':1
                                                }
                                            )
                                        touristSpotAcc = []
                                        async for i in touristSpotAccQ:
                                            touristSpotAcc.append(i)
                                        for info in touristSpotAcc:
                                            touristspotdetails.append(info)
                                            imgSample = {
                                                    "link": self.fu.serverUrl + "/uploads/imgmiss.png",
                                                    "mimeType": ".png",
                                                    "time": 1592151803174849
                                                }
                                            if len(info['basicInfo'][0]['image1']):
                                                for docx in info['basicInfo'][0]['image1']:
                                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) \
                                                        + '/service_account/' + str(info['profileId'])\
                                                        + '/img/' + str(docx['time']) + docx['mimeType']
                                            else:
                                                res['basicInfo'][0]['image1'].append(imgSample)
                                            del info['profileId']
                                        res['id'] = str(res['_id'])
                                        res['touristId'] = str(res['touristId'])
                                        del res['_id']
                                        del res['serviceAccountId']
                                        res['touristSpotDetails'] = touristspotdetails
                                        result.append(res)
                                    result.reverse()
                                    code = 2000
                                    status = True
                                else:
                                    code = 4550
                                    status = False
                                    message = "No Data Found"
                            else:
                                code = 4780
                                message = "Invalid argument - [activityId]"
                                raise Exception
                        elif self.apiId == 402021:
                            if activityId in [0,1,8]:
                                bookInfoQ = self.touristSpotBook.find(
                                            {
                                                'providerDetails.0.id':self.profileId,
                                                '$where': 'this.activity[this.activity.length - 1].id =='+str(activityId)
                                            }
                                        )
                                bookInfo = []
                                async for i in bookInfoQ:
                                    bookInfo.append(i)
                                if len(bookInfo):
                                    for res in bookInfo:
                                        v = {
                                                'id':str(res['_id']),
                                                'time':res['time'],
                                                'activity':res['activity'],
                                                'inventory':res['inventory'],
                                                'primaryTouristInfo':res['primaryTouristInfo'],
                                                'touristId':str(res['touristId']),
                                                'payment': res['payment'],
                                                'bookType':res['bookType'],
                                                'ticketId':res['ticketId']
                                            }
                                        result.append(v)
                                    result.reverse()
                                    code = 2000
                                    status = True
                                else:
                                    code = 4550
                                    status = False
                                    message = "No Data Found"
                            else:
                                code = 6550
                                status = False
                                message = "Invalid argument - [activityId]"
                                raise Exception
                        elif self.apiId == 402022:
                            if activityId in [0,1,8]:
                                bookInfoQ = self.touristSpotBook.find(
                                            {
                                                '$where': 'this.activity[this.activity.length - 1].id =='+str(activityId)
                                            }
                                        )
                                bookInfo = []
                                async for i in bookInfoQ:
                                    bookInfo.append(i)
                                if len(bookInfo):
                                    for res in bookInfo:
                                        v = {
                                                'id':str(res['_id']),
                                                'time':res['time'],
                                                'activity':res['activity'],
                                                'inventory':res['inventory'],
                                                'primaryTouristInfo':res['primaryTouristInfo'],
                                                'touristId':str(res['touristId']),
                                                'payment': res['payment'],
                                                'bookType':res['bookType'],
                                                'ticketId':res['ticketId']
                                            }
                                        touristspotdetails = []
                                        touristSpotAccQ = self.serviceAccount.find(
                                                {
                                                    '_id':res['serviceAccountId']
                                                },
                                                {
                                                    '_id':0,
                                                    'basicInfo':1,
                                                    'profileId':1
                                                }
                                            )
                                        touristSpotAcc = []
                                        async for i in touristSpotAccQ:
                                            touristSpotAcc.append(i)
                                        for info in touristSpotAcc:
                                            touristspotdetails.append(info)
                                            imgSample = {
                                                    "link": self.fu.serverUrl + "/uploads/imgmiss.png",
                                                    "mimeType": ".png",
                                                    "time": 1592151803174849
                                                }
                                            if len(info['basicInfo'][0]['image1']):
                                                for docx in info['basicInfo'][0]['image1']:
                                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) \
                                                        + '/service_account/' + str(info['profileId'])\
                                                        + '/img/' + str(docx['time']) + docx['mimeType']
                                            else:
                                                res['basicInfo'][0]['image1'].append(imgSample)
                                            del info['profileId']
                                        v['touristSpotDetails'] = touristspotdetails
                                        result.append(v)
                                    result.reverse()
                                    code = 2000
                                    status = True
                                else:
                                    code = 4550
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
                self.request.arguments = json.loads(self.request.body.decode())
            except Exception as e:
                Log.i(e)
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

                #Service Account Key for member classification
                #TODO Need to handle it properly
                try:
                    self.serviceAccountId = FN_DECRYPT(self.request.headers.get('service-Account-Key')).decode()
                    if not len(self.serviceAccountId):
                        raise Exception
                    else:
                        self.profileId = ObjectId(self.serviceAccountId)
                except Exception as e:
                    self.serviceAccountId = None


                if len(app):
                    self.apiId = app[0]['apiId']
                    if self.apiId in [ 402020, 402021]:
                        if self.apiId == 402021:
                            try:
                                if (self.request.arguments.get('id') == None):
                                    raise Exception
                                bookingId = ObjectId(self.request.arguments.get('id'))
                            except Exception as e:
                                code = 2738
                                status = False
                                message = "Invalid Booking Id"
                                raise Exception

                            bookingInfoQ = self.tourGuideBook.find(
                                        {
                                            '_id':bookingId
                                        }
                                    )
                            bookingInfo = []
                            async for i in bookingInfoQ:
                                bookingInfo.append(i)
                            if bookingInfo == []:
                                code = 4680
                                status = False
                                message = "Booking entry Not found."
                                raise Exception

                            sync = False
                            aTime = timeNow()
                            sync = self.request.arguments.get('sync')
                            if sync != None:
                                if type(sync) != bool:
                                    code = 2894
                                    status = False
                                    message = "Invalid argument - ['sync']"
                                    raise Exception
                                if sync == True:
                                    try:
                                        aTime = int(self.request.argument.get('time'))
                                    except:
                                        code = 8985
                                        status = False
                                        message = "Invalid argument - ['time']"
                                        raise Exception

                            bookingUpdate = await self.tourGuideBook.update_one(
                                        {
                                            '_id':bookingId
                                        },
                                        {
                                        '$set':{
                                                    'modifiedTime':timeNow(),
                                               },
                                        '$push':{
                                                    'activity': {
                                                                    'id':8,
                                                                    'time':aTime,
                                                                    'sync':sync
                                                                }
                                                }

                                            }
                                    )
                            code = 2000
                            status = True
                            message = "Check-out Process Complete"
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
