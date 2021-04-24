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
class MtimeWebBookingDetailsGetHandler(tornado.web.RequestHandler,
                                       MongoMixin):

    SUPPORTED_METHODS = ('GET')

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
    touristKyc = MongoMixin.serviceDb[
        CONFIG['database'][1]['table'][16]['name']
    ]
    subTourist = MongoMixin.serviceDb[
        CONFIG['database'][1]['table'][17]['name']
    ]
    imgWrite = MongoMixin.serviceDb[
        CONFIG['database'][1]['table'][18]['name']
    ]
    touristBook = MongoMixin.serviceDb[
        CONFIG['database'][1]['table'][19]['name']
    ]

    fu = FileUtil()

    async def get(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            bookingId = ObjectId(self.request.arguments['id'][0])
        except:
            bookingId = None

        try:
            activityId = int(self.request.arguments['activityId'][0])
        except Exception as e:
            activityId = None

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
                    if app[0]['apiId'] in [402021, 402022]:  # TODO: till here

                        if self.apiId == 402022:
                            if bookingId == None:
                                resQ = self.touristBook.find(
                                    {
                                        'entityId': self.entityId,
                                        # '$where': 'this.activity[this.activity.length - 1].id > 0'#original
                                        # extra
                                        '$where': 'this.activity[this.activity.length - 1].id >= 0'
                                    }
                                )
                                res = []
                                async for r in resQ:
                                    res.append(r)

                            else:
                                resQ = self.touristBook.find(
                                    {
                                        '_id': ObjectId(bookingId),
                                        'entityId': self.entityId,
                                        # '$where': 'this.activity[this.activity.length - 1].id > 0'#original
                                        # extra
                                        '$where': 'this.activity[this.activity.length - 1].id > 0'
                                    }
                                )
                                res = []
                                async for r in resQ:
                                    res.append(r)

                            if len(res):
                                for bookInfo in res:
                                    v = {
                                        '_id': str(bookInfo['_id']),
                                        'entityId': str(bookInfo['entityId']),
                                        'disabled': bookInfo['disabled'],
                                        'activity': bookInfo['activity'],
                                        'touristDetails': bookInfo['touristDetails']
                                    }
                                    for mem in bookInfo['touristDetails']:
                                        for docx in mem['documents']:
                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                + str(self.entityId) + '/tourist_kyc/' \
                                                + 'subtourist/' + str(mem['id']) \
                                                + '/' + \
                                                str(docx['time']) + \
                                                docx['mimeType']
                                        for docx in mem['faceProof']:
                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                + str(self.entityId) + '/tourist_kyc/' \
                                                + 'subtourist/' + str(mem['id']) \
                                                + '/' + \
                                                str(docx['time']) + \
                                                docx['mimeType']
                                        for docx in mem['liveProof']:
                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                + str(self.entityId) + '/tourist_kyc/' \
                                                + 'subtourist/' + str(mem['id']) \
                                                + '/' + \
                                                str(docx['time']) + \
                                                docx['mimeType']
                                    proDtQ = self.account.find(
                                        {
                                            '_id': bookInfo['providerDetails'][0]['accountId']
                                        },
                                        {
                                            '_id': 1,
                                            'firstName': 1,
                                            'lastName': 1,
                                            'contact': 1
                                        }
                                    )
                                    proDt = []
                                    async for r in proDtQ:
                                        proDt.append(r)

                                    hotelInfoQ = self.serviceAccount.find(
                                        {
                                            'profileId': bookInfo['providerDetails'][0]['id']
                                        }
                                    )
                                    hotelInfo = []
                                    async for r in hotelInfoQ:
                                        hotelInfo.append(r)

                                    if len(proDt):
                                        proDt[0]['id'] = str(proDt[0]['_id'])
                                        del proDt[0]['_id']
                                        v['providerDetails'] = proDt
                                        if len(hotelInfo):
                                            proDt[0]['hotelName'] = hotelInfo[0]['hotelInfo'][0]['hotelName']
                                    else:
                                        v['providerDetails'] = []
                                    result.append(v)
                                code = 2000
                                status = True
                            else:
                                code = 4121
                                status = False
                                message = "No data Found"

                        elif self.apiId == 402021:
                            code, message = Validate.i(
                                activityId,
                                'activityId',
                                dataType=int,
                                minNumber=0,
                                maxNumber=10
                            )
                            if code != 4100:
                                raise Exception

                            # TODO: for activity ID
                            if bookingId:
                                resQ = self.touristBook.find(
                                    {
                                        '_id': bookingId,
                                        'entityId': self.entityId,
                                        'providerDetails.0.id': self.profileId,
                                    }
                                )
                                res = []
                                async for r in resQ:
                                    res.append(r)

                            else:
                                resQ = self.touristBook.find(
                                    {
                                        'entityId': self.entityId,
                                        'providerDetails.0.id': self.profileId,
                                    }
                                )
                                res = []
                                async for r in resQ:
                                    res.append(r)

                            if len(res):
                                for bookInfo in res:
                                    v = {
                                        'id': str(bookInfo['_id']),
                                        'entityId': str(bookInfo['entityId']),
                                        'disabled': bookInfo['disabled'],
                                        'activity': bookInfo['activity']
                                    }
                                    if bookingId:
                                        v['touristDetails'] = bookInfo['touristDetails']
                                        for mem in bookInfo['touristDetails']:
                                            for docx in mem['documents']:
                                                docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                    + str(self.entityId) + '/tourist_kyc/' \
                                                    + 'subtourist/' + str(mem['id']) \
                                                    + '/' + \
                                                    str(docx['time']) + \
                                                    docx['mimeType']
                                            for docx in mem['faceProof']:
                                                docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                    + str(self.entityId) + '/tourist_kyc/' \
                                                    + 'subtourist/' + str(mem['id']) \
                                                    + '/' + \
                                                    str(docx['time']) + \
                                                    docx['mimeType']
                                            for docx in mem['liveProof']:
                                                docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                    + str(self.entityId) + '/tourist_kyc/' \
                                                    + 'subtourist/' + str(mem['id']) \
                                                    + '/' + \
                                                    str(docx['time']) + \
                                                    docx['mimeType']
                                    else:
                                        v['totalTourist'] = len(
                                            bookInfo['touristDetails'])
                                    result.append(v)
                                # Reversing Array
                                result.reverse()
                                code = 2000
                                status = True
                            else:
                                code = 4121
                                status = False
                                message = "No data Found"
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
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' +
                      str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response = {
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
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' +
                  str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response = {
                'code': code,
                'status': status,
                'message': message
            }
            self.write(response)
            self.finish()
            return
