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
import numpy
import numpy as np
import pathlib

@xenSecureV1
class MtimeAccomodationInfoHandler(tornado.web.RequestHandler,
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
    phoneCountry = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][6]['name']
                ]
    entity = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][5]['name']
                ]

    serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][0]['name']
                ]
    subTourist = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][17]['name']
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
                    if self.apiId in [ 402021, 402022, 402023]:
                        Log.i(self.apiId)
                        if self.apiId == 402021:
                            try:
                                bookingId = str(self.request.arguments['id'][0].decode())
                                try:
                                    bookingId = ObjectId(bookingId)
                                except:
                                    raise Exception
                            except:
                                bookingId = None

                            try:
                                activityId = int(self.request.arguments['activityId'][0])
                            except Exception as e:
                                activityId = None

                            resQuery = {}
                            if bookingId:
                                resQuery['_id'] = bookingId
                                resQuery['providerDetails.id'] = self.profileId
                                if activityId != None:
                                    resQuery['$where'] = 'this.activity[this.activity.length - 1].id =={} \
                                            && this.touristCount > 0'.format(activityId)
                                resQ = self.touristBook.find(
                                            resQuery
                                        )
                                res = []
                                async for i in resQ:
                                    res.append(i)
                            else:
                                if activityId != None:
                                    resQuery['providerDetails.id'] = self.profileId
                                    resQuery['$where'] = 'this.activity[this.activity.length - 1].id =={} \
                                            && this.touristCount > 0'.format(activityId)
                                resQ = self.touristBook.find(
                                            resQuery
                                    )
                                res = []
                                async for i in resQ:
                                    res.append(i)
                            if len(res):
                                for bookInfo in res:
                                    Log.i('TOURIST COUNT - ', bookInfo['touristCount'])
                                    v = {
                                            'id': str(bookInfo['_id']),
                                            'entityId':str(bookInfo['entityId']),
                                            'disabled':bookInfo['disabled'],
                                            'activity':bookInfo['activity'],
                                            'touristCount':bookInfo['touristCount'],
                                            'touristId':str(bookInfo['touristId']),
                                            'noOfDays':bookInfo.get('noOfDays'),
                                            'time': bookInfo['time']
                                        }
                                    if type(bookInfo['primaryTouristInfo']) is dict:
                                        v['primaryTouristInfo'] = [bookInfo['primaryTouristInfo']]
                                    else:
                                        v['primaryTouristInfo'] = bookInfo['primaryTouristInfo']
                                    if v['primaryTouristInfo'][0].get('_id') != None:
                                        del v['primaryTouristInfo'][0]['_id']
                                    if bookingId:
                                        v['touristDetails'] = bookInfo['touristDetails']
                                        if len(bookInfo['touristDetails']):
                                            for mem in bookInfo['touristDetails']:
                                                for docx in mem['documents']:
                                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) + '/tourist_kyc/' \
                                                        + 'subtourist/' + str(mem['id']) \
                                                        + '/' + str(docx['time']) + docx['mimeType']
                                                for docx in mem['faceProof']:
                                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) + '/tourist_kyc/' \
                                                        + 'subtourist/' + str(mem['id']) \
                                                        + '/' + str(docx['time']) + docx['mimeType']
                                                for docx in mem['liveProof']:
                                                    if docx['mimeType'] == None:
                                                        docx['link'] = None
                                                    else:
                                                        docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                            + str(self.entityId) + '/tourist_kyc/' \
                                                            + 'subtourist/' + str(mem['id']) \
                                                            + '/' + str(docx['time']) + docx['mimeType']
                                                if len(mem['liveProof2']):
                                                    for docx in mem['liveProof2']:
                                                        if docx['mimeType'] == None:
                                                            docx['link'] = None
                                                        else:
                                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                                + str(self.entityId) + '/tourist_kyc/' \
                                                                + 'subtourist/' + str(mem['id']) \
                                                                + '/' + str(docx['time']) + docx['mimeType']
                                    else:
                                        v['totalTourist'] = len(bookInfo['touristDetails'])
                                    result.append(v)
                                result.reverse()
                                status = True
                                message = "Data Found"
                            else:
                                code = 4004
                                status = False
                                message = "No Data Found"
                                raise Exception
                        elif self.apiId in [402022,402023]:
                            f_state = False
                            try:
                                f_limit = int(self.get_arguments('limit')[0])
                                f_skip = int(self.get_arguments('skip')[0])
                                f_state = True
                            except:
                                f_state = False
                            try:
                                bookingId = str(self.request.arguments['id'][0].decode())
                                try:
                                    bookingId = ObjectId(bookingId)
                                except:
                                    raise Exception
                            except:
                                bookingId = None

                            try:
                                activityId = int(self.request.arguments['activityId'][0])
                            except Exception as e:
                                activityId = None

                            resQuery = {}
                            if bookingId:
                                resQuery['_id'] = bookingId
                                if activityId != None:
                                    resQuery['$where'] = 'this.activity[this.activity.length - 1].id =={} \
                                            && this.touristCount > 0'.format(activityId)
                                resQ = self.touristBook.find(
                                            resQuery
                                        )
                                res = []
                                async for i in resQ:
                                    res.append(i)
                            else:
                                if activityId != None:
                                    if activityId == 8:
                                        resQuery['$where'] = 'this.activity[this.activity.length - 1].id =={} \
                                                && this.touristCount > 0'.format(activityId)
                                    elif activityId in [1,2,3]:
                                        activityId = 3
                                        resQuery['$where'] = 'this.activity[this.activity.length - 1].id <={} \
                                                && this.activity[this.activity.length - 1].id <= 1 && this.touristCount > 0'.format(activityId)
                                    elif activityId == 0:
                                        '''
                                        resQuery['$where'] = 'this.activity[this.activity.length - 1].id =={} \
                                                && this.touristCount > 0 || this.activity[this.activity.length - 1].id == 3'.format(activityId)
                                        '''
                                        resQuery['$where'] = 'this.touristCount > 0 && this.activity[this.activity.length - 1].id == 3'
                                    if f_state:
                                        if activityId == 0:
                                            resQ = self.touristBook.find(
                                                resQuery,
                                            )
                                        else:
                                            resQ = self.touristBook.find(
                                                resQuery,
                                                limit=f_limit,
                                                skip=f_skip
                                            )
                                    else:
                                        resQ = self.touristBook.find(
                                            resQuery,
                                        )
                                    res = []
                                    async for i in resQ:
                                        res.append(i)
                                else:
                                    code = 8911
                                    status = False
                                    message = "Missing Argument - ['activityId']"
                                    raise Exception
                            if len(res):
                                for bookInfo in res:
                                    try:
                                        inventory = bookInfo['inventory']
                                    except:
                                        inventory = []
                                    try:
                                        payment = bookInfo['payment']
                                    except:
                                        payment = []
                                    Log.i('TOURIST COUNT - ', bookInfo['touristCount'])
                                    v = {
                                            'id': str(bookInfo['_id']),
                                            'entityId':str(bookInfo['entityId']),
                                            'disabled':bookInfo['disabled'],
                                            'activity':bookInfo['activity'],
                                            'touristCount':bookInfo['touristCount'],
                                            'touristId':str(bookInfo['touristId']),
                                            'inventory':inventory,
                                            'noOfDays':bookInfo.get('noOfDays'),
                                            'payment':payment,
                                            'time': bookInfo['time']
                                        }
                                    if type(bookInfo['primaryTouristInfo']) is dict:
                                        v['primaryTouristInfo'] = [bookInfo['primaryTouristInfo']]
                                    else:
                                        v['primaryTouristInfo'] = bookInfo['primaryTouristInfo']
                                    if v['primaryTouristInfo'][0].get('_id') != None:
                                        del v['primaryTouristInfo'][0]['_id']
                                    proDtQ = self.account.find(
                                                {
                                                    '_id':bookInfo['providerDetails'][0]['accountId']
                                                },
                                                {
                                                    '_id': 1,
                                                    'firstName':1,
                                                    'lastName':1,
                                                    'contact':1
                                                }
                                            )
                                    proDt = []
                                    async for i in proDtQ:
                                        proDt.append(i)
                                    hotelInfoQ = self.serviceAccount.find(
                                                {
                                                    'profileId':bookInfo['providerDetails'][0]['id'],
                                                    'serviceType':1
                                                }
                                            )
                                    hotelInfo = []
                                    async for i in hotelInfoQ:
                                        hotelInfo.append(i)
                                    if len(proDt):
                                        proDt[0]['id'] = str(proDt[0]['_id'])
                                        del proDt[0]['_id']
                                        v['providerDetails'] = proDt
                                        if len(hotelInfo):
                                            proDt[0]['hotelName'] = hotelInfo[0]['propertyInfo'][0]['propertyName']
                                        else:
                                            proDt[0]['hotelName'] = "Not Available"
                                    else:
                                        v['providerDetails'] = []
                                    if bookingId:
                                        v['touristDetails'] = bookInfo['touristDetails']
                                        if len(bookInfo['touristDetails']):
                                            for mem in bookInfo['touristDetails']:
                                                for docx in mem['documents']:
                                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) + '/tourist_kyc/' \
                                                        + 'subtourist/' + str(mem['id']) \
                                                        + '/' + str(docx['time']) + docx['mimeType']
                                                for docx in mem['faceProof']:
                                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) + '/tourist_kyc/' \
                                                        + 'subtourist/' + str(mem['id']) \
                                                        + '/' + str(docx['time']) + docx['mimeType']
                                                for docx in mem['liveProof']:
                                                    if docx['mimeType'] == None:
                                                        docx['link'] = None
                                                    else:
                                                        docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                            + str(self.entityId) + '/tourist_kyc/' \
                                                            + 'subtourist/' + str(mem['id']) \
                                                            + '/' + str(docx['time']) + docx['mimeType']
                                                if len(mem['liveProof2']):
                                                    for docx in mem['liveProof2']:
                                                        if docx['mimeType'] == None:
                                                            docx['link'] = None
                                                        else:
                                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                                + str(self.entityId) + '/tourist_kyc/' \
                                                                + 'subtourist/' + str(mem['id']) \
                                                                + '/' + str(docx['time']) + docx['mimeType']
                                    else:
                                        v['totalTourist'] = len(bookInfo['touristDetails'])
                                    result.append(v)
                                status = True
                                message = "Data Found"
                                result.reverse()
                            else:
                                code = 4004
                                status = False
                                message = "No Data Found"
                                raise Exception
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
            response['lenResult'] = len(result)
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

