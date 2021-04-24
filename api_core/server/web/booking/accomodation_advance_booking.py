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
from PIL import Image
from ..lib.lib import *
from datetime import timezone
from datetime import date
import datetime
import requests
import http.client
import base64
#import aiohttp
#import asyncio
#import os

#from aiohttp import ClientSession

@xenSecureV1
class MtimeAccomodationAdvanceBookHandler(tornado.web.RequestHandler,
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
    touristBook = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][19]['name']
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
                            hotelId = self.request.arguments.get('hotelId')
                            if hotelId == None:
                                code = 4560
                                status = False
                                message = "Hotel not selected."
                                raise Exception
                            try:
                                hotelId = ObjectId(hotelId)
                            except:
                                code = 4565
                                status = False
                                message = "Invalid Hotel ID"
                                raise Exception

                            hotelInfoQ = self.serviceAccount.find(
                                        {
                                            '_id':hotelId,
                                            'serviceType':1,
                                            'disabled':False
                                        }
                                    )
                            hotelInfo = []
                            async for i in hotelInfoQ:
                                hotelInfo.append(i)
                            if hotelInfo == []:
                                code = 4680
                                status = False
                                message = "Hotel Not found."
                                raise Exception

                            hotelProfile = hotelInfo[0]['profileId']
                            district = hotelInfo[0]['hotelInfo'][0]['district']


                            hotelAccQ = self.profile.find(
                                        {
                                            '_id':hotelProfile,
                                        }
                                    )
                            hotelAcc = []
                            async for i in hotelAccQ:
                                hotelAcc.append(i)


                            if hotelAcc == []:
                                code = 4680
                                status = False
                                message = "Hotel Not found."
                                raise Exception

                            hotelAccount = hotelAcc[0]['accountId']


                            try:
                                timeZoneOffset = int(self.request.arguments.get('timeZoneOffset'))
                            except:
                                timeZoneOffset = 19800000000

                            try:
                                startTime = int(self.request.arguments.get('startTime'))
                                #Till timezone fix, adding 5 and half hours
                                startTime = startTime + timeZoneOffset
                                code, message = Validate.i(
                                        startTime,
                                        'startTime',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ startTime ].'
                                raise Exception

                            try:
                                endTime = int(self.request.arguments.get('endTime'))
                                #Till timezone fix, adding 5 and half hours
                                endTime = endTime + timeZoneOffset
                                code, message = Validate.i(
                                        endTime,
                                        'endTime',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ endTime ].'
                                raise Exception

                            try:
                                touristCount = int(self.request.arguments.get('touristCount'))
                                code, message = Validate.i(
                                        touristCount,
                                        'touristCount',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Input for number of tourists'
                                raise Exception

                            try:
                                numOfRoom = int(self.request.arguments.get('numOfRoom'))
                                code, message = Validate.i(
                                        numOfRoom,
                                        'numOfRoom',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Input for number of rooms'
                                raise Exception


                            try:
                                categoryId = int(self.request.arguments.get('categoryId'))
                                code, message = Validate.i(
                                        categoryId,
                                        'categoryId',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Input for category'
                                raise Exception

                            if True:
                                bookTimeN = int(startTime/1000000) 
                                st = datetime.datetime.fromtimestamp(bookTimeN).strftime('%Y-%m-%d')
                                dateList = list(st.split ("-"))
                                dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                                dayTimeStamp = int(timestamp * 1000000)

                            try:
                                endTimeN = int(endTime/1000000) 
                                et = datetime.datetime.fromtimestamp(endTimeN).strftime('%Y-%m-%d')
                                endList = list(et.split ("-"))
                                edt = datetime.datetime(int(endList[0]), int(endList[1]), int(endList[2]), 0, 0, 0)
                                timestamp = edt.replace(tzinfo=timezone.utc).timestamp()
                                endTimestamp = int(timestamp * 1000000)
                                d1 = date(int(dateList[0]), int(dateList[1]), int(dateList[2]))
                                d2 = date(int(endList[0]), int(endList[1]), int(endList[2]))
                                delta = d2 - d1
                            except:
                                code = 7832
                                status = False
                                message = "Internal Error. Please contact Support"
                                raise Exception


                            Log.i("Difference in days",delta.days)
                            noOfDays = int(delta.days)


                            #Needed when check is there
                            '''
                            if delta.days > advanceDaysLimit:
                                code = 8989
                                status = False
                                message = "Booking date is beyond the advanced booking date limit"
                                raise Exception
                            '''
                            dayRange = []
                            cTime = dayTimeStamp
                            while cTime <= endTimestamp:
                                dayRange.append(cTime)
                                categoryInfoQ = self.accSession.find(
                                                            {
                                                                'dayTimeStamp':cTime,
                                                                'serviceAccountId':hotelId,
                                                                'serviceType':1,
                                                                'profileId':hotelProfile,
                                                                'entityId':self.entityId,
                                                            },
                                                        )

                                categoryInfo = []
                                async for i in categoryInfoQ:
                                    categoryInfo.append(i)

                                if len(categoryInfo):
                                    sessionId = categoryInfo[0]['_id']




                                if not len(categoryInfo):
                                    categoryInfoQ = self.inventory.find(
                                                {
                                                    'serviceAccountId':hotelId,
                                                    'serviceType':1,
                                                    'profileId':hotelProfile,
                                                    'entityId':self.entityId,
                                                }
                                            )
                                    categoryInfo = []
                                    async for i in categoryInfoQ:
                                        categoryInfo.append(i)


                                    if len(categoryInfo):
                                        accSessionInsert = await self.accSession.insert_one(
                                                            {
                                                                'dayTimeStamp':cTime,
                                                                'serviceAccountId':hotelId,
                                                                'serviceType':1,
                                                                'profileId':hotelProfile,
                                                                'entityId':self.entityId,
                                                                'inventoryInformation':categoryInfo[0]['inventoryInformation'],
                                                                'time':timeNow(),
                                                                'modifiedTime':timeNow(),
                                                                'bookings':[]
                                                            }
                                                        )
                                        sessionId = accSessionInsert.inserted_id

                                    if not len(categoryInfo):
                                        code = 7922
                                        status = False
                                        message = "Hotel Inventory Not Found"
                                        raise Exception
                                cTime = cTime + 86400000000



                            try:
                                amount = categoryInfo[0]['inventoryInformation'][categoryId]['rate']
                                gst = categoryInfo[0]['inventoryInformation'][categoryId]['gst']
                                discount = categoryInfo[0]['inventoryInformation'][categoryId]['discount']
                                totalAmount = float((numOfRoom * amount) * noOfDays)
                                discountAmount = totalAmount * (discount / 100)
                                discountAmount = float(discountAmount)
                                beforeGst = totalAmount - discountAmount
                                gstAmount = beforeGst * (gst/100)
                                gstAmount = float(gstAmount)
                                totalDue = beforeGst + gstAmount
                                totalDue = float(int(totalDue))
                                selectedCategory = []
                                selectedCategory.append(categoryInfo[0]['inventoryInformation'][categoryId])
                            except:
                                code = 4738
                                status = False
                                message = "Invalid Category Selected"
                                raise Exception

                            bookingTime = timeNow()
                            bookingTimeN = int(bookingTime/1000000)
                            bt = datetime.datetime.fromtimestamp(bookingTimeN).strftime('%Y-%m-%d')
                            dateList = list(bt.split ("-"))
                            dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                            timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                            bookingTimeN = int(timestamp * 1000000)
                            if (startTime < bookingTimeN) or (endTime<bookingTimeN):
                                code = 4770
                                status = False
                                message = "Booking start and end date is not valid"
                                raise Exception
                            if startTime > endTime:
                                code = 4680
                                status = False
                                message = "Booking end date cannot be lesser than start date"
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
                            if len(accInfo):
                                v = {
                                        'firstName': accInfo[0]['firstName'],
                                        'lastName': accInfo[0]['lastName'],
                                        'contact':  accInfo[0]['contact']
                                    }
                            accountData.append(v)

                            receiptIdPart = base(bookingTime, 10, 64, string=True)
                            receiptId = 'mt1_' + str(receiptIdPart)

                            #razorpay api here
                            if True:
                                Log.i('razorpay_uid', RAZORPAY_UID)
                                Log.i('razorpay_pass', RAZORPAY_PWD)
                                userPassword = RAZORPAY_UID + ':' + RAZORPAY_PWD
                                userPassword = userPassword.encode()
                                userPassword = base64.b64encode(userPassword)
                                userPasswordAuth = str(userPassword.decode("utf-8"))
                                basicAuth = 'Basic ' + userPasswordAuth
                                conn = http.client.HTTPSConnection("api.razorpay.com")
                                body = {
                                                "amount": int(totalDue) * 100,
                                                #"amount":1000,
                                                "currency":"INR",
                                                "receipt": receiptId,
                                                "payment_capture":True,
                                                "transfers":[
                                                                {
                                                                    "account":"acc_G6BgSy3ZvyymFL",
                                                                    "amount":"100",
                                                                    "currency":"INR",
                                                                    "on_hold":1
                                                                }
                                                            ]
                                       }
                                body = json.dumps(body)
                                headers = {
                                        'content-type': 'application/json',
                                        'authorization': basicAuth,
                                    }

                                conn.request("POST", "/v1/orders", body, headers)
                                res = conn.getresponse()
                                data = res.read()
                                stat = json.loads(data.decode("utf-8"))

                                try:
                                    if stat['status'] == 'created':
                                        paymentOrderId = stat['id']
                                    else:
                                        raise Exception
                                except:
                                    code = 3729
                                    status = False
                                    message = "Failure in online payment. Please contact Support"
                                    raise Exception

                            else:
                                paymentOrderId = ""

                            bookingId = await self.touristBook.insert_one(
                                        {
                                            'touristCount':touristCount,
                                            'serviceAccountId':hotelId,
                                            'expiredAt': dtime.now(),
                                            'sessionId':sessionId,
                                            'serviceType':1,
                                            'primaryTouristInfo':accountData,
                                            'touristDetails':[],
                                            'disabled':False,
                                            'modifiedTime':timeNow(),
                                            'providerDetails':[
                                                                {
                                                                    'id':hotelProfile,
                                                                    'accountId':hotelAccount,
                                                                    'district':district
                                                                }
                                                            ],
                                            'time':bookingTime,
                                            'activity' : [
                                                            {
                                                                "id":0,
                                                                "time":bookingTime,
                                                                "startTime":startTime,
                                                                "endTime":endTime,
                                                                "timeZoneOffset":timeZoneOffset
                                                            }
                                                        ],
                                            "inventory": [
                                                            {
                                                                "numOfRoom": numOfRoom,
                                                                "numOfAdult": touristCount,
                                                                "numOfChild": 0,
                                                                "categoryId":categoryId,
                                                                "categoryInfo":selectedCategory
                                                            }
                                                        ],
                                            'payment': [
                                                            {
                                                                'paymentOrderId':paymentOrderId,
                                                                'amount':round(totalAmount,1),
                                                                'discount':round(discountAmount,1),
                                                                'gst':round(gstAmount,1),
                                                                'totalDue':round(totalDue,1),
                                                                'status':0,
                                                                'receipt': receiptId,
                                                                'method':0, #0 - cash, 1 - UPI
                                                                'transactionId':'',
                                                                'transactionRef':''
                                                            }
                                                        ],
                                            'entityId' : self.entityId,
                                            'sendSmsCounter':0,
                                            'touristId':self.profileId,
                                            'bookType':0
                                        }
                                    )
                            decValue = numOfRoom * -1
                            for d in dayRange:
                                accSessionUpdate = await self.accSession.update_one(
                                                            {
                                                                'dayTimeStamp':d,
                                                                'serviceAccountId':hotelId,
                                                                'serviceType':1,
                                                                'profileId':hotelProfile,
                                                                'entityId':self.entityId,
                                                                'inventoryInformation.id':categoryId
                                                            },
                                                            {
                                                                '$inc':{
                                                                            'inventoryInformation.$.preBook':numOfRoom,
                                                                            'inventoryInformation.$.availableQuantity':decValue
                                                                       },
                                                                '$push':{
                                                                            'bookings':{
                                                                                            'bookingId':str(bookingId.inserted_id),
                                                                                            'time':bookingTime
                                                                                        }
                                                                        }
                                                            }
                                                    )
                            bookEntryUpdate = await self.accSession.update_one(
                                                            {
                                                                'dayTimeStamp':d,
                                                                'serviceAccountId':hotelId,
                                                                'serviceType':1,
                                                                'profileId':hotelProfile,
                                                                'entityId':self.entityId,
                                                                'inventoryInformation.id':categoryId
                                                            },
                                                            {
                                                                '$push':{
                                                                            'bookings':{
                                                                                            'bookingId':str(bookingId.inserted_id),
                                                                                            'time':bookingTime
                                                                                        }
                                                                        }
                                                            }
                                                    )

                            v = {
                                    'bookingId':str(bookingId.inserted_id),
                                    'sessionId':str(sessionId),
                                    'serviceAccountId':str(hotelId),
                                    'paymentOrderId':str(paymentOrderId),
                                    'payment':totalAmount,
                                    'totalTourist':touristCount,
                                    'receiptId': receiptId,
                                    'paymentGatewayKey':RAZORPAY_UID
                                }
                            result.append(v)
                            code = 2000
                            status = True
                            message = "Booking has been made"
                        elif self.apiId == 402021:
                            hotelId = self.request.arguments.get('hotelId')
                            if hotelId == None:
                                code = 4560
                                status = False
                                message = "Hotel not selected."
                                raise Exception
                            try:
                                hotelId = ObjectId(hotelId)
                            except:
                                code = 4565
                                status = False
                                message = "Invalid Hotel ID"
                                raise Exception

                            profileId = self.request.arguments.get('id')
                            if profileId == None:
                                code = 4560
                                status = False
                                message = "Tourist not selected."
                                raise Exception
                            try:
                                profileId = ObjectId(profileId)
                            except:
                                code = 4565
                                status = False
                                message = "Invalid Tourist ID"
                                raise Exception

                            hotelInfoQ = self.serviceAccount.find(
                                        {
                                            '_id':hotelId,
                                            'serviceType':1,
                                            'disabled':False
                                        }
                                    )
                            hotelInfo = []
                            async for i in hotelInfoQ:
                                hotelInfo.append(i)
                            if hotelInfo == []:
                                code = 4680
                                status = False
                                message = "Hotel Not found."
                                raise Exception

                            hotelProfile = hotelInfo[0]['profileId']
                            district = hotelInfo[0]['hotelInfo'][0]['district']


                            hotelAccQ = self.profile.find(
                                        {
                                            '_id':hotelProfile,
                                        }
                                    )
                            hotelAcc = []
                            async for i in hotelAccQ:
                                hotelAcc.append(i)


                            if hotelAcc == []:
                                code = 4680
                                status = False
                                message = "Hotel Not found."
                                raise Exception

                            hotelAccount = hotelAcc[0]['accountId']
                            try:
                                timeZoneOffset = int(self.request.arguments.get('timeZoneOffset'))
                            except:
                                timeZoneOffset = 19800000000

                            try:
                                startTime = int(self.request.arguments.get('startTime'))
                                #Till timezone fix, adding 5 and half hours
                                startTime = startTime + timeZoneOffset
                                code, message = Validate.i(
                                        startTime,
                                        'startTime',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ startTime ].'
                                raise Exception

                            try:
                                endTime = int(self.request.arguments.get('endTime'))
                                #Till timezone fix, adding 5 and half hours
                                endTime = endTime + timeZoneOffset
                                code, message = Validate.i(
                                        endTime,
                                        'endTime',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ endTime ].'
                                raise Exception

                            try:
                                touristCount = int(self.request.arguments.get('touristCount'))
                                code, message = Validate.i(
                                        touristCount,
                                        'touristCount',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Input for number of tourists'
                                raise Exception

                            try:
                                numOfRoom = int(self.request.arguments.get('numOfRoom'))
                                code, message = Validate.i(
                                        numOfRoom,
                                        'numOfRoom',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Input for number of rooms'
                                raise Exception


                            try:
                                categoryId = int(self.request.arguments.get('categoryId'))
                                code, message = Validate.i(
                                        categoryId,
                                        'categoryId',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Input for category'
                                raise Exception

                            if True:
                                bookTimeN = int(startTime/1000000) 
                                st = datetime.datetime.fromtimestamp(bookTimeN).strftime('%Y-%m-%d')
                                dateList = list(st.split ("-"))
                                dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                                dayTimeStamp = int(timestamp * 1000000)

                            try:
                                endTimeN = int(endTime/1000000) 
                                et = datetime.datetime.fromtimestamp(endTimeN).strftime('%Y-%m-%d')
                                endList = list(et.split ("-"))
                                edt = datetime.datetime(int(endList[0]), int(endList[1]), int(endList[2]), 0, 0, 0)
                                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                                endTimestamp = int(timestamp * 1000000)
                                d1 = date(int(dateList[0]), int(dateList[1]), int(dateList[2]))
                                d2 = date(int(endList[0]), int(endList[1]), int(endList[2]))
                                delta = d2 - d1
                            except:
                                code = 7832
                                status = False
                                message = "Internal Error. Please contact Support"
                                raise Exception

                            Log.i("Difference in days",delta.days)
                            noOfDays = int(delta.days)

                            #Needed when check is there
                            '''
                            if delta.days > advanceDaysLimit:
                                code = 8989
                                status = False
                                message = "Booking date is beyond the advanced booking date limit"
                                raise Exception
                            '''


                            categoryInfoQ = self.accSession.find(
                                                            {
                                                                'dayTimeStamp':dayTimeStamp,
                                                                'serviceAccountId':hotelId,
                                                                'serviceType':1,
                                                                'profileId':hotelProfile,
                                                                'entityId':self.entityId,
                                                            },
                                                        )

                            categoryInfo = []
                            async for i in categoryInfoQ:
                                categoryInfo.append(i)

                            if len(categoryInfo):
                                sessionId = categoryInfo[0]['_id']




                            if not len(categoryInfo):
                                categoryInfoQ = self.inventory.find(
                                                {
                                                    'serviceAccountId':hotelId,
                                                    'serviceType':1,
                                                    'profileId':hotelProfile,
                                                    'entityId':self.entityId,
                                                }
                                            )
                                categoryInfo = []
                                async for i in categoryInfoQ:
                                    categoryInfo.append(i)


                                if len(categoryInfo):
                                    accSessionInsert = await self.accSession.insert_one(
                                                            {
                                                                'dayTimeStamp':dayTimeStamp,
                                                                'serviceAccountId':hotelId,
                                                                'serviceType':1,
                                                                'profileId':hotelProfile,
                                                                'entityId':self.entityId,
                                                                'inventoryInformation':categoryInfo[0]['inventoryInformation'],
                                                                'time':timeNow(),
                                                                'modifiedTime':timeNow()
                                                            }
                                                        )
                                    sessionId = accSessionInsert.inserted_id

                            if not len(categoryInfo):
                                code = 7922
                                status = False
                                message = "Hotel Inventory Not Found"
                                raise Exception


                            try:
                                amount = categoryInfo[0]['inventoryInformation'][categoryId]['rate']
                                gst = categoryInfo[0]['inventoryInformation'][categoryId]['gst']
                                discount = categoryInfo[0]['inventoryInformation'][categoryId]['discount']
                                totalAmount = float((numOfRoom * amount) * noOfDays)
                                discountAmount = totalAmount * (discount / 100)
                                discountAmount = float(discountAmount)
                                beforeGst = totalAmount - discountAmount
                                gstAmount = beforeGst * (gst/100)
                                gstAmount = float(gstAmount)
                                totalDue = beforeGst + gstAmount
                                totalDue = float(int(totalDue))
                                selectedCategory = []
                                selectedCategory.append(categoryInfo[0]['inventoryInformation'][categoryId])
                            except:
                                code = 4738
                                status = False
                                message = "Invalid Category Selected"
                                raise Exception

                            bookingTime = timeNow()
                            bookingTimeN = int(bookingTime/1000000)
                            bt = datetime.datetime.fromtimestamp(bookingTimeN).strftime('%Y-%m-%d')
                            dateList = list(bt.split ("-"))
                            dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                            timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                            bookingTimeN = int(timestamp * 1000000)
                            if (startTime < bookingTimeN) or (endTime<bookingTimeN):
                                code = 4770
                                status = False
                                message = "Booking start and end date is not valid"
                                raise Exception
                            if startTime > endTime:
                                code = 4680
                                status = False
                                message = "Booking end date cannot be lesser than start date"
                                raise Exception
                            accountData = []

                            proInfoQ = self.profile.find(
                                                {
                                                    '_id':profileId,
                                                    'entityId':self.entityId
                                                }
                                            )
                            proInfo = []
                            async for i in proInfoQ:
                                proInfo.append(i)
                            if not len(proInfo):
                                code = 7919
                                status = False
                                message = "Tourist Profile not found"
                                raise Exception
                            accInfoQ = self.account.find(
                                                {
                                                    '_id':proInfo[0]['accountId']
                                                }
                                            )
                            accInfo = []
                            async for i in accInfoQ:
                                accInfo.append(i)
                            if not len(accInfo):
                                code = 8392
                                status = False
                                message = "Tourist Account Not Found"
                                raise Exception

                            if len(accInfo):
                                v = {
                                        'firstName': accInfo[0]['firstName'],
                                        'lastName': accInfo[0]['lastName'],
                                        'contact':  accInfo[0]['contact']
                                    }
                            accountData.append(v)

                            # Recept Id should be unique
                            #receiptId = 'MT{}ACCOM'.format(bookingTime)
                            receiptIdPart = base(bookingTime, 10, 64, string=True)
                            receiptId = 'mt1_' + str(receiptIdPart)

                            #razorpay api here
                            try:
                                userPassword = RAZORPAY_UID + ':' + RAZORPAY_PWD
                                userPassword = userPassword.encode()
                                userPassword = base64.b64encode(userPassword)
                                userPasswordAuth = str(userPassword.decode("utf-8"))
                                basicAuth = 'Basic ' + userPasswordAuth
                                conn = http.client.HTTPSConnection("api.razorpay.com")
                                body = {
                                                "amount": int(totalDue) * 100,
                                                "currency":"INR",
                                                "receipt": receiptId,
                                                "payment_capture":True,
                                                "transfers":[
                                                                {
                                                                    "account":"acc_G6BgSy3ZvyymFL",
                                                                    "amount":"100",
                                                                    "currency":"INR",
                                                                    "on_hold":1
                                                                }
                                                            ]
                                       }
                                body = json.dumps(body)
                                headers = {
                                        'content-type': 'application/json',
                                        'authorization': basicAuth,
                                    }

                                conn.request("POST", "/v1/orders", body, headers)
                                res = conn.getresponse()
                                data = res.read()
                                stat = json.loads(data.decode("utf-8"))
                                Log.i(stat)

                                try:
                                    if stat['status'] == 'created':
                                        paymentOrderId = stat['id']
                                    else:
                                        raise Exception
                                except:
                                    code = 3729
                                    status = False
                                    message = "Failure in online payment. Please contact Support"
                                    raise Exception

                                print("Payment Id")
                                Log.i(str(paymentOrderId))

                            except:
                                code = 3729
                                status = False
                                message = "Failure in online payment. Please contact Support"
                                raise Exception

                            bookingId = await self.touristBook.insert_one(
                                        {
                                            'touristCount':touristCount,
                                            'expiredAt': dtime.now(),
                                            'serviceAccountId':hotelId,
                                            'sessionId':sessionId,
                                            'serviceType':1,
                                            'primaryTouristInfo':accountData,
                                            'touristDetails':[],
                                            'disabled':False,
                                            'modifiedTime':timeNow(),
                                            'providerDetails':[
                                                                {
                                                                    'id':hotelProfile,
                                                                    'accountId':hotelAccount,
                                                                    'district':district
                                                                }
                                                            ],
                                            'time':bookingTime,
                                            'activity' : [
                                                            {
                                                                "id":0,
                                                                "time":bookingTime,
                                                                "startTime":startTime,
                                                                "endTime":endTime,
                                                                "timeZoneOffset":timeZoneOffset
                                                            }
                                                        ],
                                            "inventory": [
                                                            {
                                                                "numOfRoom": numOfRoom,
                                                                "numOfAdult": touristCount,
                                                                "numOfChild": 0,
                                                                "categoryId":categoryId,
                                                                "categoryInfo":selectedCategory
                                                            }
                                                        ],
                                            'payment': [
                                                            {
                                                                'paymentOrderId':paymentOrderId,
                                                                'amount':round(totalAmount,1),
                                                                'discount':round(discountAmount,1),
                                                                'gst':round(gstAmount,1),
                                                                'totalDue':round(totalDue,1),
                                                                'receiptId': receiptId,
                                                                'status':0,
                                                                'method':0, #0 - cash, 1 - UPI
                                                                'transactionId':'',
                                                                'transactionRef':''
                                                            }
                                                        ],
                                            'entityId' : self.entityId,
                                            'sendSmsCounter':0,
                                            'touristId':profileId,
                                            'bookType':0,
                                            'createdBy':[
                                                            {
                                                                'serviceType':3,
                                                                'profileId':self.profileId
                                                            }
                                                        ]
                                        }
                                    )
                            decValue = numOfRoom * -1
                            accSessionUpdate = await self.accSession.update_one(
                                                            {
                                                                'dayTimeStamp':dayTimeStamp,
                                                                'serviceAccountId':hotelId,
                                                                'serviceType':1,
                                                                'profileId':hotelProfile,
                                                                'entityId':self.entityId,
                                                                'inventoryInformation.id':categoryId
                                                            },
                                                            {
                                                                '$inc':{
                                                                            'inventoryInformation.$.preBook':numOfRoom,
                                                                            'inventoryInformation.$.availableQuantity':decValue
                                                                       },
                                                                '$push':{
                                                                            'bookings':{
                                                                                            'bookingId':str(bookingId.inserted_id),
                                                                                            'time':bookingTime
                                                                                        }
                                                                        }
                                                            }
                                                    )
                            v = {
                                    'bookingId':str(bookingId.inserted_id),
                                    'sessionId':str(sessionId),
                                    'serviceAccountId':str(hotelId),
                                    'paymentOrderId':str(paymentOrderId),
                                    'payment':totalAmount,
                                    'totalTourist':touristCount,
                                    'receiptId': receiptId,
                                    'paymentGatewayKey':RAZORPAY_UID
                                }
                            result.append(v)
                            code = 2000
                            status = True
                            message = "Booking has been made"
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
