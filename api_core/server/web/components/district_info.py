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
import requests
import http.client
@xenSecureV1
class MtimeDistrictInfoHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ('GET','POST','PUT','DELETE','OPTIONS')

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
    allIndiaPincode = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][7]['name']
                ]

    stateDb = MongoMixin.userDb[
                    'state'
                ]

    districtDb = MongoMixin.userDb[
                    'district'
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
                    if app[0]['apiId'] in [ 402020, 402021,402022, 402023]: # TODO: till here
                        if True:

                            try:
                                allQ = int(self.request.arguments['all'][0].decode())
                            except:
                                allQ = False

                            if allQ:
                                # TODO: country code is hard codded
                                allD = self.districtDb.find(
                                            {
                                                'country.isoAlpha3Code': 'IND'
                                            }
                                        )
                                async for i in allD:
                                    del i['_id']
                                    result.append(i)

                                if not len(result):
                                    self.write(
                                        {
                                            'result': [],
                                            'status': False,
                                            'message': 'No district found for {}'.format('IND'),
                                            'code': 4420
                                        }
                                    )
                                    self.finish()
                                    return

                                self.write(
                                    {
                                        'result': result,
                                        'status': True,
                                        'message': 'All district of {}'.format('IND'),
                                        'code': 2000
                                    }
                                )
                                self.finish()
                                return

                            #nicURL = "http://districts.gov.in"
                            try:
                                state = self.request.arguments['state'][0].decode()
                            except:
                                code = 4658
                                status = False
                                message = "State Not Selected"
                                raise Exception

                            state = state.upper()
                            #requestURL = "/doi_service/rest.php/district/" + state + "/json"
                            #fullURL = nicURL + requestURL
                            try:
                                # TODO: country code is hard codded
                                allD = self.districtDb.find(
                                            {
                                                'country.isoAlpha3Code': 'IND',
                                                'state.code': state,
                                            }
                                        )
                                async for i in allD:
                                    del i['_id']
                                    result.append(i)
                            except:
                                code = 3299
                                status = False
                                message = "No Districts Found. Failure to Fetch"
                                raise Exception
                            if len(result):
                                code = 2000
                                status = True
                                message = "Districts Found"
                            else:
                                code = 4004
                                status = False
                                message = "No Districts Found"
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
