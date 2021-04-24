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
class MtimeWebV2AccomodationPaymentHandler(tornado.web.RequestHandler,
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
    onlineTransaction = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][30]['name']
                ]
    inventory = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][39]['name']
                ]
    accSession = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][40]['name']
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
                            if True:
                                activityId = 3
                                bookInfoQ = self.touristBook.find(
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
                                                'touristDetails':1
                                            }
                                        )
                                bookInfo = []
                                async for i in bookInfoQ:
                                    bookInfo.append(i)
                                if len(bookInfo):
                                    for res in bookInfo:
                                        accomodationdetails = []
                                        accomodationAccQ = self.serviceAccount.find(
                                                {
                                                    '_id':res['serviceAccountId'],
                                                    'serviceType':1
                                                },
                                                {
                                                    '_id':0,
                                                    'hotelInfo':1,
                                                    'propertyInfo':1,
                                                }
                                            )
                                        accomodationAcc = []
                                        async for i in accomodationAccQ:
                                            accomodationAcc.append(i)
                                        res['id'] = str(res['_id'])
                                        res['touristId'] = str(res['touristId'])
                                        del res['serviceAccountId']
                                        del res['_id']
                                        res['AccomodationDetails'] = accomodationdetails
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
                            Log.i(bookingId)

                            bookingInfoQ = self.touristSpotBook.find(
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

                            '''
                            bookTimeN = int(bookingInfo[0]['activity'][0]['date']/1000000)
                            st = datetime.datetime.fromtimestamp(bookTimeN).strftime('%Y-%m-%d')
                            dateList = list(st.split ("-"))
                            dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                            timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                            dayTimeStamp = int(timestamp * 1000000)
                            '''
                            sessionId = bookingInfo[0]['bookingSession']
                            totalEntry = bookingInfo[0]['inventory'][0]['numOfAdult'] + bookingInfo[0]['inventory'][0]['numOfChild']

                            startTime = bookingInfo[0]['activity'][0]['startTime']
                            endTime = bookingInfo[0]['activity'][0]['endTime']

                            bookingUpdate = await self.touristSpotBook.update_one(
                                        {
                                            '_id':bookingId
                                        },
                                        {
                                        '$set':{
                                                    'modifiedTime':timeNow()
                                            },
                                        '$push':{
                                                    'activity': {
                                                                    'id':1,
                                                                    'time':aTime,
                                                                    'sync':sync
                                                                }
                                                }

                                            }
                                    )
                            if bookingUpdate.modified_count != None:
                                sessionAvailabilityQ = self.bookingSession.find(
                                                    {
                                                        'serviceAccountId':bookingInfo[0]['serviceAccountId'],
                                                        '_id':sessionId
                                                    }
                                                )
                                sessionAvailability = []
                                async for i in sessionAvailabilityQ:
                                    sessionAvailability.append(i)

                                if sessionAvailability == []:
                                    code = 7843
                                    status = False
                                    message = "Invalid Session"
                                    raise Exception

                                sessionUpdate = await self.bookingSession.update_one(
                                                    {
                                                        'serviceAccountId':bookingInfo[0]['serviceAccountId'],
                                                        '_id':sessionId
                                                    },
                                                    {
                                                    '$set':{
                                                        'availableCapacity': sessionAvailability[0]['availableCapacity'] - totalEntry,
                                                        'confirmBook': sessionAvailability[0]['confirmBook'] + totalEntry,
                                                    }
                                                }
                                        )
                                code = 2000
                                status = True
                                message = "Payment has been made"
                            else:
                                code = 8953
                                status = False
                                message = "Payment could not be made"
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

    async def put(self):

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
            Log.i(self.request.arguments)
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
                    if self.apiId in [ 402020, 402021]:
                        if self.apiId == 402020:
                            try:
                                if (self.request.arguments.get('bookingId') == None):
                                    raise Exception
                                bookingId = ObjectId(self.request.arguments.get('bookingId'))
                            except Exception as e:
                                code = 2738
                                status = False
                                message = "Invalid booking Id"
                                raise Exception
                            activityId = 0
                            bookingInfoQ = self.touristBook.find(
                                        {
                                            '_id':bookingId,
                                            'touristId':self.profileId
                                        }
                                    )
                            bookingInfo = []
                            async for i in bookingInfoQ:
                                bookingInfo.append(i)
                            if bookingInfo == []:
                                code = 4680
                                status = False
                                message = "Booking not found."
                                raise Exception
                            try:
                                sessionRange = bookingInfo[0]['sessionRange']
                            except:
                                sessionRange = []

                            try:
                                bookingActivityId = []
                                if len(bookingInfo[0]['activity']):
                                    for res in bookingInfo[0]['activity']:
                                        bookingActivityId.append(res['id'])
                                else:
                                    raise Exception
                            except:
                                code = 4902
                                status = False
                                message = "Invalid Booking"
                                raise Exception

                            if 3 in bookingActivityId:
                                code = 8302
                                status = False
                                message = "Payment has been already done for this booking"
                                raise Exception


                            #Find payment and numOfRoom
                            try:
                                payment = bookingInfo[0]['payment'][0]['totalDue']
                                numOfRoom = bookingInfo[0]['inventory'][0]['numOfRoom']
                                categoryId = bookingInfo[0]['inventory'][0]['categoryInfo'][0]['id']
                            except:
                                code = 4728
                                status = False
                                message = "Booking Not Found"
                                raise Exception

                            serAccQ = self.serviceAccount.find(
                                                        {
                                                            '_id':bookingInfo[0]['serviceAccountId'],
                                                            'serviceType':1
                                                        }
                                                    )
                            serAcc = []
                            async for i in serAccQ:
                                serAcc.append(i)
                            if not len(serAcc):
                                code = 2892
                                status = False
                                message = "Invalid Accomodation"
                                raise Exception

                            try:
                                sessionId = str(self.request.arguments.get('sessionId'))
                                try:
                                    sessionId = ObjectId(sessionId)
                                except:
                                    raise Exception
                            except Exception as e:
                                code = 2738
                                status = False
                                message = "Invalid session Id"
                                raise Exception



                            transactionId = self.request.arguments.get('txnId')
                            if transactionId == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [txnId]"
                                raise Exception

                            transactionRef = self.request.arguments.get('txnRef')
                            if transactionRef == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [txnRef]"
                                raise Exception

                            approvalRefNo = self.request.arguments.get('approvalRefNo')
                            if approvalRefNo == None:
                                approvalRefNo = ''

                            paymentMethod = self.request.arguments.get('paymentMethod')
                            if paymentMethod == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [paymentMethod]"
                                raise Exception
                            try:
                                paymentMethod = int(paymentMethod)
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - [paymentMethod]"
                                raise Exception

                            rawResponse = self.request.arguments.get('rawResponse')
                            if rawResponse == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [rawResponse]"
                                raise Exception

                            time = self.request.arguments.get('time')
                            if time == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [time]"
                                raise Exception
                            try:
                                time = int(time)
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - [time]"
                                raise Exception



                            responseStatus = self.request.arguments.get('status')
                            if responseStatus == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [status]"
                                raise Exception
                            try:
                                responseStatus = int(responseStatus)
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - [status]"
                                raise Exception

                            application = self.request.arguments.get('application')
                            if application == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [application]"
                                raise Exception

                            preferredOrder = self.request.arguments.get('preferredOrder')
                            if preferredOrder == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [preferredOrder]"
                                raise Exception
                            try:
                                preferredOrder = int(preferredOrder)
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - [preferredOrder]"
                                raise Exception

                            packageName = self.request.arguments.get('packageName')
                            if packageName == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [packageName]"
                                raise Exception

                            priority = self.request.arguments.get('priority')
                            if priority == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [priority]"
                                raise Exception
                            try:
                                priority = int(priority)
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - [priority]"
                                raise Exception

                            amount = self.request.arguments.get('amount')
                            if amount == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [amount]"
                                raise Exception
                            try:
                                amount = int(amount)
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - [amount]"
                                raise Exception

                            '''#Need to confirm
                            if amount < payment:
                                code = 6829
                                status = False
                                message = "Incorrect payment made. Actual payment is " + str(payment)
                                raise Exception
                            '''

                            receiverName = self.request.arguments.get('receiverName')
                            if receiverName == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [receiverName]"
                                raise Exception

                            receiverUpiAddress = self.request.arguments.get('receiverUpiAddress')
                            if receiverUpiAddress == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [receiverUpiAddress]"
                                raise Exception



                            bookingUpdate = await self.touristBook.update_one(
                                        {
                                            '_id':bookingId
                                        },
                                        {
                                        '$set':{
                                                    'expiredAt':None,
                                                    'modifiedTime':timeNow(),
                                                    'payment.0.transactionId':transactionId,
                                                    'payment.0.transactionRef': transactionRef,
                                                    'payment.0.responseStatus': responseStatus
                                                },
                                        '$push':{
                                                    'activity': {
                                                                    'id':3,
                                                                    'time':timeNow()
                                                                },
                                                },
                                        }
                                    )
                            if bookingUpdate.modified_count != None:
                                onlineTransactionInsert = await self.onlineTransaction.insert_one(
                                                                    {
                                                                        'senderId':self.profileId,
                                                                        'senderName':"",
                                                                        'senderUpiAddress':"",
                                                                        'receiverId':bookingInfo[0]['providerDetails'][0]['id'],
                                                                        'receiverName':receiverName,
                                                                        'receiverUpiAddress':receiverUpiAddress,
                                                                        'priority':priority,
                                                                        'packageName':packageName,
                                                                        'preferredOrder':preferredOrder,
                                                                        'application':application,
                                                                        'responseStatus':responseStatus,
                                                                        'time':time,
                                                                        'rawResponse':rawResponse,
                                                                        'paymentMethod':paymentMethod,
                                                                        'approvalRefNo':approvalRefNo,
                                                                        'serviceAccountId':bookingInfo[0]['serviceAccountId'],
                                                                        'serviceType':1,
                                                                        'bookingId':bookingId,
                                                                        'amount':amount,
                                                                        'txnId':transactionId,
                                                                        'txnRef':transactionRef
                                                                    }
                                                                )
                                code = 2000
                                status = True
                                message = "Payment has been made"
                                decValue = numOfRoom * -1
                                if len(sessionRange):
                                    for d in sessionRange:
                                        accSessionUpdate = await self.accSession.update_one(
                                                            {
                                                                'serviceType':1,
                                                                '_id':ObjectId(d),
                                                                'serviceAccountId':bookingInfo[0]['serviceAccountId'],
                                                                'inventoryInformation.id':categoryId
                                                            },
                                                            {
                                                                '$inc':{
                                                                            'inventoryInformation.$.confirmBook':numOfRoom,
                                                                            'inventoryInformation.$.availableQuantity':decValue
                                                                       }
                                                            }
                                                    )
                                else:
                                    accSessionUpdate = await self.accSession.update_one(
                                                            {
                                                                'serviceType':1,
                                                                '_id':sessionId,
                                                                'serviceAccountId':bookingInfo[0]['serviceAccountId'],
                                                                'inventoryInformation.id':categoryId
                                                            },
                                                            {
                                                                '$inc':{
                                                                            'inventoryInformation.$.confirmBook':numOfRoom,
                                                                            'inventoryInformation.$.availableQuantity':decValue
                                                                       }
                                                            }
                                                )
                            else:
                                code = 6872
                                status = False
                                message = "Payment could not be made. Please contact Support"
                                raise Exception
                        elif self.apiId == 402021:
                            try:
                                if (self.request.arguments.get('bookingId') == None):
                                    raise Exception
                                bookingId = ObjectId(self.request.arguments.get('bookingId'))
                            except Exception as e:
                                code = 2738
                                status = False
                                message = "Invalid booking Id"
                                raise Exception

                            try:
                                profileId = str(self.request.arguments.get('id'))
                                try:
                                    profileId = ObjectId(profileId)
                                except:
                                    raise Exception
                            except:
                                code = 9032
                                status = False
                                message = "Invalid Tourist Id"
                                raise Exception

                            activityId = 0
                            bookingInfoQ = self.touristBook.find(
                                        {
                                            '_id':bookingId,
                                            'touristId':profileId
                                        }
                                    )
                            bookingInfo = []
                            async for i in bookingInfoQ:
                                bookingInfo.append(i)
                            if bookingInfo == []:
                                code = 4680
                                status = False
                                message = "Booking not found."
                                raise Exception

                            try:
                                sessionRange = bookingInfo[0]['sessionRange']
                            except:
                                sessionRange = []

                            try:
                                bookingActivityId = []
                                if len(bookingInfo[0]['activity']):
                                    for res in bookingInfo[0]['activity']:
                                        bookingActivityId.append(res['id'])
                                else:
                                    raise Exception
                            except:
                                code = 4902
                                status = False
                                message = "Invalid Booking"
                                raise Exception

                            if 3 in bookingActivityId:
                                code = 8302
                                status = False
                                message = "Payment has been already done for this booking"
                                raise Exception


                            #Find payment and numOfRoom
                            try:
                                payment = bookingInfo[0]['payment'][0]['totalDue']
                                numOfRoom = bookingInfo[0]['inventory'][0]['numOfRoom']
                                categoryId = bookingInfo[0]['inventory'][0]['categoryInfo'][0]['id']
                            except:
                                code = 4728
                                status = False
                                message = "Booking Not Found"
                                raise Exception

                            serAccQ = self.serviceAccount.find(
                                                        {
                                                            '_id':bookingInfo[0]['serviceAccountId'],
                                                            'serviceType':1
                                                        }
                                                    )
                            serAcc = []
                            async for i in serAccQ:
                                serAcc.append(i)
                            if not len(serAcc):
                                code = 2892
                                status = False
                                message = "Invalid Accomodation"
                                raise Exception

                            try:
                                if (self.request.arguments.get('sessionId') == None):
                                    raise Exception
                                sessionId = ObjectId(self.request.arguments.get('sessionId'))
                            except Exception as e:
                                code = 2738
                                status = False
                                message = "Invalid session Id"
                                raise Exception



                            transactionId = self.request.arguments.get('txnId')
                            if transactionId == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [txnId]"
                                raise Exception

                            transactionRef = self.request.arguments.get('txnRef')
                            if transactionRef == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [txnRef]"
                                raise Exception

                            approvalRefNo = self.request.arguments.get('approvalRefNo')
                            if approvalRefNo == None:
                                approvalRefNo = ''

                            paymentMethod = self.request.arguments.get('paymentMethod')
                            if paymentMethod == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [paymentMethod]"
                                raise Exception
                            try:
                                paymentMethod = int(paymentMethod)
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - [paymentMethod]"
                                raise Exception

                            rawResponse = self.request.arguments.get('rawResponse')
                            if rawResponse == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [rawResponse]"
                                raise Exception

                            time = self.request.arguments.get('time')
                            if time == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [time]"
                                raise Exception
                            try:
                                time = int(time)
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - [time]"
                                raise Exception



                            responseStatus = self.request.arguments.get('status')
                            if responseStatus == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [status]"
                                raise Exception
                            try:
                                responseStatus = int(responseStatus)
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - [status]"
                                raise Exception

                            application = self.request.arguments.get('application')
                            if application == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [application]"
                                raise Exception

                            preferredOrder = self.request.arguments.get('preferredOrder')
                            if preferredOrder == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [preferredOrder]"
                                raise Exception
                            try:
                                preferredOrder = int(preferredOrder)
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - [preferredOrder]"
                                raise Exception

                            packageName = self.request.arguments.get('packageName')
                            if packageName == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [packageName]"
                                raise Exception

                            priority = self.request.arguments.get('priority')
                            if priority == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [priority]"
                                raise Exception
                            try:
                                priority = int(priority)
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - [priority]"
                                raise Exception

                            amount = self.request.arguments.get('amount')
                            if amount == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [amount]"
                                raise Exception
                            try:
                                amount = int(amount)
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - [amount]"
                                raise Exception

                            '''#Need to confirm
                            if amount < payment:
                                code = 6829
                                status = False
                                message = "Incorrect payment made. Actual payment is " + str(payment)
                                raise Exception
                            '''

                            receiverName = self.request.arguments.get('receiverName')
                            if receiverName == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [receiverName]"
                                raise Exception

                            receiverUpiAddress = self.request.arguments.get('receiverUpiAddress')
                            if receiverUpiAddress == None:
                                code = 9329
                                status = False
                                message = "Missing Argument - [receiverUpiAddress]"
                                raise Exception


                            bookingUpdate = await self.touristBook.update_one(
                                        {
                                            '_id':bookingId
                                        },
                                        {
                                        '$set':{
                                                    'modifiedTime':timeNow(),
                                                    'expiredAt':None,
                                                    'payment.0.transactionId':transactionId,
                                                    'payment.0.method':paymentMethod,
                                                    'payment.0.transactionRef': transactionRef,
                                                    'payment.0.responseStatus': responseStatus
                                                },
                                        '$push':{
                                                    'activity': {
                                                                    'id':3,
                                                                    'time':timeNow()
                                                                },
                                                },
                                        }
                                    )
                            if bookingUpdate.modified_count != None:
                                onlineTransactionInsert = await self.onlineTransaction.insert_one(
                                                                    {
                                                                        'senderId':self.profileId,
                                                                        'senderName':"",
                                                                        'senderUpiAddress':"",
                                                                        'receiverId':bookingInfo[0]['providerDetails'][0]['id'],
                                                                        'receiverName':receiverName,
                                                                        'receiverUpiAddress':receiverUpiAddress,
                                                                        'priority':priority,
                                                                        'packageName':packageName,
                                                                        'preferredOrder':preferredOrder,
                                                                        'application':application,
                                                                        'responseStatus':responseStatus,
                                                                        'time':time,
                                                                        'rawResponse':rawResponse,
                                                                        'paymentMethod':paymentMethod,
                                                                        'approvalRefNo':approvalRefNo,
                                                                        'serviceAccountId':bookingInfo[0]['serviceAccountId'],
                                                                        'serviceType':3,
                                                                        'bookingId':bookingId,
                                                                        'amount':amount,
                                                                        'txnId':transactionId,
                                                                        'txnRef':transactionRef
                                                                    }
                                                                )
                                code = 2000
                                status = True
                                message = "Payment has been made"
                                decValue = numOfRoom * -1
                                if len(sessionRange):
                                    for d in sessionRange:
                                        accSessionUpdate = await self.accSession.update_one(
                                                            {
                                                                'serviceType':1,
                                                                '_id':ObjectId(d),
                                                                'serviceAccountId':bookingInfo[0]['serviceAccountId'],
                                                                'inventoryInformation.id':categoryId
                                                            },
                                                            {
                                                                '$inc':{
                                                                            'inventoryInformation.$.confirmBook':numOfRoom,
                                                                            'inventoryInformation.$.availableQuantity':decValue
                                                                        }
                                                            }
                                                        )
                                else:
                                    accSessionUpdate = await self.accSession.update_one(
                                                            {
                                                                'serviceType':1,
                                                                '_id':sessionId,
                                                                'serviceAccountId':bookingInfo[0]['serviceAccountId'],
                                                                'inventoryInformation.id':categoryId
                                                            },
                                                            {
                                                                '$inc':{
                                                                            'inventoryInformation.$.confirmBook':numOfRoom,
                                                                            'inventoryInformation.$.availableQuantity':decValue
                                                                        }
                                                            }
                                                        )
                            else:
                                code = 6872
                                status = False
                                message = "Payment could not be made. Please contact Support"
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
