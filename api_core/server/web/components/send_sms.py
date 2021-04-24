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
class MtimeWebSendSMSHandler(tornado.web.RequestHandler,
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
            availablityTime = int(self.request.arguments['availabilityTime'][0])
        except:
            availablityTime = None

        try:
            session = int(self.request.arguments['session'][0])
        except:
            session = None
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
                    if app[0]['apiId'] in [ 402020, 402021, 402022]: # TODO: till here
                        if self.apiId == 402020:
                            try:
                                bookingId = self.request.arguments['bookingId'][0].decode()
                            except:
                                bookingId = None
                            if bookingId:
                                bookInfoQ = self.touristSpotBook.find(
                                            {
                                                'touristId':self.profileId,
                                                '_id':ObjectId(bookingId)
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
                            else:
                                if activityId in [0,1,2,5,8]:
                                    if activityId == 0:
                                        activityId = 1
                                        query = 'this.activity[this.activity.length - 1].id <='+str(activityId)
                                    else:
                                        query = 'this.activity[this.activity.length - 1].id =='+str(activityId)
                                    bookInfoQ = self.touristSpotBook.find(
                                            {
                                                'touristId':self.profileId,
                                                '$where': query
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
                                else:
                                    code = 4780
                                    message = "Invalid argument - [activityId]"
                                    raise Exception
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
                                                        'profileId':1,
                                                        'paymentInfo':1
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
                        elif self.apiId == 402021:
                            if self.serviceAccountId == None:
                                self.profileId = profile[0]['_id']
                            else:
                                self.profileId = self.serviceAccountId
                            if activityId in [0,1,2,5,8]:
                                if activityId == 0:
                                    activityId = 1
                                    query = 'this.activity[this.activity.length - 1].id <='+str(activityId)
                                else:
                                    query = 'this.activity[this.activity.length - 1].id =='+str(activityId)
                                bookInfo = []
                                bookInfoQ = self.touristSpotBook.find(
                                            {
                                                'providerDetails.0.id':self.profileId,
                                                '$where': query
                                            }
                                        )
                                async for i in bookInfoQ:
                                    bookInfo.append(i)
                                Log.i('booklen',len(bookInfo))
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
                                        if res['primaryTouristInfo'][0].get('_id') != None:
                                            del res['primaryTouristInfo'][0]['_id']
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
                            if activityId in [0,1,2,5,8]:
                                if activityId == 0:
                                    activityId = 1
                                    query = 'this.activity[this.activity.length - 1].id <='+str(activityId)
                                else:
                                    query = 'this.activity[this.activity.length - 1].id =='+str(activityId)
                                bookInfoQ = self.touristSpotBook.find(
                                            {
                                                '$where': query
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
                                        if res['primaryTouristInfo'][0].get('_id') != None:
                                            del res['primaryTouristInfo'][0]['_id']
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
                            serviceType = self.request.arguments.get('serviceType')
                            if serviceType == None:
                                code = 8942
                                status = False
                                message = "Missing argument - ['serviceType']"
                                raise Exception
                            if type(serviceType) != int and serviceType not in [0,1,2,3,4,5,6]:
                                code = 8942
                                status = False
                                message = "Invalid argument - ['serviceType']"
                                raise Exception

                            smsMessage = self.request.arguments.get('smsMessage')
                            if smsMessage == None or smsMessage == "":
                                code = 4999
                                status = False
                                message = "Please enter the message"
                                raise Exception

                            contacts = []
                            if serviceType == 0:
                                touristAppQ = self.applications.find(
                                                {
                                                    'apiId':402020
                                                }
                                            )
                                touristApp = []
                                async for i in touristAppQ:
                                    touristApp.append(i)
                                if not len(touristApp):
                                    code = 8942
                                    status = False
                                    message = "Internal Error in sending SMS. Please contact Support"
                                    raise Exception
                                touristProfileFindQ = self.profile.find(
                                                {
                                                    'applicationId':touristApp[0]['_id'],
                                                    'entityId':self.entityId
                                                }
                                            )
                                touristProfileFind = []
                                async for i in touristProfileFindQ:
                                    touristProfileFind.append(i)
                                if len(touristProfileFind):
                                    for res in touristProfileFind:
                                        accFindQ = self.account.find(
                                                {
                                                    '_id':res['accountId']
                                                }
                                            )
                                        accFind = []
                                        async for i in accFindQ:
                                            accFind.append(i)
                                        if len(accFind):
                                            phoneNumber = str(accFind[0]['contact'][0]['value'] - 910000000000)
                                            Log.i("phoneNumber",phoneNumber)
                                            contacts.append(phoneNumber)
                            else:
                                serAccFindQ = self.serviceAccount.find(
                                            {
                                                'serviceType':serviceType,
                                                'verified': False
                                            }
                                        )
                                serAccFind = []
                                async for i in serAccFindQ:
                                    serAccFind.append(i)

                                if len(serAccFind):
                                    for res in serAccFind:
                                        proFindQ = self.profile.find(
                                                {
                                                    '_id':res['profileId'],
                                                    'entityId':self.entityId
                                                }
                                            )
                                        proFind = []
                                        async for i in proFindQ:
                                            proFind.append(i)
                                        if len(proFind):
                                            accFindQ = self.account.find(
                                                    {
                                                        '_id':proFind[0]['accountId']
                                                    }
                                                )
                                            accFind = []
                                            async for i in accFindQ:
                                                accFind.append(i)
                                            if len(accFind):
                                                try:
                                                    Log.i("propertName",res['propertyInfo'][0]['propertyName'])
                                                except:
                                                    Log.i("Property Name Not Found")
                                                phoneNumber = str(accFind[0]['contact'][0]['value'] - 910000000000)
                                                Log.i("phoneNumber",phoneNumber)
                                                contacts.append(phoneNumber)
                            if len(contacts):
                                conn = http.client.HTTPSConnection("api.msg91.com")
                                payloadJson = {
                                            "sender":"SOCKET",
                                            "route":4,
                                            "country":91,
                                            "sms":[
                                                    {
                                                        "message":smsMessage,
                                                        "to":contacts
                                                    }
                                                ]
                                            }
                                payload = json.dumps(payloadJson)
                                headers = {
                                        'authkey': MSG91_GW_ID,
                                        'content-type': "application/json"
                                    }
                                conn.request("POST", "/api/v2/sendsms", payload, headers)
                                res = conn.getresponse()
                                data = res.read()
                                stat = json.loads(data.decode("utf-8"))
                                Log.i('Notification Status',stat['type'])
                                if stat['type'] == "success":
                                    code = 2000
                                    message = "SMS Message has been successfully sent"
                                    status = True
                                else:
                                    message = "SMS Message could not be sent"
                                    status = False
                                    code = 4055
                            else:
                                code = 8932
                                status = False
                                message  = "No contacts found to send SMS"
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
