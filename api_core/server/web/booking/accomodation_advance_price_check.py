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

@xenSecureV1
class MtimeAccomodationAdvancePriceCheckHandler(tornado.web.RequestHandler,
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
                        if self.apiId == 402020 or 402021:
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
                                startTime = int(self.request.arguments.get('startTime'))
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


                            #TODO: Need to confirm on one day limit for booking
                            if noOfDays == 0:
                                code = 8392
                                status = False
                                message = "Booking Start Date and End Date cannot be same"
                                raise Exception

                            #Needed when check is there
                            '''
                            if delta.days > advanceDaysLimit:
                                code = 8989
                                status = False
                                message = "Booking date is beyond the advanced booking date limit"
                                raise Exception
                            '''

                            checkInTime = 43200
                            checkOutTime = 39600

                            InvFindQ = self.inventory.find(
                                                {
                                                    'serviceAccountId':hotelId,
                                                    'serviceType':1,
                                                    'profileId':hotelProfile,
                                                    'entityId':self.entityId
                                                }
                                            )
                            InvFind = []
                            async for i in InvFindQ:
                                InvFind.append(i)
                            if len(InvFind):
                                if len(InvFind[0]['settings']):
                                    try:
                                        checkInTime = InvFind[0]['settings'][0]['checkInTime']
                                        checkOutTime = InvFind[0]['settings'][0]['checkOutTime']
                                    except:
                                        Log.i("Check In and Check Out Time not set. So, taking default values")



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


                            if not len(categoryInfo):
                                code = 7922
                                status = False
                                message = "Hotel Inventory Not Found"
                                raise Exception


                            try:
                                amount = int(categoryInfo[0]['inventoryInformation'][categoryId]['rate'])
                                gst = int(categoryInfo[0]['inventoryInformation'][categoryId]['gst'])
                                discount = int(categoryInfo[0]['inventoryInformation'][categoryId]['discount'])
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
                            except Exception as e:
                                Log.e(e)
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
                            v = {
                                    'serviceAccountId':str(hotelId),
                                    'payment': round(totalAmount, 1),
                                    'discountPercentage': round(discount, 1),
                                    'discountAmount': round(discountAmount, 1),
                                    'gstPercentage': round(gst, 1),
                                    'gstAmount': round(gstAmount, 1),
                                    'totalDue': round(totalDue, 1),
                                    'noOfDays': int(noOfDays),
                                    'checkInTime':checkInTime,
                                    'checkOutTime':checkOutTime,
                                    'totalTourist':touristCount
                                }
                            result.append(v)

                            code = 2000
                            status = True
                            message = "Accomodation Advanced Payment Info"
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
