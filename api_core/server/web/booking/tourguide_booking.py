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
from baseconvert import base

@xenSecureV1
class MtimeWebTourGuideBookHandler(tornado.web.RequestHandler,
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
                    if self.apiId in [ 402020, 402021]:
                        if self.apiId == 402020:
                            tourGuideId = self.request.arguments.get('tourGuideId')
                            if tourGuideId == None:
                                code = 4560
                                status = False
                                message = "Tour Guide not selected."
                                raise Exception
                            try:
                                tourGuideId = ObjectId(tourGuideId)
                            except:
                                code = 4565
                                status = False
                                message = "Invalid Tour Guide ID"
                                raise Exception



                            tourGuideInfo = []
                            tourGuideInfoQ = self.serviceAccount.find(
                                        {
                                            '_id':tourGuideId,
                                            'serviceType':2
                                        }
                                    )
                            async for i in tourGuideInfoQ:
                                tourGuideInfo.append(i)

                            if not len(tourGuideInfo):
                                code = 7328
                                status = False
                                message = "Tour Guide Service Not Found"
                                raise Exception

                            if len(tourGuideInfo):
                                try:
                                    minHour = tourGuideInfo[0]['serviceInfo'][0]['minHour']
                                    halfDayCharge = tourGuideInfo[0]['serviceInfo'][0]['halfDayCharge']
                                    hourCharge = tourGuideInfo[0]['serviceInfo'][0]['hourCharge']
                                    extraHourRate = tourGuideInfo[0]['serviceInfo'][0]['extraHourRate']
                                    nightHaltCharge = tourGuideInfo[0]['serviceInfo'][0]['nightHaltCharge']
                                    fullDayCharge = tourGuideInfo[0]['serviceInfo'][0]['fullDayCharge']
                                except:
                                    code = 9100
                                    status = False
                                    message = "Invalid Service Charges"
                                    raise Exception


                            tourGuideProfile = tourGuideInfo[0]['profileId']

                            tourGuideAccQ = self.profile.find(
                                        {
                                            '_id':tourGuideProfile,
                                        }
                                    )
                            tourGuideAcc = []
                            async for i in tourGuideAccQ:
                                tourGuideAcc.append(i)

                            if tourGuideAcc == []:
                                code = 4680
                                status = False
                                message = "Tour Guide Not found."
                                raise Exception

                            tourGuideAccount = tourGuideAcc[0]['accountId']

                            try:
                                bookTime = int(self.request.arguments.get('bookTime'))
                                code, message = Validate.i(
                                        bookTime,
                                        'bookTime',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ bookTime ].'
                                raise Exception


                            try:
                                noOfHours = int(self.request.arguments.get('noOfHours'))
                                code, message = Validate.i(
                                        noOfHours,
                                        'No of Hours',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ noOfHours ].'
                                raise Exception

                            if noOfHours == 0 or noOfHours > 24:
                                code = 3279
                                status = False
                                message = "Booking Hours cannot be zero or greater than 24"
                                raise Exception


                            if minHour > noOfHours:
                                code = 2982
                                status = False
                                message = "No of hours lesser than the Tour Guide's minimum hours count"
                                raise Exception


                            if noOfHours == 12:
                                payment = halfDayCharge
                            elif noOfHours == 24:
                                payment = fullDayCharge
                            else:
                                payment = noOfHours * hourCharge



                            nightHalt= self.request.arguments.get('nightHalt')
                            if nightHalt == None:
                                nightHalt = False
                            if type(nightHalt) != bool:
                                code = 8932
                                status = False
                                message = "Invalid Argument - ['nightHalt']"
                                raise Exception

                            if nightHalt == True:
                                payment = payment + nightHaltCharge


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
                            adultInfo = self.request.arguments.get('adultInfo')
                            if adultInfo == None:
                                adultInfo = []
                            else:
                                if type(adultInfo) != list:
                                    code = 7873
                                    status = False
                                    message = "Invalid Argument - [adultInfo]"
                                    raise Exception
                                if len(adultInfo) > numOfAdult:
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
                                if len(childrenInfo) > numOfChild:
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
                            currentTime = timeNow()
                            if (((bookTime/1000000)) < ((currentTime/1000000))):
                                code = 4770
                                status = False
                                message = "Booking date cannot be older than current date."
                                raise Exception

                            totalEntry = numOfAdult + numOfChild

                            bookTimeN = int(bookTime/1000000) + timeOffsetIST
                            st = datetime.datetime.fromtimestamp(bookTimeN).strftime('%Y-%m-%d')
                            dateList = list(st.split ("-"))
                            dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                            timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                            dayTimeStamp = int(timestamp * 1000000)
                            #newBookTime = (timestamp + startTime) * 1000000 # if required to add starttime to booking time.
                            newBookTime = int(bookTimeN * 1000000)



                            sessionAvailabilityQ = self.bookingSession.find(
                                                    {
                                                        'serviceAccountId':tourGuideId,
                                                        'dayTimeStamp':dayTimeStamp,
                                                        'serviceType':2
                                                    }
                                                )
                            sessionAvailability = []
                            async for i in sessionAvailabilityQ:
                                sessionAvailability.append(i)

                            if not len(sessionAvailability):
                                sessionInsert = await self.bookingSession.insert_one(
                                                    {
                                                        'serviceAccountId':tourGuideId,
                                                        'dayTimeStamp':dayTimeStamp,
                                                        'preBook':totalEntry,
                                                        'confirmBook':0,
                                                        'serviceType':2
                                                    }
                                                )
                                sessionId = str(sessionInsert.inserted_id)
                            if len(sessionAvailability):
                                code = 2567
                                status = False
                                message = "Tour Guide is already booked for this day"
                                raise Exception

                            accountData = []
                            accInfoQ = self.account.find(
                                                {
                                                    '_id':self.accountId
                                                }
                                            )
                            accInfo = []
                            async for i in accInfoQ:
                                accInfo.append(i)
                            if not len(accInfo):
                                code = 5600
                                status = False
                                message = "Account Not Found"
                                raise Exception
                            if len(accInfo):
                                v = {
                                        'firstName': accInfo[0]['firstName'],
                                        'lastName': accInfo[0]['lastName'],
                                        'contact':  accInfo[0]['contact']
                                    }
                            accountData.append(v)

                            #Converting base 10 timestamp to base 36 to get ticket ID with ASCII letters
                            ticketId = base(currentTime, 10, 36, string=True)
                            bookingId = await self.tourGuideBook.insert_one(
                                        {
                                            'ticketId':ticketId,
                                            'serviceAccountId':tourGuideId,
                                            'bookingSession':ObjectId(sessionId),
                                            'serviceType':2,
                                            'primaryTouristInfo':accountData,
                                            'modifiedTime':timeNow(),
                                            'disabled':False,
                                            'providerDetails':[
                                                                {
                                                                    'id':tourGuideProfile,
                                                                    'accountId':tourGuideAccount
                                                                }
                                                            ],
                                            'time':currentTime,
                                            'activity' : [
                                                            {
                                                                "id":0,
                                                                "time":currentTime,
                                                                #"date":bookTime,
                                                                #"bookTime":bookTime,
                                                                "date":int(newBookTime),
                                                                "bookTime":int(newBookTime),
                                                            }
                                                        ],
                                            "inventory": [
                                                            {
                                                                "numOfAdult": numOfAdult,
                                                                "numOfChild": numOfChild,
                                                                "adultInfo":adultInfo,
                                                                "childrenInfo":childrenInfo,
                                                            }
                                                        ],
                                            'extraChargeInfo':[
                                                            {
                                                                'nightHalt':nightHalt,
                                                                "extraHour":False,
                                                                "extraHourCount":0,
                                                                'extraHourRate':extraHourRate,
                                                                'nightHaltCharge':nightHaltCharge
                                                            }
                                                        ],
                                            'payment': [
                                                            {

                                                                'amount':payment,
                                                                'status':0,
                                                                'method':0, #0 - cash, 1 - UPI
                                                                'transacationId':'',
                                                                'transacationRef':''
                                                            }
                                                        ],
                                            'entityId' : self.entityId,
                                            'sendSmsCounter':0,
                                            'touristId':self.profileId,
                                            'bookType':0,
                                            'ticketId': ticketId
                                        }
                                    )
                            bookingId = str(bookingId.inserted_id)
                            v = {
                                    'bookingId': bookingId,
                                    'touristSpotId':str(tourGuideId),
                                    'paymentMade':payment,
                                    'totalTourist':numOfAdult + numOfChild
                                }
                            result.append(v)
                            code = 2000
                            status = True
                            message = "Tour Guide has been booked."
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
