#!/usr/bin/env python
# -*- coding: utf-8 -*-



from __future__ import division
from ..lib.lib import *
from PIL import Image
from datetime import timezone
from datetime import date
import datetime
from baseconvert import base

@xenSecureV1
class MtimeWebTouristSpotBookHandler(tornado.web.RequestHandler,
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
            modifiedTime = int(self.request.arguments['modifiedTime'][0])
        except Exception as e:
            modifiedTime = 0

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
                    if app[0]['apiId'] in [ 402020, 402021, 402022, 402023]: # TODO: till here
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
                                if modifiedTime > 0:
                                    bookInfoQ = self.touristSpotBook.find(
                                            {
                                                'providerDetails.0.id':self.profileId,
                                                '$where': query,
                                                'modifiedTime':{
                                                                    '$gte':modifiedTime
                                                               }
                                            }
                                        )
                                else:
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
                                                'ticketId':res['ticketId'],
                                                'modifiedTime':res['modifiedTime']
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
                        elif self.apiId in [402022,402023]:
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
                            '''
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
                            '''
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
                            touristSpotId = self.request.arguments.get('touristSpotId')
                            if touristSpotId == None:
                                code = 4560
                                status = False
                                message = "Tourist Spot not selected."
                                raise Exception
                            try:
                                touristSpotId = ObjectId(touristSpotId)
                            except:
                                code = 4565
                                status = False
                                message = "Invalid Tourist Spot ID"
                                raise Exception

                            touristSpotInfoQ = self.serviceAccount.find(
                                        {
                                            '_id':touristSpotId
                                        }
                                    )
                            touristSpotInfo = []
                            async for i in touristSpotInfoQ:
                                touristSpotInfo.append(i)
                            if touristSpotInfo == []:
                                code = 4680
                                status = False
                                message = "Tourist Spot Not found."
                                raise Exception

                            touristSpotProfile = touristSpotInfo[0]['profileId']

                            touristSpotAccQ = self.profile.find(
                                        {
                                            '_id':touristSpotProfile,
                                        }
                                    )
                            touristSpotAcc = []
                            async for i in touristSpotAccQ:
                                touristSpotAcc.append(i)

                            if touristSpotAcc == []:
                                code = 4680
                                status = False
                                message = "Tourist Spot Not found."
                                raise Exception

                            touristSpotAccount = touristSpotAcc[0]['accountId']

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
                                session = int(self.request.arguments.get('session'))
                                code, message = Validate.i(
                                        session,
                                        'session',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ session ].'
                                raise Exception


                            serviceSessionFindQ = self.serviceAccount.find(
                                                    {
                                                        '_id':touristSpotId,
                                                        'serviceType':6
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
                                    advanceDaysLimit = serviceSessionFind[0]['serviceInfo'][0]['advanceDays']
                                except:
                                    code = 9100
                                    status = False
                                    message = "Invalid Session"
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
                            if (((bookTime/1000000)+startTime) < ((currentTime/1000000))):
                                code = 4770
                                status = False
                                message = "Booking date/time cannot be older than current date/time."
                                raise Exception

                            totalEntry = numOfAdult + numOfChild
                            if (totalEntry > maxCapacity):
                                code = 8291
                                status = False
                                message = "Total number of people exceeds the available Capacity"
                                raise Exception

                            bookTimeN = int(bookTime/1000000) + timeOffsetIST
                            st = datetime.datetime.fromtimestamp(bookTimeN).strftime('%Y-%m-%d')
                            dateList = list(st.split ("-"))
                            dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                            timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                            dayTimeStamp = int(timestamp * 1000000)
                            #newBookTime = (timestamp + startTime) * 1000000 # if required to add starttime to booking time.
                            newBookTime = int(bookTimeN * 1000000)
                            Log.i(bookTime)
                            Log.i(dateList)
                            Log.i(dayTimeStamp)


                            currentTimeN = int(currentTime/1000000)
                            st = datetime.datetime.fromtimestamp(currentTimeN).strftime('%Y-%m-%d')
                            currentdateList = list(st.split ("-"))

                            #Counting no of days between current time and the book time.
                            try:
                                d1 = date(int(dateList[0]), int(dateList[1]), int(dateList[2]))
                                d0 = date(int(currentdateList[0]), int(currentdateList[1]), int(currentdateList[2]))
                                delta = d1 - d0
                            except:
                                code = 7832
                                status = False
                                message = "Internal Error. Please contact Support"
                                raise Exception

                            Log.i("Difference in days",delta.days)

                            if delta.days > advanceDaysLimit:
                                code = 8989
                                status = False
                                message = "Booking date is beyond the advanced booking date limit"
                                raise Exception


                            sessionAvailabilityQ = self.bookingSession.find(
                                                    {
                                                        'serviceAccountId':touristSpotId,
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
                                                        'serviceAccountId':touristSpotId,
                                                        'dayTimeStamp':dayTimeStamp,
                                                        'startTime':startTime,
                                                        'endTime':endTime,
                                                        'maxCapacity': maxCapacity,
                                                        'availableCapacity':maxCapacity,
                                                        'preBook':totalEntry,
                                                        'confirmBook':0,
                                                        'serviceType':6
                                                    }
                                                )
                                sessionId = str(sessionInsert.inserted_id)
                            if len(sessionAvailability):
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
                                                        'serviceAccountId':touristSpotId,
                                                        'dayTimeStamp':dayTimeStamp,
                                                        'startTime':startTime,
                                                        'endTime':endTime,
                                                    },
                                                    {
                                                    '$set':{
                                                        'preBook': sessionAvailability[0]['preBook'] + totalEntry
                                                    }
                                                }
                                        )


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
                            payment = (numOfAdult * touristSpotInfo[0]['serviceInfo'][0]['adultCharge']) \
                                    + (numOfChild * touristSpotInfo[0]['serviceInfo'][0]['childCharge'])

                            #Converting base 10 timestamp to base 36 to get ticket ID with ASCII letters
                            ticketId = base(currentTime, 10, 36, string=True)
                            bookingId = await self.touristSpotBook.insert_one(
                                        {
                                            'ticketId':ticketId,
                                            'serviceAccountId':touristSpotId,
                                            'bookingSession':ObjectId(sessionId),
                                            'serviceType':6,
                                            'primaryTouristInfo':accountData,
                                            'modifiedTime':timeNow(),
                                            'disabled':False,
                                            'providerDetails':[
                                                                {
                                                                    'id':touristSpotProfile,
                                                                    'accountId':touristSpotAccount
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
                                                                "startTime":startTime,
                                                                "endTime":endTime,
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
                                    'touristSpotId':str(touristSpotId),
                                    'paymentMade':payment,
                                    'totalTourist':numOfAdult + numOfChild
                                }
                            result.append(v)
                            code = 2000
                            status = True
                            message = "Ticket has been created."
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
