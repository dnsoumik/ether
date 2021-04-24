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
class MtimeWebAccountOverviewHandler(tornado.web.RequestHandler,
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
    serviceResource = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][46]['name']
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
            serviceType = int(self.request.arguments['serviceType'][0])
        except:
            code = 3455
            status = False
            message = "Argument missing - [serviceType]"
            raise Exception

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
                try:
                    self.serviceAccountId = FN_DECRYPT(self.request.headers.get('service-Account-Key'))
                    if not len(self.serviceAccountId):
                        raise Exception
                    self.serviceAccountId = ObjectId(self.serviceAccountId)
                except Exception as e:
                    self.serviceAccountId = None
                Log.i('service account Id:',self.serviceAccountId)
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
                    Log.i(self.apiId)
                    if app[0]['apiId'] in [ 402020, 402021, 402022, 402023]: # TODO: till here
                        if serviceType == None:
                            code = 4565
                            status = False
                            message = 'Invalid Service Type'
                            raise Exception
                        if self.apiId == 402021:
                            if self.serviceAccountId == None:
                                accOverviewQ = self.serviceAccount.find(
                                    {
                                        'profileId':self.profileId,
                                        'entityId':self.entityId,
                                        'serviceType':serviceType
                                    }
                                )
                                accOverview = []
                                async for i in accOverviewQ:
                                    accOverview.append(i)
                            else:
                                accOverviewQ = self.serviceAccount.find(
                                    {
                                        'profileId':self.serviceAccountId,
                                        'entityId':self.entityId,
                                        'serviceType':serviceType
                                    }
                                )
                                accOverview = []
                                async for i in accOverviewQ:
                                    accOverview.append(i)
                            if len(accOverview):
                                v = {}
                                if serviceType == 1:
                                    try:
                                        if len(accOverview[0]['propertyInfo']):
                                            v['propertyInfo'] = True
                                            v['serviceName'] = accOverview[0]['propertyInfo'][0]['propertyName']
                                        else:
                                            v['propertyInfo'] = False
                                            v['serviceName'] = ''
                                    except:
                                        v['propertyInfo'] = False
                                        v['serviceName'] = ''
                                if serviceType in [3,4]:
                                    try:
                                        if len(accOverview[0]['basicInfo']):
                                            v['basicInfo'] = True
                                        else:
                                            v['basicInfo'] = False
                                    except:
                                        v['basicInfo'] = False
                                    try:
                                        if len(accOverview[0]['empInfo']):
                                            v['empInfo'] = True
                                        else:
                                            v['empInfo'] = False
                                    except:
                                        v['empInfo'] = False
                                    try:
                                        if len(accOverview[0]['document']):
                                            v['document'] = True
                                        else:
                                            v['document'] = False
                                    except:
                                        v['document'] = False
                                    try:
                                        if len(accOverview[0]['declaration']):
                                            v['declaration'] = True
                                        else:
                                            v['declaration'] = False
                                    except:
                                        v['declaration'] = False
                                if serviceType in [2,4,5]:
                                    try:
                                        if len(accOverview[0]['contactInfo']):
                                            v['contactInfo'] = True
                                        else:
                                            v['contactInfo'] = False
                                    except:
                                        v['declaration'] = False
                                try:
                                    if len(accOverview[0]['serviceInfo']):
                                        v['serviceInfo'] = True
                                    else:
                                        v['serviceInfo'] = False
                                except:
                                    v['serviceInfo'] = False

                                if serviceType == 3:
                                    try:
                                        if len(accOverview[0]['tourTransInfo']):
                                            v['tourTransInfo'] = True
                                        else:
                                            v['tourTransInfo'] = False
                                    except:
                                        v['tourTransInfo'] = False
                                    try:
                                        if len(accOverview[0]['tourGuideInfo']):
                                            v['tourGuideInfo'] = True
                                        else:
                                            v['tourGuideInfo'] = False
                                    except:
                                        v['tourGuideInfo'] = False
                                if serviceType in [6,8]:
                                    try:
                                        if len(accOverview[0]['basicInfo']):
                                            v['basicInfo'] = True
                                            v['serviceName'] = accOverview[0]['basicInfo'][0]['touristSpotName']
                                        else:
                                            v['basicInfo'] = False
                                            v['serviceName'] = ''
                                    except:
                                        v['basicInfo'] = False
                                        v['serviceName'] = ''
                                    if serviceType == 6:
                                        try:
                                            if len(accOverview[0]['serviceInfo']):
                                                v['serviceInfo'] = True
                                            else:
                                                v['serviceInfo'] = False
                                        except:
                                            v['serviceInfo'] = False
                                    elif serviceType == 8:
                                        resourceFindQ = self.serviceResource.find(
                                                        {
                                                            'profileId':self.profileId,
                                                            'serviceType':8,
                                                            'disabled':False
                                                        }
                                                    )
                                        resourceFind = []
                                        async for i in resourceFindQ:
                                            resourceFind.append(i)
                                        if len(resourceFind):
                                            v['resource'] = True
                                        else:
                                            v['resource'] = False
                                if serviceType in [1,2,3,4,5,6,8]:
                                    try:
                                        if len(accOverview[0]['paymentInfo']):
                                            v['paymentInfo'] = True
                                        else:
                                            v['paymentInfo'] = False
                                    except:
                                        v['paymentInfo'] = False

                                v ['verified'] = accOverview[0]['verified']
                                result.append(v)
                                code = 2000
                                status = True
                                message = "Account Overview Information"
                            else:
                                '''
                                v = {
                                        'basicInfo':False,
                                        'contactInfo':False,
                                        'serviceInfo':False,
                                        'empInfo':False,
                                        'document':False,
                                        'declaration':False
                                    }
                                status = True
                                result.append(v)
                                '''
                                code = 4855
                                status = False
                                message = "No Account Found"
                        elif self.apiId in [402022,402023]:
                            try:
                                serviceId = str(self.request.arguments['id'][0].decode())
                                try:
                                    serviceId = ObjectId(serviceId)
                                except:
                                    raise Exception
                            except:
                                code = 4275
                                status = False
                                message = "Invalid Service Account Id"
                                raise Exception
                            accOverviewQ = self.serviceAccount.find(
                                    {
                                        '_id':serviceId,
                                        'entityId':self.entityId,
                                        'serviceType':serviceType
                                    }
                                )
                            accOverview = []
                            async for i in accOverviewQ:
                                accOverview.append(i)
                            if len(accOverview):
                                profileId = accOverview[0]['profileId']
                                v = {}
                                if serviceType in [3,4]:
                                    try:
                                        if len(accOverview[0]['basicInfo']):
                                            v['basicInfo'] = True
                                        else:
                                            v['basicInfo'] = False
                                    except:
                                        v['basicInfo'] = False
                                    try:
                                        if len(accOverview[0]['empInfo']):
                                            v['empInfo'] = True
                                        else:
                                            v['empInfo'] = False
                                    except:
                                        v['empInfo'] = False
                                    try:
                                        if len(accOverview[0]['document']):
                                            v['document'] = True
                                        else:
                                            v['document'] = False
                                    except:
                                        v['document'] = False
                                    try:
                                        if len(accOverview[0]['declaration']):
                                            v['declaration'] = True
                                        else:
                                            v['declaration'] = False
                                    except:
                                        v['declaration'] = False
                                if serviceType in [2,4,5]:
                                    try:
                                        if len(accOverview[0]['contactInfo']):
                                            v['contactInfo'] = True
                                        else:
                                            v['contactInfo'] = False
                                    except:
                                        v['declaration'] = False
                                try:
                                    if len(accOverview[0]['serviceInfo']):
                                        v['serviceInfo'] = True
                                    else:
                                        v['serviceInfo'] = False
                                except:
                                    v['serviceInfo'] = False

                                if serviceType == 3:
                                    try:
                                        if len(accOverview[0]['tourTransInfo']):
                                            v['tourTransInfo'] = True
                                        else:
                                            v['tourTransInfo'] = False
                                    except:
                                        v['tourTransInfo'] = False
                                    try:
                                        if len(accOverview[0]['tourGuideInfo']):
                                            v['tourGuideInfo'] = True
                                        else:
                                            v['tourGuideInfo'] = False
                                    except:
                                        v['tourGuideInfo'] = False
                                if serviceType in [6,8]:
                                    try:
                                        if len(accOverview[0]['basicInfo']):
                                            v['basicInfo'] = True
                                        else:
                                            v['basicInfo'] = False
                                    except:
                                        v['basicInfo'] = False
                                    if serviceType == 6:
                                        try:
                                            if len(accOverview[0]['serviceInfo']):
                                                v['serviceInfo'] = True
                                            else:
                                                v['serviceInfo'] = False
                                        except:
                                            v['serviceInfo'] = False
                                    elif serviceType == 8:
                                        resourceFindQ = self.serviceResource.find(
                                                        {
                                                            'profileId':profileId,
                                                            'serviceType':8,
                                                            'disabled':False
                                                        }
                                                    )
                                        resourceFind = []
                                        async for i in resourceFindQ:
                                            resourceFind.append(i)
                                        if len(resourceFind):
                                            v['resource'] = True
                                        else:
                                            v['resource'] = False
                                if serviceType in [1,2,3,4,5,6,8]:
                                    try:
                                        if len(accOverview[0]['paymentInfo']):
                                            v['paymentInfo'] = True
                                        else:
                                            v['paymentInfo'] = False
                                    except:
                                        v['paymentInfo'] = False
                                v ['verified'] = accOverview[0]['verified']
                                result.append(v)
                                code = 2000
                                status = True
                                message = "Account Overview Information"
                            else:
                                '''
                                v = {
                                        'basicInfo':False,
                                        'contactInfo':False,
                                        'serviceInfo':False,
                                        'empInfo':False,
                                        'document':False,
                                        'declaration':False
                                    }
                                status = True
                                result.append(v)
                                '''
                                code = 4855
                                status = False
                                message = "No Account Found"
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
