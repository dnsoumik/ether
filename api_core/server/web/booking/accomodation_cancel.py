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
from datetime import date
import datetime
import pytz


@xenSecureV1
class MtimeWebAccomodationCancelHandler(tornado.web.RequestHandler,
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
                            try:
                                bookingId = str(self.request.arguments['id'][0].decode())
                                try:
                                    bookingId = ObjectId(bookingId)
                                except:
                                    raise Exception
                            except:
                                code = 4324
                                status = False
                                message = "Invalid Booking"
                                raise Exception
                            bookingFindQ = self.touristBook.find(
                                                {
                                                    '_id':bookingId,
                                                    'bookType':0,
                                                    'touristId':self.profileId,
                                                }
                                            )
                            bookingFind = []
                            async for i in bookingFindQ:
                                bookingFind.append(i)
                            if not len(bookingFind):
                                code = 7843
                                status = False
                                message = "Booking Not Found"
                                raise Exception
                            actLen = len(bookingFind[0]['activity'])
                            lastActivityCheck = bookingFind[0]['activity'][actLen - 1]['id']
                            if lastActivityCheck in [0, 21]:
                                code = 8043
                                status = False
                                message = "Invalid Booking. Refund cannot be issued"
                                raise Exception
                            elif lastActivityCheck in [1, 8]:
                                code = 8043
                                status = False
                                message = "No refund will be issued for Checked-In Booking"
                                raise Exception
                            elif lastActivityCheck == 3:
                                currentTime = timeNow()
                                checkInTime = bookingFind[0]['activity'][0]['startTime']

                                currentTimeN = int(currentTime/1000000)
                                st = datetime.datetime.fromtimestamp(currentTimeN).strftime('%Y-%m-%d')
                                dateList = list(st.split ("-"))

                                checkInTimeN = int(checkInTime/1000000)
                                et = datetime.datetime.fromtimestamp(checkInTimeN).strftime('%Y-%m-%d')
                                endList = list(et.split ("-"))

                                if True:
                                    d1 = date(int(dateList[0]), int(dateList[1]), int(dateList[2]))
                                    d2 = date(int(endList[0]), int(endList[1]), int(endList[2]))
                                    delta = d2 - d1
                                else:
                                    code = 7832
                                    status = False
                                    message = "Internal Error. Please contact Support"
                                    raise Exception

                                noOfDays = int(delta.days)
                                if noOfDays < 0:
                                    code = 9403
                                    status = False
                                    message = "Refund cannot be issued for booking after the Check-In Date"
                                    raise Exception
                                amountPaid = bookingFind[0]['payment'][0]['totalDue']
                                inventoryFindQ = self.inventory.find(
                                                    {
                                                        'serviceAccountId':bookingFind[0]['serviceAccountId'],
                                                        'serviceType':1
                                                    }
                                                )
                                inventoryFind = []
                                async for i in inventoryFindQ:
                                    inventoryFind.append(i)
                                try:
                                    refundPercentage = 0
                                    noOfHours = noOfDays * 24
                                    if noOfHours > (inventoryFind[0]['cancellation'][0]['period'] * 24):
                                        refundPercentage = 100
                                    elif noOfHours < (inventoryFind[0]['cancellation'][0]['period'] * 24) and noOfHours > (inventoryFind[0]['cancellation'][1]['period'] * 24):
                                        refundPercentage = inventoryFind[0]['cancellation'][1]['charge']
                                    elif noOfHours < (inventoryFind[0]['cancellation'][2]['period'] * 24):
                                        refundPercentage = 0
                                except:
                                    code = 5849
                                    status = False
                                    message = "Please contact Support to check on refund for this booking"
                                    raise Exception
                                if refundPercentage == 100:
                                    cancellationFee = 0
                                    refund = amountPaid
                                elif refundPercentage == 0:
                                    cancellationFee = amountPaid
                                    refund = 0
                                else:
                                    cancellationFee = amountPaid - ((refundPercentage/100) * amountPaid)
                                    refund = amountPaid - cancellationFee
                                v = {
                                        'amountPaid':amountPaid,
                                        'cancellationFee':round(cancellationFee,1),
                                        'refund':round(refund,1)
                                    }
                                result.append(v)
                                code = 2000
                                status = True
                                message = "Refund Information"
                            else:
                                code = 4994
                                status = False
                                message = "Invalid Booking. Please contact Support"
                                raise Exception
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
                    if self.apiId in [ 402020, 402021, 402022]:
                        if self.apiId == 402020:
                            try:
                                bookingId = str(self.request.arguments.get('id'))
                                try:
                                    bookingId = ObjectId(bookingId)
                                except:
                                    raise Exception
                            except:
                                code = 8493
                                status = False
                                message = "Invalid Booking Id"
                                raise Exception
                            touristBookFindQ = self.touristBook.find(
                                                {
                                                    '_id':bookingId,
                                                    'touristId':self.profileId
                                                }
                                            )
                            touristBookFind = []
                            async for i in touristBookFindQ:
                                touristBookFind.append(i)
                            if not len(touristBookFind):
                                code = 4932
                                status = False
                                message = "Booking Not Found"
                                raise Exception
                            bookUpdate = await self.touristBook.update_one(
                                                {
                                                    '_id':bookingId,
                                                    'touristId':self.profileId
                                                },
                                                {
                                                    '$push':{
                                                                'activity':{
                                                                                'id':40,
                                                                                'time':timeNow()
                                                                            }
                                                            }
                                                }
                                            )
                            if bookUpdate.modified_count != None:
                                code = 2000
                                status = True
                                message = "Cancellation request has been submitted"
                            else:
                                code = 4500
                                status = False
                                message = "Cancellation request could not be submitted. Please contact Support"
                                raise Exception
                        elif self.apiId == 402022:
                            try:
                                bookingId = str(self.request.arguments.get('id'))
                                try:
                                    bookingId = ObjectId(bookingId)
                                except:
                                    raise Exception
                            except:
                                code = 8493
                                status = False
                                message = "Invalid Booking Id"
                                raise Exception
                            try:
                                activityId = int(self.request.arguments.get('activityId'))
                            except:
                                code = 8493
                                status = False
                                message = "Invalid Activity Id"
                                raise Exception

                            touristBookFindQ = self.touristBook.find(
                                                {
                                                    '_id':bookingId,
                                                    'touristId':self.profileId
                                                }
                                            )
                            touristBookFind = []
                            async for i in touristBookFindQ:
                                touristBookFind.append(i)
                            if not len(touristBookFind):
                                code = 4932
                                status = False
                                message = "Booking Not Found"
                                raise Exception
                            bookUpdate = await self.touristBook.update_one(
                                                {
                                                    '_id':bookingId,
                                                    'touristId':self.profileId
                                                },
                                                {
                                                    '$push':{
                                                                'activity':{
                                                                                'id':activityId,
                                                                                'time':timeNow()
                                                                            }
                                                            }
                                                }
                                            )
                            if bookUpdate.modified_count != None:
                                code = 2000
                                status = True
                                message = "Cancellation request has been updated"
                            else:
                                code = 4500
                                status = False
                                message = "Cancellation request could not be updated. Please contact Support"
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

