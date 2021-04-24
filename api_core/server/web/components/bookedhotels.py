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
from datetime import timezone
import datetime
from datetime import date
import csv
from collections import OrderedDict


@xenSecureV1
class MtimeBookedHotelsHandler(tornado.web.RequestHandler,
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
    state = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][8]['name']
                ]

    serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][0]['name']
                ]
    subTourist = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][17]['name']
                ]
    touristPassV2 = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][38]['name']
                ]
    touristBook = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][19]['name']
                ]
    touristPassStatus = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][43]['name']
                ]
    state = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][8]['name']
                ]
    accDomReport = MongoMixin.reportDb[
                    CONFIG['database'][2]['table'][0]['name']
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
                    if app[0]['apiId'] in [ 402020, 402022, 402021,402023]: # TODO: till here
                        if self.apiId in [402023,402022]:
                            query = {
                                                '$where':'(this.touristCount > 0 && \
                                                        this.activity[this.activity.length - 1].id !=0 && this.activity[this.activity.length - 1].id <20)'
                                    }
                            bookFindQ = await self.touristBook.distinct("serviceAccountId",query)
                            for i in bookFindQ:
                                serAccFind = await self.serviceAccount.find_one({"_id":i})
                                if serAccFind:
                                    v = {
                                            'id':str(i),
                                            'hotelName':serAccFind['propertyInfo'][0]['propertyName']
                                        }
                                    result.append(v)
                            if len(result):
                                code = 2000
                                status = True
                                message = "List of Booked Hotels"
                            else:
                                code = 4004
                                status = False
                                message = "No Booked Hotels Found"
                                raise Exception
                        elif self.apiId == 402021:
                            code = 2000
                            status = True
                            message = "API Not Yet Implemented"
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

