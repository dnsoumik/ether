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


@xenSecureV1
class MtimeWebServiceActiveHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ('POST','OPTIONS')

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
    def options(self):
        self.set_status(200)
        self.write({})
        self.finish()
        return

    fu = FileUtil()

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
            async for r in profileQ:
                profile.append(r)
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
                async for r in appQ:
                    app.append(r)

                if len(app):
                    self.apiId = app[0]['apiId']
                    if app[0]['apiId'] in [ 402020, 402021, 402022]: # TODO: till here
                        if self.apiId == 402022:
                            serviceAccountId = self.request.arguments.get('serviceAccountId')
                            if serviceAccountId == None:
                                code = 8793
                                status = False
                                message = "Missing Argument - ['serviceAccountId']"
                                raise Exception
                            try:
                                serviceAccountId = ObjectId(serviceAccountId)
                            except:
                                code = 8988
                                status = False
                                message = "Invalid Argument -['serviceAccountId']"
                                raise Exception

                            serviceType = self.request.arguments.get('serviceType')
                            if serviceType == None:
                                code = 8932
                                status = False
                                message = "Missing Argument - ['serviceType']"
                                raise Exception
                            if serviceType not in [1,2,3,4,5,6]:
                                code = 3827
                                status = False
                                message = "Invalid Argument - ['serviceType']"
                                raise Exception

                            serAccFindQ = self.serviceAccount.find(
                                            {
                                                '_id':serviceAccountId,
                                                'entityId':self.entityId,
                                                'serviceType':serviceType,
                                            }
                                        )
                            serAccFind = []
                            async for i in serAccFindQ:
                                serAccFind.append(i)
                            if not len(serAccFind):
                                code = 2839
                                status = False
                                message = "Service Account Not Found"
                                raise Exception
                            if serAccFind[0]['disabled'] == False:
                                disabledValue = True
                                disabledValueMsg = "enabled"
                            elif serAccFind[0]['disabled'] == True:
                                disabledValue = False
                                disabledValueMsg = "disabled"
                            serAccStatusUpdate = await self.serviceAccount.update_one(
                                                    {
                                                        '_id':serviceAccountId,
                                                        'entityId':self.entityId,
                                                        'serviceType':1
                                                    },
                                                    {
                                                        '$set':
                                                                {
                                                                    'disabled':disabledValue
                                                                },
                                                        '$push':{
                                                                    'activity':{
                                                                                    'task':disabledValueMsg,
                                                                                    'time':timeNow(),
                                                                                    'accountId':self.accountId,
                                                                                    'profileId':self.profileId
                                                                               }
                                                                }
                                                    }
                                                )
                            if serAccStatusUpdate.modified_count != None:
                                code = 2000
                                status = True
                                message = "Service Account has been " + disabledValueMsg
                            else:
                                code = 7832
                                status = False
                                message = "Service Account could not be " + disabledValueMsg
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
