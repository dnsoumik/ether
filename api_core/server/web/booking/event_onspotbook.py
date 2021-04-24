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
from datetime import timezone
from datetime import date
import datetime
import requests
import http.client
from baseconvert import base


@xenSecureV1
class MtimeWebEventOnSpotBookHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ('GET','POST','PUT')

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
                    if self.apiId in [ 402021, 402022]:
                        if self.apiId == 402021:
                            firstName = self.request.arguments.get('firstName')
                            code,message = Validate.i(
                                            firstName,
                                            'First Name',
                                            notEmpty = True,
                                            maxLength = 50,
                                            noSpecial = True,
                                            noNumber = True
                                            )
                            if code != 4100:
                                raise Exception
                            lastName = self.request.arguments.get('lastName')
                            code,message = Validate.i(
                                            lastName,
                                            'Last Name',
                                            notEmpty = True,
                                            maxLength = 50,
                                            noSpecial = True,
                                            noNumber = True
                                        )
                            if code != 4100:
                                raise Exception
                            phoneNumber = self.request.arguments.get('phoneNumber')
                            code,message = Validate.i(
                                            phoneNumber,
                                            'Phone Number',
                                            notEmpty = True,
                                            dataType = int,
                                            minNumber=1000000000,
                                            maxNumber=999999999999
                                        )
                            if code != 4100:
                                raise Exception

                            countryCode = self.request.arguments.get('countryCode')
                            if countryCode == None:
                                code = 4251
                                message = 'Missing Argument - [ countryCode ].'
                                raise Exception
                            elif type(countryCode) != int:
                                code = 4552
                                message = 'Invalid Argument - [ countryCode ].'
                                raise Exception
                            else:
                                countryCode = int(countryCode)

                            phoneNumber = int(str(countryCode) + str(phoneNumber))


                            email = self.request.arguments.get('email')
                            if email == None or email == "":
                                email = ""
                            else:
                                #if email != None or email != "":
                                code,message = Validate.i(
                                                    email,
                                                    'Email',
                                                    inputType='email',
                                                    maxLength = 50,
                                                )
                                if code != 4100:
                                    raise Exception


                            try:
                                numOfAdult = self.request.arguments.get('numOfAdult')
                                code, message = Validate.i(
                                        numOfAdult,
                                        'numOfAdult',
                                        dataType=int,
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ numOfAdult ].'
                                raise Exception

                            try:
                                numOfChild = self.request.arguments.get('numOfChild')
                                code, message = Validate.i(
                                        numOfChild,
                                        'numOfChild',
                                        dataType=int,
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ numOfChild ].'
                                raise Exception

                            try:
                                session = self.request.arguments.get('session')
                                code, message = Validate.i(
                                        session,
                                        'session',
                                        dataType=int,
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [session].'
                                raise Exception

                            adultInfo = self.request.arguments.get('adultInfo')
                            if adultInfo == None:
                                adultInfo = []
                            else:
                                if type(adultInfo) != list:
                                    code = 7873
                                    status = False
                                    message = "Invalid Argument - [adultInfo]"
                                    raise Exception
                                if len(adultInfo) != numOfAdult:
                                    code = 8493
                                    status = False
                                    message = "Invalid number of adults"
                                    raise Exception
                                try:
                                    for i in adultInfo:
                                        len(i['name'])
                                except:
                                    code = 7878
                                    status = False
                                    message = "Name is missing in adults"
                                    raise Exception
                            childrenInfo = self.request.arguments.get('childrenInfo')
                            if childrenInfo == None:
                                childrenInfo = []
                            else:
                                if type(adultInfo) != list:
                                    code = 7873
                                    status = False
                                    message = "Invalid Argument - [childrenInfo]"
                                    raise Exception
                                if len(childrenInfo) != numOfChild:
                                    code = 8493
                                    status = False
                                    message = "Invalid number of childrens"
                                    raise Exception
                                try:
                                    for i in childrenInfo:
                                        len(i['name'])
                                except:
                                    code = 7878
                                    status = False
                                    message = "Name is missing in children"
                                    raise Exception

                            try:
                                eventId = self.request.arguments.get('event')
                                try:
                                    eventId = ObjectId(eventId)
                                except:
                                    raise Exception
                            except:
                                code = 2494
                                status = False
                                message = "Invalid Event Id"
                                raise Exception


                            proFind = []
                            accFindQ = self.account.find(
                                        {
                                            'contact.0.value':phoneNumber,
                                        }
                                    )
                            accFind = []
                            async for i in accFindQ:
                                accFind.append(i)
                            if len(accFind):
                                proFindQ = self.profile.find(
                                        {
                                            'accountId':accFind[0]['_id'],
                                            'entityId': self.entityId,
                                            'applicationId': ObjectId('5e5611bcb0c34f3bb9c2cd36')
                                        },
                                        limit=1
                                    )
                                proFind = []
                                async for i in proFindQ:
                                    proFind.append(i)
                                if not len(proFind):
                                    code = 7873
                                    status = False
                                    message = "The number " + str(phoneNumber) + " is already registered as service provider."
                                    raise Exception
                                if len(proFind):
                                    primaryTouristId = proFind[0]['_id']
                                    accountData =   [{
                                                    'firstName': accFind[0]['firstName'],
                                                    'lastName': accFind[0]['lastName'],
                                                    'contact':  accFind[0]['contact']
                                                }]
                            else:
                                if len(email):
                                    emailValQ = self.account.find(
                                                {
                                                    'contact.1.value': email
                                                }
                                            )
                                    emailVal = []
                                    async for i in emailValQ:
                                        emailVal.append(i)
                                    if len(emailVal):
                                        if phoneNumber != emailVal[0]['contact'][0]['value']:
                                            code = 4655
                                            status = False
                                            message = "Email address already used for different number " \
                                                    + str(emailVal[0]['contact'][0]['value'])
                                            raise Exception
                                accountData =   [{
                                                    'firstName': firstName,
                                                    'lastName': lastName,
                                                    'contact':  [
                                                                    {
                                                                        'verified': False,
                                                                        'value': phoneNumber
                                                                    }
                                                                ]
                                                }]
                                if len(email):
                                    accountData[0]['contact'].append(
                                            {
                                                'verified': False,
                                                'value': email
                                            }
                                        )
                                try:
                                    if not len(accFind):
                                        accountId = await self.account.insert_one(accountData[0])
                                        accountId = str(accountId.inserted_id)
                                        Log.i(accountId, 'New Account Created!')
                                    else:
                                        accountId = str(accFind[0]['_id'])
                                except:
                                    code = 5830
                                    status = False
                                    message = 'Internal Error Please Contact the Support Team.'
                                    raise Exception
                                try:
                                    if not len(proFind):
                                        primaryTouristId = await self.profile.insert_one(
                                            {
                                                'active': True,
                                                'locked': False,
                                                'closed': False,
                                                'entityId': self.entityId,
                                                'applicationId': ObjectId("5e5611bcb0c34f3bb9c2cd36"),
                                                'accountId': ObjectId(accountId),
                                                'data':[]
                                            }
                                        )
                                        primaryTouristId = str(primaryTouristId.inserted_id)
                                        Log.i(primaryTouristId, 'New Profile Created!')
                                    else:
                                        primaryTouristId = proFind[0]['_id']
                                except:
                                    code = 4560
                                    status = False
                                    message = "Internal Error. Please contact the Support Team"
                                    raise Exception
                            if True:
                                serAccQ = self.serviceResource.find(
                                        {
                                            'profileId':self.profileId,
                                            'serviceType':8,
                                            '_id':eventId
                                        },
                                        {
                                            '_id':1,
                                            'serviceInfo':1
                                        },
                                        limit = 1
                                    )
                                serAcc = []
                                async for i in serAccQ:
                                    serAcc.append(i)
                                if len(serAcc):
                                    serviceAccountId = serAcc[0]['_id']
                                    payment = (numOfAdult * serAcc[0]['serviceInfo'][0]['adultCharge']) \
                                        + (numOfChild * serAcc[0]['serviceInfo'][0]['childCharge'])
                                else:
                                    code = 2819
                                    status = False
                                    message = "Event Not Found"
                                    raise Exception
                                try:
                                    startTime = serAcc[0]['serviceInfo'][0]['sessions'][session]['startTime']
                                    endTime = serAcc[0]['serviceInfo'][0]['sessions'][session]['endTime']
                                    maxCapacity = serAcc[0]['serviceInfo'][0]['sessions'][session]['maxCapacity']
                                except:
                                    code = 9100
                                    status = False
                                    message = "Invalid Session"
                                    raise Exception

                            sync = False
                            bookTime = timeNow()
                            ticketId = base(bookTime, 10, 36, string=True)

                            sync = self.request.arguments.get('sync')
                            if sync != None:
                                if type(sync) != bool:
                                    code = 2894
                                    status = False
                                    message = "Invalid argument - ['sync']"
                                    raise Exception
                                if sync == True:
                                    try:
                                        bookTime = int(self.request.arguments.get('time'))
                                    except:
                                        code = 8985
                                        status = False
                                        message = "Invalid argument - ['time']"
                                        raise Exception
                                    ticketId = base(bookTime, 10, 36, string=True)


                            totalEntry = numOfAdult + numOfChild
                            bookTimeN = int(bookTime/1000000) + timeOffsetIST
                            st = datetime.datetime.fromtimestamp(bookTimeN).strftime('%Y-%m-%d')
                            dateList = list(st.split ("-"))
                            dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                            timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                            dayTimeStamp = int(timestamp * 1000000)
                            newBookTime = bookTimeN * 1000000
                            #newBookTime = (timestamp + startTime) * 1000000 #If required to add startTime to bookTime timestamp
                            sessionAvailabilityQ = self.bookingSession.find(
                                                    {
                                                        'serviceAccountId':serviceAccountId,
                                                        'dayTimeStamp':dayTimeStamp,
                                                        'startTime':startTime,
                                                        'endTime':endTime,
                                                    }
                                                )
                            sessionAvailability = []
                            async for i in sessionAvailabilityQ:
                                sessionAvailability.append(i)

                            if not len(sessionAvailability):
                                sessionInsert = await self.bookingSession.insert_one(
                                                    {
                                                        'serviceAccountId':serviceAccountId,
                                                        'dayTimeStamp':dayTimeStamp,
                                                        'startTime':startTime,
                                                        'endTime':endTime,
                                                        'maxCapacity': maxCapacity,
                                                        'availableCapacity':maxCapacity - totalEntry,
                                                        'preBook':totalEntry,
                                                        'confirmBook':totalEntry,
                                                        'serviceType':8
                                                    }
                                                )
                                sessionId = str(sessionInsert.inserted_id)
                            if len(sessionAvailability):
                                if sync == False:
                                    if sessionAvailability[0]['availableCapacity'] <= 0:
                                        code = 2568
                                        status = False
                                        message = "No booking slots are available"
                                        raise Exception
                                    if totalEntry > sessionAvailability[0]['availableCapacity']:
                                        code = 2567
                                        status = False
                                        message = "Total number of people exceeds the available Capacity"
                                        raise Exception
                                sessionId = str(sessionAvailability[0]['_id'])
                                sessionUpdate = await self.bookingSession.update_one(
                                                    {
                                                        'serviceAccountId':serviceAccountId,
                                                        'dayTimeStamp':dayTimeStamp,
                                                        'startTime':startTime,
                                                        'endTime':endTime,
                                                    },
                                                    {
                                                    '$set':{
                                                        'preBook': sessionAvailability[0]['preBook'] + totalEntry,
                                                        'availableCapacity': sessionAvailability[0]['availableCapacity'] - totalEntry,
                                                        'confirmBook': sessionAvailability[0]['confirmBook'] + totalEntry,
                                                    }
                                                }
                                        )
                            '''
                            else:
                                serAcc = yield self.serviceAccount.find(
                                        {
                                            'profileId':self.serviceAccountId,
                                            'serviceType':1
                                        },
                                        {
                                            'profileId':1
                                        },
                                        limit = 1
                                    )
                                if len(serAcc):
                                    serviceAccountId = serAcc[0]['_id']
                                    serviceProfileId = serAcc[0]['profileId']
                                else:
                                    code = 3555
                                    status = False
                                    message = "Service Account Not available"
                                    raise Exception
                                accFind = yield self.profile.find(
                                            {
                                                '_id':serviceProfileId
                                            },
                                            {
                                                'accountId':1
                                            },
                                            limit = 1
                                        )
                                if len(accFind):
                                    accountId = accFind[0]['accountId']
                                else:
                                    code = 3555
                                    status = False
                                    message = "Account Not available"
                                    raise Exception
                            Log.i('Primary Tourist Id - ', primaryTouristId)
                            # raise Exception
                            '''
                            try:
                                bookingId = await self.eventBook.insert_one(
                                        {
                                            'serviceAccountId':serviceAccountId,
                                            'bookingSession':ObjectId(sessionId),
                                            'serviceType':8,
                                            'primaryTouristInfo':accountData,
                                            'disabled':False,
                                            'providerDetails':[
                                                                {
                                                                    'id':self.profileId,
                                                                    'accountId':self.accountId
                                                                }
                                                            ],
                                            'time':bookTime,
                                            'modifiedTime':timeNow(),
                                            'activity' : [
                                                            {
                                                                "id":0,
                                                                "time":int(newBookTime),
                                                                "date":int(newBookTime),
                                                                "bookTime":int(newBookTime),
                                                                "startTime":startTime,
                                                                "endTime":endTime,
                                                                "sync":sync
                                                            },
                                                            {
                                                                "id":1,
                                                                "time":bookTime,
                                                                "sync":sync
                                                            }
                                                        ],
                                            "inventory": [
                                                            {
                                                                "numOfAdult": numOfAdult,
                                                                "numOfChild": numOfChild,
                                                                "adultInfo":adultInfo,
                                                                "childrenInfo":childrenInfo
                                                            }
                                                        ],
                                            'payment': [
                                                            {

                                                                'amount':payment,
                                                                'status':0,
                                                                'method':0,
                                                                'transacationId':'',
                                                                'transacationRef':''
                                                            }
                                                        ],
                                            'entityId' : self.entityId,
                                            'sendSmsCounter':0,
                                            'touristId':primaryTouristId,
                                            'bookType':1,
                                            'ticketId': ticketId
                                        }
                                    )
                            except:
                                code = 4566
                                status = False
                                message = "Unqiue Ticket ID could not be created. Try Again"
                                raise Exception
                            if True:
                                bookTime = int(bookTime / 1000000) + timeOffsetIST
                                bookedDay = datetime.datetime.fromtimestamp(bookTime).strftime('%d %B, %Y')

                                dayTimeStamp = dayTimeStamp /1000000
                                startTimeStamp = dayTimeStamp + startTime
                                endTimeStamp = dayTimeStamp + endTime

                                startTimeN = datetime.datetime.fromtimestamp(startTimeStamp).strftime('%I:%M %p')
                                endTimeN = datetime.datetime.fromtimestamp(endTimeStamp).strftime('%I:%M %p')

                                sessionTime = str(startTimeN) + ' - ' + str(endTimeN)

                                phoneNumber = str(phoneNumber - 910000000000)
                                Log.i("phoneNumber:",phoneNumber)
                                sms = 'ID for your ticket booked on {} at session {} is {}. Total People: {}. Ticket \
                                    cost: Rs{}.'.format(bookedDay,sessionTime,ticketId.upper(),totalEntry,payment)
                                Log.i("sms:",sms)
                                conn = http.client.HTTPSConnection("api.msg91.com")
                                payloadJson = {
                                            "sender":"SOCKET",
                                            "route":4,
                                            "country":91,
                                            "sms":[
                                                    {
                                                        "message":sms,
                                                        "to":[phoneNumber]
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
                                    message = "Ticket has been created and SMS notification has been sent"
                                    status = True
                                else:
                                    message = "Ticket has been created but the SMS notification could not be sent"
                                    status = True
                                    code = 4055
                            Log.i(ticketId)
                            v = {
                                    'bookingId':str(bookingId),
                                    'touristId':str(primaryTouristId)
                                }
                            result.append(v)
                            #code = 2000
                            #status = True
                            #message = "Primary Tourist is added and booking is initiated."
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

