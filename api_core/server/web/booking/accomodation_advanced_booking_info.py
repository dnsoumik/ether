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
from datetime import datetime
from datetime import timezone
import datetime
from calendar import monthrange

@xenSecureV1
class MtimeAccomodationAdvancedBookingInfoHandler(tornado.web.RequestHandler,
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
                        if self.apiId in [402022,402023]:
                            try:
                                bookingId = str(self.request.arguments['id'][0].decode())
                                try:
                                    bookingId = ObjectId(bookingId)
                                except:
                                    raise Exception
                            except:
                                bookingId = None

                            resQuery = {}
                            if bookingId:
                                resQuery['_id'] = bookingId
                                resQuery['bookType'] = 0
                                resQ = self.touristBook.find(
                                            resQuery
                                        )
                                res = []
                                async for i in resQ:
                                    res.append(i)
                            else:
                                try:
                                    month = int(self.request.arguments['month'][0])
                                except:
                                    month = None
                                try:
                                    year = int(self.request.arguments['year'][0])
                                except:
                                    year = None
                                if month == None or year == None:
                                    currentTime = timeNow()
                                    currentTime = int(currentTime/1000000)
                                    ct = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d')
                                    currentDate = list(ct.split ("-"))
                                    year = int(currentDate[0])
                                    month = int(currentDate[1])
                                try:
                                    noOfDays = list((monthrange(year, month)))
                                except:
                                    message = 'Invalid month or year has given'
                                    self.write(
                                            {
                                                'status': False,
                                                'code': 4232,
                                                'result': [],
                                                'message': message
                                            }
                                        )
                                    self.finish()
                                    return

                                lastDate = int(noOfDays[1])

                                startDate = datetime.datetime(year, month, 1, 0, 0, 0)
                                timestamp = startDate.replace(tzinfo=timezone.utc).timestamp()
                                #startTimeStamp = int(timestamp) - 19800#10 digit timestamp
                                startTimeStamp = int(timestamp) * 1000000
                                endDate = datetime.datetime(year, month, lastDate, 0, 0, 0)
                                timestamp = endDate.replace(tzinfo=timezone.utc).timestamp()
                                #endTimeStamp = int(timestamp) - 19800#10 digit timestamp
                                endTimeStamp = int(timestamp) * 1000000
                                if True:
                                    resQuery['bookType'] = 0
                                    resQuery['$where'] = 'this.activity[this.activity.length - 1].id != 0 \
                                            && this.touristCount > 0'
                                    resQuery['activity.0.startTime'] = {'$gte':startTimeStamp,'$lte':endTimeStamp}
                                    resQ = self.touristBook.find(
                                            resQuery
                                        )
                                    res = []
                                    async for i in resQ:
                                        res.append(i)
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

