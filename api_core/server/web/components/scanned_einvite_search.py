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
from baseconvert import base
from ..lib.lib import *
from datetime import timezone
from datetime import date
import datetime


@xenSecureV1
class ScannedEinviteSearchHandler(tornado.web.RequestHandler,
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
    touristKyc = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][16]['name']
                ]
    subTourist = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][17]['name']
                ]
    touristPassV2 = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][38]['name']
                ]
    touristPassStatus = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][43]['name']
                ]
    touristPass = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][20]['name']
                ]
    touristBook = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][19]['name']
                ]
    fu = FileUtil()
    def options(self):
        self.set_status(200)
        self.write({})
        self.finish()
        return



    async def get(self):
        msgquery = []
        status = False
        code = 4000
        result = []
        message = ''
        passCount = 0
        passId = None



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
                    Log.i('api-ID',self.apiId)
                    if app[0]['apiId'] in [ 402020, 402022, 402021, 402023]: # TODO: till here
                        if self.apiId == 402022 or self.apiId == 402023:
                            try:
                                aRegex = str(self.request.arguments['regex'][0].decode())
                            except:
                                code = 9302
                                status = False
                                message = "Please submit valid search keyword"
                                raise Exception
                            state = None
                            try:
                                limit = int(self.get_arguments('limit')[0])
                                skip = int(self.get_arguments('skip')[0])
                                f_state = True
                            except:
                                f_state = False
                            res = []

                            query = {
                                        '$or':[
                                                {
                                                    "passIdn":{
                                                                '$regex':aRegex.upper(),
                                                                "$options":'i'
                                                                }
                                                },
                                                {
                                                    "activity.locationName":{
                                                                                '$regex':aRegex,
                                                                                "$options":'i'
                                                                            }
                                                },
                                        ]
                                    }
                            if f_state == True:
                                resQ = self.touristPassStatus.find(query,limit=limit,skip=skip).sort('_id',-1)
                                async for i in resQ:
                                    res.append(i)
                            else:
                                resQ = self.touristPassStatus.find(query)
                                async for i in resQ:
                                    res.append(i)
                            passCount = await self.touristPassStatus.count_documents(query)
                            if not len(res):
                                profiles = []
                                if aRegex.isnumeric():
                                    if len(aRegex) != 10:
                                        code = 2090
                                        status = False
                                        message = "Please enter valid 10-digit phone number"
                                        raise Exception
                                    numCheck = int(910000000000 + int(aRegex))
                                    accFind = await self.account.find_one({"contact.0.value":numCheck})
                                    if accFind:
                                        proFind = await self.profile.find_one({"accountId":accFind['_id']})
                                        if proFind:
                                            profiles.append(proFind['_id'])
                                else:
                                    accFindQ = self.account.find(
                                        {
                                            '$or': [
                                                {
                                                    "firstName": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                },
                                                {
                                                    "lastName": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                }
                                            ]
                                        }
                                    )
                                    accFind = []
                                    async for i in accFindQ:
                                        accFind.append(i['_id'])
                                    if len(accFind):
                                        proFindQ = self.profile.find(
                                                    {
                                                        'accountId':{'$in':accFind}
                                                    }
                                                )
                                        async for i in proFindQ:
                                            profiles.append(i['_id'])
                                if f_state == True:
                                    resQ = self.touristPassStatus.find({"profileId":{'$in':profiles}},limit=limit,skip=skip).sort('_id',-1)
                                else:
                                    resQ = self.touristPassStatus.find({"profileId":{'$in':profiles}})
                                async for i in resQ:
                                    res.append(i)
                                passCount = await self.touristPassStatus.count_documents({"profileId":{'$in':profiles}})
                            if len(res):
                                if state != None:
                                    passFindQ = self.touristPassV2.find(
                                                {
                                                    '_id':passInfo['passId'],
                                                    'passIdn':passInfo['passIdn'],
                                                    'travelState':{
                                                                    "$in":state
                                                                 }
                                                }
                                            )
                                    passFind = []
                                    async for i in passFindQ:
                                        passFind.append(i)
                                    passCount = len(passFind)
                                    if len(passFind):
                                        for passInfo in res:
                                            v = {
                                                    'id':str(passInfo['_id']),
                                                    'profileId':str(passInfo['touristProfileId']),
                                                    'passId':str(passInfo['passId']),
                                                    'passIdn':str(passInfo['passIdn']),
                                                    'time':passInfo['time'],
                                                    'modifiedTime':passInfo['modifiedTime']
                                                }
                                            activity = []
                                            for j in passInfo['activity']:
                                                x = {
                                                        'location':j['location'],
                                                        'time':j['time'],
                                                        'id':j['id'],
                                                        'locationName':j['locationName']
                                                    }
                                                activity.append(x)
                                            v['activity'] = activity
                                            v['firstName'] = ""
                                            v['lastName'] = ""
                                            v['contact'] = ""
                                            proFindQ = self.profile.find(
                                                    {
                                                        '_id':passInfo['touristProfileId'],
                                                        'entityId':self.entityId
                                                    }
                                                )
                                            proFind = []
                                            async for i in proFindQ:
                                                proFind.append(i)
                                            if len(proFind):
                                                accFindQ = self.account.find(
                                                        {
                                                            '_id':proFind[0]['accountId']
                                                        }
                                                    )
                                                accFind = []
                                                async for i in accFindQ:
                                                    accFind.append(i)
                                                if len(accFind):
                                                    v['firstName'] = accFind[0]['firstName']
                                                    v['lastName'] = accFind[0]['lastName']
                                                    v['contact'] = accFind[0]['contact'][0]['value']
                                            result.append(v)
                                else:
                                    for passInfo in res:
                                        v = {
                                                'id':str(passInfo['_id']),
                                                'profileId':str(passInfo['touristProfileId']),
                                                'passId':str(passInfo['passId']),
                                                'passIdn':str(passInfo['passIdn']),
                                                'time':passInfo['time'],
                                                'modifiedTime':passInfo['modifiedTime']
                                            }
                                        activity = []
                                        for j in passInfo['activity']:
                                            x = {
                                                    'location':j['location'],
                                                    'time':j['time'],
                                                    'id':j['id'],
                                                    'locationName':j['locationName']
                                                }
                                            activity.append(x)
                                        v['activity'] = activity
                                        v['firstName'] = ""
                                        v['lastName'] = ""
                                        v['contact'] = ""
                                        proFindQ = self.profile.find(
                                                    {
                                                        '_id':passInfo['touristProfileId'],
                                                        'entityId':self.entityId
                                                    }
                                                )
                                        proFind = []
                                        async for i in proFindQ:
                                            proFind.append(i)
                                        if len(proFind):
                                            accFindQ = self.account.find(
                                                        {
                                                            '_id':proFind[0]['accountId']
                                                        }
                                                    )
                                            accFind = []
                                            async for i in accFindQ:
                                                accFind.append(i)
                                            if len(accFind):
                                                v['firstName'] = accFind[0]['firstName']
                                                v['lastName'] = accFind[0]['lastName']
                                                v['contact'] = accFind[0]['contact'][0]['value']
                                        result.append(v)
                                result = sorted(result, key = lambda i: i['modifiedTime'])
                                result.reverse()
                                code = 2000
                                status = True
                                message = "List of scanned e-invites"
                            else:
                                code = 4650
                                status = False
                                message = "No Data Found"
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
                    'message': message,
                    'filterData':msgquery
                }
        Log.d('RSP', response)
        try:
            response['result'] = result
            response['count'] = passCount
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

