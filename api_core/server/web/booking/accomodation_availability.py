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


@xenSecureV1
class MtimeWebAccomodationAvailablityHandler(tornado.web.RequestHandler,
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

    touristBook = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][19]['name']
                ]
    touristPass = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][20]['name']
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
                    if app[0]['apiId'] in [ 402020, 402021, 402022]: # TODO: till here
                        if self.apiId == 402020:

                            try:
                                serviceAccountId = str(self.request.arguments['id'][0].decode())
                                try:
                                    serviceAccountId = ObjectId(serviceAccountId)
                                except:
                                    raise Exception
                            except:
                                code = 7378
                                status = False
                                message = "Invalid Argument - ['serviceAccountId']"
                                raise Exception

                            try:
                                availabilityTime = int(self.request.arguments['availabilityTime'][0].decode())
                            except:
                                code = 7378
                                status = False
                                message = "Invalid availablity time"
                                raise Exception

                            '''
                            #For Future Use
                            try:
                                noOfGuest = int(self.request.arguments['noOfGuest'][0].decode())
                            except:
                                code = 7378
                                status = False
                                message = "Invalid input for number of guests"
                                raise Exception
                            try:
                                noOfRoom = int(self.request.arguments['noOfRoom'][0].decode())
                            except:
                                code = 7378
                                status = False
                                message = "Invalid input for number of rooms"
                                raise Exception
                            '''


                            if True:
                                bookTimeN = int(availabilityTime/1000000)
                                st = datetime.datetime.fromtimestamp(bookTimeN).strftime('%Y-%m-%d')
                                dateList = list(st.split ("-"))
                                dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                                dayTimeStamp = int(timestamp * 1000000) - 19800000000


                                accSessionFindQ = self.accSession.find(
                                                    {
                                                        'serviceAccountId':serviceAccountId,
                                                        'serviceType':1,
                                                        'entityId':self.entityId,
                                                        'dayTimeStamp':dayTimeStamp
                                                    }
                                                )

                                accSessionFind = []
                                async for i in accSessionFindQ:
                                    accSessionFind.append(i)


                                if len(accSessionFind):
                                    v = {
                                            'id': str(accSessionFind[0]['_id']),
                                            'inventoryInformation':accSessionFind[0]['inventoryInformation'],
                                            'time':accSessionFind[0]['time'],
                                            'modifiedTime':accSessionFind[0]['modifiedTime']
                                        }
                                    result.append(v)
                                else:
                                    accSessionFindQ = self.inventory.find(
                                                        {
                                                            'serviceAccountId':serviceAccountId,
                                                            'serviceType':1,
                                                            'entityId':self.entityId
                                                        }
                                                    )
                                    accSessionFind = []
                                    async for i in accSessionFindQ:
                                        accSessionFind.append(i)

                                    if len(accSessionFind):
                                        v = {
                                                'id': str(accSessionFind[0]['_id']),
                                                'inventoryInformation':accSessionFind[0]['inventoryInformation'],
                                                'time':accSessionFind[0]['time'],
                                                'modifiedTime':accSessionFind[0]['modifiedTime']
                                            }
                                        result.append(v)

                                if len(result):
                                    code = 2000
                                    status = True
                                    message = "Inventory Information"
                                else:
                                    code = 4004
                                    status = True
                                    message = "No Inventory Information Found"
                        elif self.apiId == 402021:
                            try:
                                availabilityTime = int(self.request.arguments['availabilityTime'][0].decode())
                            except:
                                code = 7378
                                status = False
                                message = "Invalid availablity time"
                                raise Exception


                            if True:
                                bookTimeN = int(availabilityTime/1000000)
                                st = datetime.datetime.fromtimestamp(bookTimeN).strftime('%Y-%m-%d')
                                dateList = list(st.split ("-"))
                                dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                                dayTimeStamp = int(timestamp * 1000000) - 19800000000


                                accSessionFindQ = self.accSession.find(
                                                    {
                                                        'profileId':self.profileId,
                                                        'serviceType':1,
                                                        'entityId':self.entityId,
                                                        'dayTimeStamp':dayTimeStamp
                                                    }
                                                )

                                accSessionFind = []
                                async for i in accSessionFindQ:
                                    accSessionFind.append(i)


                                if len(accSessionFind):
                                    inventoryInfo = []
                                    for j in accSessionFind[0]['inventoryInformation']:
                                        if j['active'] == False:
                                            j['availableQuantity'] = 0
                                        if j['confirmBook'] > 0 or j['active'] == True:
                                            inventoryInfo.append(j)
                                    v = {
                                            'id': str(accSessionFind[0]['_id']),
                                            #'inventoryInformation':accSessionFind[0]['inventoryInformation'],
                                            'inventoryInformation':inventoryInfo,
                                            'time':accSessionFind[0]['time'],
                                            'modifiedTime':accSessionFind[0]['modifiedTime']
                                        }
                                    result.append(v)
                                else:
                                    accSessionFindQ = self.inventory.find(
                                                        {
                                                            'profileId':self.profileId,
                                                            'serviceType':1,
                                                            'entityId':self.entityId
                                                        }
                                                    )
                                    accSessionFind = []
                                    async for i in accSessionFindQ:
                                        accSessionFind.append(i)

                                    if len(accSessionFind):
                                        inventoryInfo = []
                                        for j in accSessionFind[0]['inventoryInformation']:
                                            if j['active'] == False:
                                                j['availableQuantity'] = 0
                                            if j['confirmBook'] > 0 or j['active'] == True:
                                                inventoryInfo.append(j)
                                        v = {
                                                'id': str(accSessionFind[0]['_id']),
                                                #'inventoryInformation':accSessionFind[0]['inventoryInformation'],
                                                'inventoryInformation':inventoryInfo,
                                                'time':accSessionFind[0]['time'],
                                                'modifiedTime':accSessionFind[0]['modifiedTime']
                                            }
                                        result.append(v)

                                if len(result):
                                    code = 2000
                                    status = True
                                    message = "Inventory Information"
                                else:
                                    code = 4004
                                    status = True
                                    message = "No Inventory Information Found"
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

