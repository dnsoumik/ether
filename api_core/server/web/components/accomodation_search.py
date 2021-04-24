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
class MtimeWebAccomodationSearchHandler(tornado.web.RequestHandler,
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
    covidDecl = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][29]['name']
                ]


    def options(self):
        self.set_status(200)
        self.write({})
        self.finish()
        return

    fu = FileUtil()

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
                    if app[0]['apiId'] in [ 402020, 402021, 402022, 402023]: # TODO: till here
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
                                try:
                                    disabled = int(self.get_arguments('disabled')[0])
                                except:
                                    disabled = 0
                                if disabled == 0:
                                    disabled = False
                                elif disabled == 1:
                                    disabled = True
                                f_state = False
                                try:
                                    f_limit = int(self.get_arguments('limit')[0])
                                    f_skip = int(self.get_arguments('skip')[0])
                                    f_state = True
                                except:
                                    f_state = False
                                if f_state:
                                    accListQ = self.serviceAccount.find(
                                        {
                                            #'entityId': self.entityId,
                                            'serviceType':1,
                                            'disabled':disabled,
                                            '$or': [
                                                {
                                                    "propertyInfo.propertyName": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                },
                                                {
                                                    "propertyInfo.propertyType": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                },
                                                {
                                                    "hotelInfo.district": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                },
                                                {
                                                    "hotelInfo.ownerName": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                },
                                                {
                                                    "hotelInfo.ownerNumber": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                },
                                            ]
                                        },
                                        limit=f_limit,
                                        skip=f_skip
                                    )
                                else:
                                    accListQ = self.serviceAccount.find(
                                        {
                                            #'entityId': self.entityId,
                                            'serviceType':1,
                                            'disabled':disabled,
                                            '$or': [
                                                {
                                                    "propertyInfo.propertyName": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                },
                                                {
                                                    "propertyInfo.propertyType": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                },
                                                {
                                                    "hotelInfo.district": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                },
                                                {
                                                    "hotelInfo.ownerName": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                },
                                                {
                                                    "hotelInfo.ownerNumber": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                },
                                            ]
                                        },
                                    )
                                accList = []
                                async for r in accListQ:
                                    accList.append(r)

                                applicationIdFindQ = self.applications.find(
                                                        {
                                                            'apiId':402021
                                                        }
                                                    )
                                applicationIdFind = []
                                async for i in applicationIdFindQ:
                                    applicationIdFind.append(i)

                                if not len(applicationIdFind):
                                    code = 9999
                                    status = False
                                    message = "Internal Error in Application. Please contact Support"
                                    raise Exception

                                if aRegex.isdigit():
                                    ownerNumberQ = self.serviceAccount.find(
                                                {
                                                    'serviceType':1,
                                                    'hotelInfo.ownerNumber':int(aRegex),
                                                    'disabled':False
                                                }
                                            )
                                    async for r in ownerNumberQ:
                                        accList.append(r)



                                    regNum = 910000000000 + int(aRegex)
                                    accFindQ = self.account.find(
                                                {
                                                    'contact.0.value':regNum
                                                }
                                            )
                                    accFind = []
                                    async for i in accFindQ:
                                        accFind.append(i)
                                    if len(accFind):
                                        proFindQ = self.profile.find(
                                                    {
                                                        'accountId':accFind[0]['_id'],
                                                        'entityId':self.entityId,
                                                        'applicationId':applicationIdFind[0]['_id']
                                                    }
                                                )
                                        proFind = []
                                        async for i in proFindQ:
                                            proFind.append(i)


                                        if len(proFind):
                                            serAccQ = self.serviceAccount.find(
                                                    {
                                                        'serviceType':1,
                                                        'profileId':proFind[0]['_id'],
                                                        'entityId':self.entityId,
                                                        'disabled':False
                                                    }
                                                )
                                            async for i in serAccQ:
                                                accList.append(i)

                                if len(accList):
                                    for res in accList:
                                        covFindQ = self.covidDecl.find(
                                                        {
                                                            'profileId':res['profileId'],
                                                            'serviceType':1
                                                        }
                                                    )
                                        covFind = []
                                        async for i in covFindQ:
                                            covFind.append(i)
                                        if len(covFind):
                                            covid19Declaration = covFind[0]['covid19Declaration']
                                        else:
                                            covid19Declaration = False
                                        proFindQ = self.profile.find(
                                            {
                                                '_id':res['profileId'],
                                                'entityId':self.entityId,
                                                'applicationId':applicationIdFind[0]['_id']
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
                                                regNum = accFind[0]['contact'][0]['value'] - 910000000000
                                            else:
                                                regNum = None
                                        else:
                                            regNum = None
                                        v = {
                                                'registeredPhoneNum':regNum,
                                                'accServiceType':res['accServiceType'],
                                                'serviceType':res['serviceType'],
                                                'disabled':res['disabled'],
                                                'verified':res['verified'],
                                                'status':res['status'],
                                                'serviceAccountId':str(res['_id']),
                                                'covid19Declaration':covid19Declaration,
                                                'hotelInfo':res['hotelInfo'],
                                                'propertyInfo':res['propertyInfo'],
                                                'id':str(res['profileId'])
                                            }
                                        result.append(v)
                                    code = 2000
                                    status = True
                                    message = "Data Found"
                                else:
                                    code = 4750
                                    status = False
                                    message = "Data not found"
                            else:
                                try:
                                    hotelId = ObjectId(hotelId)
                                except:
                                    code = 4560
                                    message = "Invalid Hotel Id"
                                    raise Exception
                                accListQ = self.serviceAccount.find(
                                        {
                                            'entityId': self.entityId,
                                            '_id':hotelId,
                                            #'verified':True
                                        },
                                    )
                                accList = []
                                async for r in accListQ:
                                    accList.append(r)
                                if len(accList):
                                    for res in accList:
                                        v = {
                                                    'hotelInfo':res['hotelInfo'],
                                                    #'facility':res['facility'],
                                                    #'tourOpInfo':res['tourOpInfo'],
                                                    'media':res['media'],
                                                    'location':res['location']
                                            }
                                        if len(res['media']):
                                            for docx in res['media'] :
                                                docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(res['entityId']) \
                                                        + '/service_media/' + str(res['profileId'])\
                                                        + '/' + str(docx['time']) + docx['mimeType']
                                        else:
                                            img = {
                                                    'link':"https://mtime.xlayer.in/uploads/Placeholder.png"
                                                }
                                            res['media'].append(img)
                                        result.append(v)
                                    code = 2000
                                    status = True
                                else:
                                    code = 4750
                                    status = False
                                    message = "Hotel not found"
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
            response['lenResult'] = len(result)
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
