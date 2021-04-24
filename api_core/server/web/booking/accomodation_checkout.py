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

#import face_recognition

@xenSecureV1
class MtimeWebAccomodationCheckoutHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ( 'POST','OPTIONS')

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
    subTourist = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][17]['name']
                ]
    noregTouristBook = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][23]['name']
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
                bookingId = str(self.request.arguments['bookingId'][0].decode())
                try:
                    bookingId = ObjectId(bookingId)
                except:
                    raise Exception
            except Exception as e:
                code = 4103
                message = 'Invalid Argument [ bookingId ].'
                raise Exception

            try:
                subId = str(self.request.arguments['subId'][0].decode())
                try:
                    subId = ObjectId(subId)
                except:
                    raise Exception
            except:
                code == 4320
                message = 'Invalid Argument - [ Subtourist Id ].'
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
                    if self.apiId in [ 402021]:
                        if self.apiId == 402021: # TODO: till here

                            try:
                                sync = self.get_arguments('sync')[0]
                                if sync == "true":
                                    sync = True
                                elif sync == "false":
                                    sync = False
                                if sync != None:
                                    if type(sync) != bool:
                                        code = 2894
                                        status = False
                                        message = "Invalid argument - ['sync']"
                                        raise Exception
                                    if sync == True:
                                        try:
                                            checkoutTime = int(self.get_arguments['time'][0])
                                        except:
                                            code = 8985
                                            status = False
                                            message = "Invalid argument - ['time']"
                                            raise Exception
                            except:
                                sync = False
                                checkoutTime = timeNow()



                            cOutCounterQ = self.touristBook.find(
                                            {
                                                '_id': bookingId,
                                                'entityId':self.entityId
                                            },
                                            {
                                                '_id':0,
                                                'liveCheckOutCount':1
                                            }
                                        )

                            cOutCounter = []
                            async for i in cOutCounterQ:
                                cOutCounter.append(i)


                            if not len(cOutCounter):
                                code = 2356
                                status = False
                                message = "Booking Not Found"
                                raise Exception


                            checkoutCount =  int(cOutCounter[0]['liveCheckOutCount'])

                            if checkoutCount == 0:
                                case = 4750
                                status = True
                                message = "Checkout is already done."
                                self.write(
                                        {
                                            'status': True,
                                            'result': [],
                                            'message': message,
                                            'code': code,
                                        }
                                    )
                                self.finish()
                                return

                            elif checkoutCount == 1:
                                proofCheckQ = self.touristBook.find(
                                                {
                                                    '_id': bookingId,
                                                    'touristDetails.id': str(subId)
                                                },
                                                {
                                                    'touristDetails.liveProof2.$':1
                                                }
                                            )
                                proofCheck = []
                                async for i in proofCheckQ:
                                    proofCheck.append(i)
                                if len(proofCheck[0]['touristDetails'][0]['liveProof2']):
                                    code = 4565
                                    result = []
                                    status = True
                                    message = "This person has been already checked out"
                                    self.write(
                                        {
                                            'status': status,
                                            'result': result,
                                            'message': message,
                                            'code': code,
                                        }
                                    )
                                    self.finish()
                                    return

                                checkOutUpdate = await self.touristBook.update_one(
                                    {
                                        '_id': bookingId,
                                        'touristDetails.id': str(subId)
                                    },
                                    {
                                        '$set': {
                                                    'modifiedTime':timeNow(),
                                                    'touristDetails.$.liveProof2':
                                                                                    [
                                                                                        {
                                                                                            'time': checkoutTime,
                                                                                            'mimeType': None
                                                                                        }
                                                                                    ]
                                                },
                                        '$push':{
                                                    'activity':{
                                                                    'id':8,
                                                                    'time':checkoutTime,
                                                                    'sync':sync
                                                                }
                                                },
                                        '$inc': {
                                                    'liveCheckOutCount': -1,
                                                }
                                    }
                                )
                                if checkOutUpdate.modified_count != None:
                                    code = 2000
                                    status = True
                                    message = "Checkout is complete."
                                else:
                                    code = 4302
                                    status = False
                                    message = 'Invalid Booking'
                            else:
                                proofCheckQ = self.touristBook.find(
                                                {
                                                    '_id': bookingId,
                                                    'touristDetails.id': str(subId)
                                                },
                                                {
                                                    'touristDetails.liveProof2.$':1
                                                }
                                            )
                                proofCheck = []
                                async for i in proofCheckQ:
                                    proofCheck.append(i)
                                if len(proofCheck[0]['touristDetails'][0]['liveProof2']):
                                    code = 4565
                                    status = True
                                    result = []
                                    message = "This person has been already checked out"
                                    self.write(
                                        {
                                            'status': status,
                                            'result': result,
                                            'message': message,
                                            'code': code,
                                        }
                                    )
                                    self.finish()
                                    return
                                checkOutUpdate = await self.touristBook.update_one(
                                    {
                                        '_id': bookingId,
                                        'touristDetails.id': str(subId)
                                    },
                                    {
                                        '$set': {
                                                    'modifiedTime':timeNow(),
                                                    'touristDetails.$.liveProof2': [
                                                                                    {
                                                                                        'time': checkoutTime,
                                                                                        'mimeType': None
                                                                                    }
                                                                                ]
                                                    },
                                        '$inc': {
                                                    'liveCheckOutCount': -1,
                                                }
                                    }
                                )
                                if checkOutUpdate.modified_count != None:
                                    code = 2000
                                    status = True
                                    message = "This person has been successfully checked out"
                                else:
                                    code = 4302
                                    status = False
                                    message = 'Invalid Booking'
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

