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
class MtimeWebTagsRegexGetHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ('GET','OPTIONS')

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
    tags = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][31]['name']
                ]

    fu = FileUtil()
    def options(self):
        self.set_status(200)
        self.write({})
        self.finish()
        return

    #@defer.inlineCallbacks
    async def get(self):

        status = False
        code = 4000
        result = []
        message = ''

        #try:
        #    hotelId = self.request.arguments['id'][0].decode()
        #except:
        #    hotelId = None

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
                    if app[0]['apiId'] in [ 402020, 402021, 402022,402023]: # TODO: till here
                        if self.apiId == 402020 or True:
                            if True:
                                try:
                                    aRegex = str(self.get_arguments('regex')[0])
                                    code, message = Validate.i(
                                        aRegex,
                                        'radius',
                                        maxLength=2000,
                                        minLength=0
                                    )
                                    if code != 4100:
                                        raise Exception
                                except:
                                    code = 4410
                                    message = 'Invalid Argument - [ regex ].'
                                    raise Exception

                                '''
                                try:
                                    aLongitude = float(self.get_arguments('longitude')[0])
                                    code, message = Validate.i(
                                            aLongitude,
                                            'longitude',
                                            maxNumber=180,
                                            minNumber=-180
                                        )
                                    if code != 4100:
                                        raise Exception
                                except Exception as e:
                                    code = 4210
                                    message = 'Invalid Argument - [ longitude ].'
                                    raise Exception

                                try:
                                    aLatitude = float(self.get_arguments('latitude')[0])
                                    code, message = Validate.i(
                                            aLatitude,
                                            'latitude',
                                            maxNumber=90,
                                            minNumber=-90
                                        )
                                    if code != 4100:
                                        raise Exception
                                except Exception as e:
                                    code = 4210
                                    message = 'Invalid Argument - [ latitude ].'
                                    raise Exception
                                '''
                                tagListQ = self.tags.find(
                                        {
                                            'entityId': self.entityId,
                                            'blocked':False,
                                            '$or': [
                                                {
                                                    "tagName": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                }
                                            ]
                                        },
                                        limit=10
                                    )

                                tagList = []
                                async for r in tagListQ:
                                    tagList.append(r)
                                if len(tagList):
                                    for res in tagList:
                                        v = {
                                                'tagName':res['tagName']
                                            }
                                        result.append(v)
                                    code = 2000
                                    status = True
                                    message = "List of Tags"
                                else:
                                    code = 4750
                                    status = False
                                    message = "No Tags Found"
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
