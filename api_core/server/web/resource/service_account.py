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
class MtimeWebServiceAccountInfoHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ('GET','POST','OPTIONS')

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

    fu = FileUtil()
    def options(self):
        self.set_status(200)
        self.write({})
        self.finish()
        return

    # @defer.inlineCallbacks
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
                    if app[0]['apiId'] in [402020, 402021, 402022, 402023]:  # TODO: till here
                        if self.apiId == 402022 or self.apiId == 402023:
                            try:
                                currentNum = int(self.get_arguments('currentNum')[0])
                            except:
                                currentNum = None
                            try:
                                newNum = int(self.get_arguments('newNum')[0])
                            except:
                                newNum = None
                            if currentNum == None and newNum == None:
                                proFindQ = self.profile.find(
                                        {
                                            'applicationId':ObjectId("5e5626be91ae0dbdf6592b2e")
                                        }
                                    )
                                proFind = []
                                async for i in proFindQ:
                                    proFind.append(i)
                                for res in proFind:
                                    accFindQ = self.account.find(
                                            {
                                                '_id':res['accountId']
                                            }
                                        )
                                    accFind = []
                                    async for i in accFindQ:
                                        accFind.append(i)
                                    if len(accFind):
                                        for res in accFind:
                                            v = {
                                                'fullName':res['firstName'] + ' ' + res['lastName'],
                                                'contact':res['contact']
                                                }
                                            result.append(v)
                                code = 2000
                                status = True
                                message = "List of Service Account"
                            else:
                                appFindQ = self.applications.find(
                                            {
                                                "apiId" : 402021
                                            }
                                        )
                                appFind = []
                                async for i in appFindQ:
                                    appFind.append(i)
                                if not len(appFind):
                                    code = 3882
                                    status = False
                                    message = "Internal Error. Please contact Support"
                                    raise Exception
                                numList = []
                                if len(str(currentNum)) > 12:
                                    currentNum = int(str(currentNum)[-10:])
                                    currentNum = 910000000000 + currentNum
                                if len(str(currentNum)) != 12:
                                    code = 4555
                                    status = False
                                    message = "Invalid Current Number"
                                    raise Exception
                                numList.append(currentNum)
                                if len(str(newNum)) != 12:
                                    code = 4560
                                    status = False
                                    message = "Invalid New Number"
                                    raise Exception
                                if currentNum == newNum:
                                    code = 4721
                                    status = False
                                    message = "Both phone numbers cannot be same"
                                    raise Exception
                                numList.append(newNum)
                                for num in numList:
                                    accFindQ = self.account.find(
                                                {
                                                    'contact.0.value':num
                                                },
                                            )
                                    accFind = []
                                    async for i in accFindQ:
                                        accFind.append(i)
                                    if not len(accFind):
                                        code = 4675
                                        status = False
                                        message = "Account not found for number " + str(num)
                                        raise Exception
                                    proFindQ = self.profile.find(
                                                {
                                                    'accountId':accFind[0]['_id'],
                                                    'applicationId':appFind[0]['_id']
                                                }
                                            )
                                    proFind = []
                                    async for i in proFindQ:
                                        proFind.append(i)
                                    if not len(proFind):
                                        code = 4829
                                        status = False
                                        message = "Service Provider Profile does not exist for number " + str(num)
                                        raise Exception
                                    accFind[0]['profileId'] = str(proFind[0]['_id'])
                                    accFind[0]['accountId'] = str(accFind[0]['_id'])
                                    del accFind[0]['_id']
                                    result.append(accFind[0])
                                code = 2000
                                status = True
                                message = "Account Information"
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
            # self.set_status(400)
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
                    if app[0]['apiId'] in [402020, 402021, 402022]:  # TODO: till here
                        if self.apiId == 402022:
                            try:
                                currentProfile = str(self.request.arguments['currentProfile'][0].decode())
                                try:
                                    currentProfile = ObjectId(currentProfile)
                                except:
                                    raise Exception
                            except:
                                code = 8765
                                status = False
                                message = "Invalid Current Profile ID"
                                raise Exception
                            try:
                                newProfile = str(self.request.arguments['newProfile'][0].decode())
                                try:
                                    newProfile = ObjectId(newProfile)
                                except:
                                    raise Exception
                            except:
                                code = 8770
                                status = False
                                message = "Invalid New Profile ID"
                                raise Exception
                            try:
                                currentAccount = str(self.request.arguments['currentAccount'][0].decode())
                                try:
                                    currentAccount = ObjectId(currentAccount)
                                except:
                                    raise Exception
                            except:
                                code = 8765
                                status = False
                                message = "Invalid Current Account ID"
                                raise Exception
                            try:
                                newAccount = str(self.request.arguments['newAccount'][0].decode())
                                try:
                                    newAccount = ObjectId(newAccount)
                                except:
                                    raise Exception
                            except:
                                code = 8770
                                status = False
                                message = "Invalid New Account ID"
                                raise Exception

                            newProfileSetNull = await self.profile.update_one(
                                                    {
                                                        '_id':newProfile
                                                    },
                                                    {
                                                    '$set':{
                                                                'accountId':None
                                                            }
                                                    }
                                                )
                            currentProfileSet = await self.profile.update_one(
                                                    {
                                                        '_id':currentProfile
                                                    },
                                                    {
                                                    '$set':{
                                                                'accountId':newAccount
                                                            }
                                                    }
                                                )
                            newProfileSet = await self.profile.update_one(
                                                    {
                                                        '_id':newProfile
                                                    },
                                                    {
                                                    '$set':{
                                                                'accountId':currentAccount
                                                            }
                                                    }
                                                )
                            code = 2000
                            status = True
                            message = "Account has been migrated"
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
            # self.set_status(400)
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
