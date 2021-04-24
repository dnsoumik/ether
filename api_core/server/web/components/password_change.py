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
from lib import *
from ..lib.lib import *
from datetime import datetime

@xenSecureV1
class MtimeWebPasswordChangeHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ('GET', 'POST', 'DELETE','PUT','OPTIONS')

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
                # GET JSON FROM REQUEST BODY
                self.request.arguments = json.loads(self.request.body.decode())

            except Exception as e:
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                code = 4100
                message = 'Expected Request Type FormData.'
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
                if len(app):
                    self.apiId = app[0]['apiId']
                    if app[0]['apiId'] in [402022, 402023]: # TODO: till here
                        accFindQ = self.account.find(
                                    {
                                        '_id':self.accountId
                                    }
                                )
                        accFind = []
                        async for i in accFindQ:
                            accFind.append(i)
                        if not len(accFind):
                            code = 4665
                            status = False
                            message = "Account does not exist for this profile"
                            raise Exception
                        oldPassword = self.request.arguments.get('oldPassword')
                        if oldPassword == None or oldPassword == '':
                            code = 4556
                            status = True
                            message = "Please enter the old password"
                            raise Exception
                        code,message = Validate.i(
                                        oldPassword,
                                        'Old Password',
                                        maxLength = 50
                                    )
                        if code != 4100:
                            raise Exception
                        if oldPassword != accFind[0]['privacy'][0]['value']:
                            code = 4755
                            status = False
                            message = "The entered old password is incorrect"
                            raise Exception
                        newPassword = self.request.arguments.get('newPassword')
                        if newPassword == None or newPassword == '':
                            code = 4556
                            status = True
                            message = "Please enter the new password"
                            raise Exception
                        code,message = Validate.i(
                                        newPassword,
                                        'New Password',
                                        maxLength = 50
                                    )
                        if code != 4100:
                            raise Exception
                        changePassword = await self.account.update_one(
                                            {
                                                '_id':self.accountId
                                            },
                                            {
                                            '$set':
                                                {
                                                    'privacy.0.value':newPassword
                                                }
                                            }
                                        )
                        if changePassword.modified_count != None:
                            code = 2000
                            status = True
                            message = "The password has been changed"
                        else:
                            code = 4855
                            status = False
                            message = "Invalid password change"
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
