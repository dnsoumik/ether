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

@xenSecureV1
class MtimeWebCovidHandler(tornado.web.RequestHandler,
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
    serviceType = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][44]['name']
                ]
    covidDecl = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][29]['name']
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
            '''
            try:
                self.request.arguments = json.loads(self.request.body)
            except:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
            '''
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
                    Log.i(self.apiId)
                    if self.apiId in [ 402020, 402022, 402021]:
                        '''
                        serviceType = self.request.arguments.get('serviceType')
                        code,message,serviceType = Validate.i(
                                serviceType,
                                'Service Type',
                                apex=110000,
                                parse = int,
                                minNumber = 0,
                                maxNumber = 9
                            )
                        if code != 4100:
                            raise Exception
                        '''
                        covidCheckQ = self.covidDecl.find(
                                        {
                                            'profileId':self.profileId,
                                            'serviceType':1
                                        }
                                    )
                        covidCheck = []
                        async for i in covidCheckQ:
                            covidCheck.append(i)
                        if len(covidCheck) == 1:
                            covidUpdate = await self.covidDecl.update_one(
                                        {
                                            'profileId':self.profileId,
                                            'serviceType':1
                                        },
                                        {
                                        "$set":{
                                                'covid19Declaration':True,
                                                'time':timeNow()
                                            }
                                        }
                                    )
                            if covidUpdate.modified_count != None:
                                code = 2000
                                status = True
                                message = "Your COVID-19 declaration has been submitted."
                            else:
                                code = 4555
                                status = False
                                message = "Your COVID-19 declaration could not be submitted."
                        elif len(covidCheck) == 0:
                            covidInsert = await self.covidDecl.insert_one(
                                            {
                                                'profileId':self.profileId,
                                                'entityId':self.entityId,
                                                'accountId':self.accountId,
                                                'serviceType':1,
                                                'covid19Declaration':True,
                                                'time':timeNow()
                                            }
                                        )
                            code = 2000
                            status = True
                            message = "Your COVID-19 declaration has been submitted."

                        #Need to check if this situation comes
                        else:
                            code = 2000
                            status = True
                            message = "COVID-19 declaration is already submitted."
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

    async def get(self):

        status = False
        code = 4000
        result = []
        message = ''


        try:

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
                    Log.i(self.apiId)
                    if self.apiId in [ 402020, 402022, 402021, 402023]:
                        '''
                        try:
                            serviceType = int(self.request.arguments['serviceType'][0])
                        except:
                            code = 4500
                            status = False
                            message = "Invalid Service Type"
                            raise Exception
                        '''
                        covidFindQ = self.covidDecl.find(
                                        {
                                            'profileId':self.profileId,
                                            'serviceType':1
                                        }
                                    )
                        covidFind = []
                        async for i in covidFindQ:
                            covidFind.append(i)
                        if len(covidFind):
                            v = {
                                    'id':str(covidFind[0]['_id']),
                                    'profileId':str(covidFind[0]['profileId']),
                                    'time':covidFind[0]['time'],
                                    'serviceType':covidFind[0]['serviceType'],
                                    'covid19Declaration':covidFind[0]['covid19Declaration']
                                }
                            result.append(v)
                            code = 2000
                            status = True
                        else:
                            code = 4500
                            status = False
                            message = "No Data Found."
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
