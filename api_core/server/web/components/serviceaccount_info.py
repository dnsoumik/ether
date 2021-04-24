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


@xenSecureV1
class MtimeServiceAccountTypeInformationHandler(tornado.web.RequestHandler,
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
                    if app[0]['apiId'] in [ 402020, 402021, 402022,402023]: # TODO: till here
                        if self.apiId == 402020:
                            code = 7832
                            status = False
                            message = "API Not Implemented"
                            raise Exception
                        elif self.apiId == 402021:
                            if self.serviceAccountId == None:
                                self.profileId = profile[0]['_id']
                            else:
                                self.profileId = self.serviceAccountId
                            try:
                                serviceType = int(self.request.arguments['serviceType'][0])
                            except:
                                code = 8922
                                status = False
                                message = "Missing Argument - ['serviceType']"
                                raise Exception

                            if serviceType == 6:
                                sessionFindQ = self.serviceAccount.find(
                                                {
                                                    'serviceType':6,
                                                    'profileId':self.profileId,
                                                    'entityId':self.entityId
                                                }
                                            )
                                sessionFind = []
                                async for i in sessionFindQ:
                                    sessionFind.append(i)
                                if len(sessionFind):
                                    if sessionFind[0]['serviceInfo'] == []:
                                        code = 2578
                                        status = False
                                        message = "Service Information is not submitted"
                                        raise Exception
                                    if sessionFind[0]['serviceInfo'][0]['sessions'] == []:
                                        code = 2580
                                        status = False
                                        message = "Session Information is not submitted"
                                        raise Exception
                                    idNum = 0
                                    for i in sessionFind[0]['serviceInfo'][0]['sessions']:
                                        i['id'] = idNum
                                        idNum = idNum + 1
                                        result.append(i)
                                    code = 2000
                                    status = True
                                    message = "List of sessions"
                                else:
                                    code = 7889
                                    status = False
                                    message = "Data Not Found"
                            else:
                                code = 8923
                                status = False
                                message = "Service Type Not Supported"
                                raise Exception
                        elif self.apiId == 402022:
                            code = 7832
                            status = False
                            message = "API Not Implemented"
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
