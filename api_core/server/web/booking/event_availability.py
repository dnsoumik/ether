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
class MtimeWebEventAvailablityHandler(tornado.web.RequestHandler,
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
    eventBook = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][45]['name']
                ]
    serviceResource = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][46]['name']
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
                    if app[0]['apiId'] in [ 402020, 402021, 402022]: # TODO: till here
                        if self.apiId == 402020:
                            try:
                                eventId = ObjectId(self.request.arguments['id'][0].decode())
                            except:
                                code = 7378
                                status = False
                                message = "Invalid Event"
                                raise Exception


                            eventFindQ = self.serviceResource.find(
                                            {
                                                '_id':eventId,
                                                'serviceType':8
                                            }
                                        )
                            eventFind = []
                            async for i in eventFindQ:
                                eventFind.append(i)

                            if not len(eventFind):
                                code = 4004
                                status = False
                                message = "Event Not Found"
                                raise Exception

                            try:
                                availablityTime = eventFind[0]['serviceInfo'][0]['startDate']
                            except:
                                code = 3444
                                status = False
                                message = "Event Date Not Found"
                                raise Exception

                            try:
                                session = int(self.request.arguments['session'][0])
                            except:
                                code = 7378
                                status = False
                                message = "Invalid session"
                                raise Exception

                            if True:
                                bookTimeN = int(availablityTime/1000000) + timeOffsetIST
                                st = datetime.datetime.fromtimestamp(bookTimeN).strftime('%Y-%m-%d')
                                dateList = list(st.split ("-"))
                                dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                                dayTimeStamp = int(timestamp * 1000000)
                                Log.i(availablityTime)
                                Log.i(dateList)
                                Log.i(dayTimeStamp)

                                serviceSessionFindQ = self.serviceResource.find(
                                                    {
                                                        '_id':eventId,
                                                        'serviceType':8
                                                    }
                                                )

                                serviceSessionFind = []
                                async for i in serviceSessionFindQ:
                                    serviceSessionFind.append(i)



                                if len(serviceSessionFind):
                                    try:
                                        startTime = serviceSessionFind[0]['serviceInfo'][0]['sessions'][session]['startTime']
                                        endTime = serviceSessionFind[0]['serviceInfo'][0]['sessions'][session]['endTime']
                                        maxCapacity = serviceSessionFind[0]['serviceInfo'][0]['sessions'][session]['maxCapacity']
                                        adultCharge = serviceSessionFind[0]['serviceInfo'][0]['adultCharge']
                                        childCharge = serviceSessionFind[0]['serviceInfo'][0]['childCharge']
                                    except:
                                        code = 9100
                                        status = False
                                        message = "Invalid Session"
                                        raise Exception

                                sessionAvailabilityQ = self.bookingSession.find(
                                                    {
                                                        'serviceAccountId':eventId,
                                                        'dayTimeStamp':dayTimeStamp,
                                                        'startTime':startTime,
                                                        'endTime':endTime,
                                                    }
                                                )
                                sessionAvailability = []
                                async for i in sessionAvailabilityQ:
                                    sessionAvailability.append(i)

                                if len(sessionAvailability):
                                    if sessionAvailability[0]['availableCapacity'] == 0:
                                        code = 8322
                                        status = False
                                        message = "Booking is full. No Available tickets for this session"
                                        raise Exception
                                    v = {
                                            'availableCapacity':sessionAvailability[0]['availableCapacity'],
                                            'preBook':sessionAvailability[0]['preBook'],
                                            'confirmBook':sessionAvailability[0]['confirmBook'],
                                            'adultPayment':adultCharge,
                                            'childrenPayment':childCharge
                                        }
                                else:
                                    v = {
                                            'availableCapacity':serviceSessionFind[0]['serviceInfo'][0]['sessions'][session]['maxCapacity'],
                                            'preBook':int(0),
                                            'confirmBook':int(0),
                                            'adultPayment':adultCharge,
                                            'childrenPayment':childCharge
                                        }
                                code = 2000
                                status = True
                                message = "Availability of Tickets"
                                result.append(v)
                        elif self.apiId == 402021:
                            try:
                                eventId = str(self.request.arguments['id']['0'].decode())
                                try:
                                    eventId = ObjectId(eventId)
                                except:
                                    raise Exception
                            except:
                                code = 3903
                                status = False
                                message = "Invalid Event Id"
                                raise Exception
                            eventFindQ = self.serviceResource.find(
                                            {
                                                '_id':eventId,
                                                'profileId':self.profileId,
                                                'serviceType':8
                                            }
                                        )
                            eventFind = []
                            async for i in eventFindQ:
                                eventFind.append(i)

                            if not len(eventFind):
                                code = 4004
                                status = False
                                message = "Event Not Found"
                                raise Exception

                            try:
                                availablityTime = eventFind[0]['sessionInfo'][0]['startDate']
                            except:
                                code = 3444
                                status = False
                                message = "Event Date Not Found"
                                raise Exception


                            try:
                                session = int(self.request.arguments['session'][0].decode())
                            except:
                                code = 7378
                                status = False
                                message = "Invalid session"
                                raise Exception

                            if True:
                                bookTimeN = int(availablityTime/1000000) + timeOffsetIST
                                st = datetime.datetime.fromtimestamp(bookTimeN).strftime('%Y-%m-%d')
                                dateList = list(st.split ("-"))
                                dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                                dayTimeStamp = int(timestamp * 1000000)
                                Log.i(availablityTime)
                                Log.i(dateList)
                                Log.i(dayTimeStamp)

                                serviceSessionFindQ = self.serviceResource.find(
                                                    {
                                                        'profileId':self.profileId,
                                                        'serviceType':8
                                                    }
                                                )

                                serviceSessionFind = []
                                async for i in serviceSessionFindQ:
                                    serviceSessionFind.append(i)


                                if not len(serviceSessionFind):
                                    code = 9299
                                    status = False
                                    message = "Event Not Found"
                                    raise Exception

                                if len(serviceSessionFind):
                                    try:
                                        startTime = serviceSessionFind[0]['serviceInfo'][0]['sessions'][session]['startTime']
                                        endTime = serviceSessionFind[0]['serviceInfo'][0]['sessions'][session]['endTime']
                                        maxCapacity = serviceSessionFind[0]['serviceInfo'][0]['sessions'][session]['maxCapacity']
                                        adultCharge = serviceSessionFind[0]['serviceInfo'][0]['adultCharge']
                                        childCharge = serviceSessionFind[0]['serviceInfo'][0]['childCharge']
                                    except:
                                        code = 9100
                                        status = False
                                        message = "Invalid Session"
                                        raise Exception

                                sessionAvailabilityQ = self.bookingSession.find(
                                                    {
                                                        'serviceAccountId':serviceSessionFind[0]['_id'],
                                                        'dayTimeStamp':dayTimeStamp,
                                                        'startTime':startTime,
                                                        'endTime':endTime,
                                                    }
                                                )
                                sessionAvailability = []
                                async for i in sessionAvailabilityQ:
                                    sessionAvailability.append(i)


                                if len(sessionAvailability):
                                    if sessionAvailability[0]['availableCapacity'] == 0:
                                        code = 8322
                                        status = False
                                        message = "Booking is full. No Available tickets for this session"
                                        raise Exception
                                    v = {
                                            'availableCapacity':sessionAvailability[0]['availableCapacity'],
                                            'preBook':sessionAvailability[0]['preBook'],
                                            'confirmBook':sessionAvailability[0]['confirmBook'],
                                            'adultPayment':adultCharge,
                                            'childrenPayment':childCharge
                                        }
                                else:
                                    v = {
                                            'availableCapacity':serviceSessionFind[0]['serviceInfo'][0]['sessions'][session]['maxCapacity'],
                                            'preBook':int(0),
                                            'confirmBook':int(0),
                                            'adultPayment':adultCharge,
                                            'childrenPayment':childCharge
                                        }
                                code = 2000
                                status = True
                                message = "Availability of Tickets"
                                result.append(v)
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

