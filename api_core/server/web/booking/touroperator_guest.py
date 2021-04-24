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
from bson.json_util import dumps as b_dumps

@xenSecureV1
class MtimeTourOperatorGuestHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ('GET','OPTIONS','POST','PUT')

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
    phoneCountry = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][9]['name']
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
    guestList = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][41]['name']
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
                    Log.i('API-ID', self.apiId)
                    if app[0]['apiId'] in [ 402020, 402021, 402022]: # TODO: till here
                        if self.apiId == 402021:
                            try:
                                serviceType = int(self.request.arguments['serviceType'][0])
                                if serviceType not in [1,3]:
                                    raise Exception
                            except:
                                code = 8493
                                status = False
                                message = "Invalid Argument - ['serviceType']"
                                raise Exception

                            guestListFindQ = self.guestList.find(
                                                        {
                                                            'profileId':self.profileId,
                                                            'disabled':False,
                                                            'serviceType':serviceType,
                                                        }
                                                    )
                            guestListFind = []
                            async for i in guestListFindQ:
                                guestListFind.append(i)
                            if len(guestListFind):
                                for res in guestListFind:
                                    v = {
                                            '_id':str(res['_id']),
                                            'touristContactDetails':res['touristContactDetails'],
                                            'activity':res['activity'],
                                            'time':res['time'],
                                            'touristProfileId':str(res['touristProfileId']),
                                            'touristAccountId':str(res['touristAccountId']),
                                            'modifiedTime':res['modifiedTime']
                                        }
                                    x = json.loads(b_dumps(v))
                                    result.append(x)
                            if len(result):
                                result.reverse()
                                code = 2000
                                status = True
                                message = "List of Guests"
                            else:
                                code = 4004
                                status = False
                                message = "No Data Found"
                        elif self.apiId == 402020:
                            try:
                                activityId = int(self.request.arguments['index'][0])
                            except:
                                code = 8926
                                status = False
                                message = "Invalid Argument - ['id']"
                                raise Exception
                            guestListFindQ = self.guestList.find(
                                                        {
                                                            'touristProfileId':self.profileId,
                                                            'touristAccountId':self.accountId,
                                                            'disabled':False,
                                                            #'serviceType':3,
                                                            'serviceType':{"$in":[1,3]},
                                                            '$where': 'this.activity[this.activity.length - 1].id =='+str(activityId)
                                                        }
                                                    )
                            guestListFind = []
                            async for i in guestListFindQ:
                                guestListFind.append(i)
                            if len(guestListFind):
                                for res in guestListFind:
                                    v = {
                                            '_id':str(res['_id']),
                                            'activity':res['activity'],
                                            'time':res['time'],
                                            'modifiedTime':res['modifiedTime'],
                                            'serviceAccountInfo':res['serviceAccountInfo']
                                        }
                                    result.append(v)
                            if len(result):
                                result.reverse()
                                code = 2000
                                status = True
                                message = "List of Guests"
                            else:
                                code = 4004
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

    async def post(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments1 = json.loads(self.request.body.decode())
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
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
                    if self.apiId in [ 402021, 402022]:
                        if self.apiId == 402021:
                            # TODO Have to re-confirm on field validations
                            try:
                                serviceType = int(self.request.arguments['serviceType'][0].decode())
                                if serviceType not in [1,3]:
                                    raise Exception
                            except:
                                code = 8493
                                status = False
                                message = "Invalid Argument - ['serviceType']"
                                raise Exception
                            serAccFindQ = self.serviceAccount.find(
                                            {
                                                'profileId':self.profileId,
                                                'entityId':self.entityId,
                                                'serviceType':serviceType,
                                                'disabled':False,
                                                'verified':True
                                            }
                                        )
                            serAccFind = []
                            async for i in serAccFindQ:
                                serAccFind.append(i)

                            if not len(serAccFind):
                                code = 2180
                                status = False
                                message = "Active Service Account Not Found"
                                raise Exception

                            if serviceType == 3:
                                serviceAccountInfo = serAccFind[0]['basicInfo']
                            elif serviceType == 1:
                                serviceAccountInfo = [
                                                        {
                                                            'organizationName':serAccFind[0]['propertyInfo'][0]['propertyName'],
                                                            'district':serAccFind[0]['hotelInfo'][0]['district'],
                                                            'mobileNumber':serAccFind[0]['hotelInfo'][0]['ownerNumber'],
                                                            'ownerName':serAccFind[0]['hotelInfo'][0]['ownerName'],
                                                            'address':serAccFind[0]['hotelInfo'][0]['hotelAddress'],
                                                            'emailAddress':serAccFind[0]['hotelInfo'][0]['ownerEmail']
                                                        }
                                                    ]
                            firstName = self.request.arguments1.get('firstName')
                            if firstName == None or firstName == "":
                                code = 2909
                                status = False
                                message = "First Name cannot be empty"
                                raise Exception
                            code,message = Validate.i(
                                            firstName,
                                            'First Name',
                                            maxLength = 50,
                                            #noSpecial = True,
                                            #noNumber = True
                                            )
                            if code != 4100:
                                raise Exception

                            firstName = firstName.title()

                            lastName = self.request.arguments1.get('lastName')
                            if lastName == None or lastName == "":
                                code = 2909
                                status = False
                                message = "Last Name cannot be empty"
                                raise Exception
                            code,message = Validate.i(
                                            lastName,
                                            'Last Name',
                                            maxLength = 50,
                                            #noSpecial = True,
                                            #noNumber = True
                                        )
                            if code != 4100:
                                raise Exception

                            lastName = lastName.title()

                            countryCode = self.request.arguments1.get('countryCode')
                            if countryCode == None:
                                code = 4251
                                message = 'Missing Argument - [ countryCode ].'
                                raise Exception
                            try:
                                countryCode = int(countryCode)
                            except:
                                code = 4552
                                message = 'Invalid Argument - [ countryCode ].'
                                raise Exception
                            countryQ = self.phoneCountry.find(
                                        {
                                            'dialCode': countryCode
                                        },
                                        limit=1
                                    )
                            country = []
                            async for i in countryQ:
                                country.append(i)
                            if not len(country):
                                code = 4242
                                message = 'Please enter a valid Country Code.'
                                raise Exception

                            # Phone number validation with regex and geo data
                            phoneNumber = self.request.arguments1.get('phoneNumber')
                            code,message = Validate.p(
                                            phoneNumber,
                                            country[0]['alpha2'],
                                            country[0]['sDialCode']
                                        )
                            if code != 4100:
                                Log.i('any issuesss -------------------------> ')
                                raise Exception

                            orgPhoneNumber = int(phoneNumber)
                            phoneNumber = int(str(countryCode) + str(phoneNumber))


                            email = self.request.arguments1.get('email')
                            if email != None:
                                code,message = Validate.i(
                                                    email,
                                                    'Email',
                                                    #inputType='email',
                                                    maxLength = 50,
                                                )
                                if code != 4100:
                                    raise Exception
                            else:
                                email = ''
                            appFindQ = self.applications.find(
                                {
                                    'apiId': 402020
                                }
                            )
                            appFind = []
                            async for i in appFindQ:
                                appFind.append(i)

                            if not len(app):
                                code = 1002
                                status = False
                                message = "Invalid Application. Please contact Support"
                                raise Exception
                            proFind = []
                            Log.i('Guest phone number', phoneNumber)
                            accFindQ = self.account.find(
                                        {
                                            'contact.0.value':phoneNumber,
                                        }
                                    )
                            accFind = []
                            async for i in accFindQ:
                                accFind.append(i)
                            if len(accFind):
                                Log.i('Account already axist.')
                                proFindQ = self.profile.find(
                                        {
                                            'accountId':accFind[0]['_id'],
                                            'entityId': self.entityId,
                                            'applicationId': appFind[0]['_id']
                                        },
                                        limit=1
                                    )
                                proFind = []
                                async for i in proFindQ:
                                    proFind.append(i)
                                if len(proFind):
                                    primaryTouristId = proFind[0]['_id']
                                    accountData =   [{
                                                    'firstName': accFind[0]['firstName'],
                                                    'lastName': accFind[0]['lastName'],
                                                    'contact':  accFind[0]['contact']
                                                }]

                            else:
                                if len(email):
                                    emailValQ = self.account.find(
                                                {
                                                    'contact.1.value': email
                                                }
                                            )
                                    emailVal = []
                                    async for i in emailValQ:
                                        emailVal.append(i)
                                    if len(emailVal):
                                        if phoneNumber != emailVal[0]['contact'][0]['value']:
                                            code = 4655
                                            status = False
                                            message = "Email address already used for different number " \
                                                    + str(emailVal[0]['contact'][0]['value'])
                                            raise Exception
                                accountData =   [{
                                                    'firstName': firstName.title(),
                                                    'lastName': lastName.title(),
                                                    'country': [
                                                        {
                                                            'code': country[0]['code'],
                                                            'name': country[0]['name'],
                                                            '_id': country[0]['_id']
                                                        }
                                                    ],
                                                    'contact':  [
                                                                    {
                                                                        'verified': False,
                                                                        'value': phoneNumber,
                                                                        "countryCode" : country[0]['code'],
                                                                        "dialCode" : country[0]['dialCode'],
                                                                        "phoneNumber" : orgPhoneNumber,
                                                                        "sDialCode" : country[0]['sDialCode']
                                                                    }
                                                                ]
                                                }]
                                if len(email):
                                    accountData[0]['contact'].append(
                                            {
                                                'verified': False,
                                                'value': email.lower()
                                            }
                                        )

                            try:
                                if not len(accFind):
                                    accountId = await self.account.insert_one(accountData[0])
                                    accountId = accountId.inserted_id
                                else:
                                    accountId = accFind[0]['_id']
                            except:
                                code = 5830
                                status = False
                                message = 'Internal Error Please Contact the Support Team.'
                                raise Exception
                            try:
                                if not len(proFind):
                                    profileId = await self.profile.insert_one(
                                        {
                                            'active': True,
                                            'locked': False,
                                            'closed': False,
                                            'entityId': self.entityId,
                                            'applicationId': appFind[0]['_id'],
                                            'accountId': accountId,
                                            'data':[]
                                        }
                                    )
                                    Log.i(profileId, 'New Profile Created!')
                                    profileId = str(profileId.inserted_id)
                                else:
                                    profileId = proFind[0]['_id']
                            except:
                                code = 4560
                                status = False
                                message = "Internal Error. Please contact the Support Team"
                                raise Exception
                            contactN = [
                                            {
                                                'verified':False,
                                                'value':phoneNumber,
                                                "countryCode" : country[0]['code'],
                                                "dialCode" : country[0]['dialCode'],
                                                "phoneNumber" : orgPhoneNumber,
                                                "sDialCode" : country[0]['sDialCode']
                                            }
                                        ]
                            if len(email):
                                contactN.append({'verified':False,'value':email})

                            try:
                                guestListInsert = await self.guestList.insert_one(
                                                            {
                                                                'touristProfileId':profileId,
                                                                'touristAccountId':accountId,
                                                                'touristContactDetails':[
                                                                                            {
                                                                                                'firstName':firstName,
                                                                                                'lastName':lastName,
                                                                                                'contact':contactN,
                                                                                                'country': [
                                                                                                        {
                                                                                                            'code': country[0]['code'],
                                                                                                            'name': country[0]['name'],
                                                                                                            '_id': country[0]['_id']
                                                                                                        }
                                                                                                ],
                                                                                            }
                                                                                        ],
                                                                'serviceAccountId':serAccFind[0]['_id'],
                                                                'serviceType':serviceType,
                                                                'serviceAccountInfo':serviceAccountInfo,
                                                                'profileId':self.profileId,
                                                                'accountId':self.accountId,
                                                                'entityId':self.entityId,
                                                                'disabled':False,
                                                                'activity':[
                                                                                {
                                                                                    'id':1,
                                                                                    'time':timeNow()
                                                                                }
                                                                            ],
                                                                'time':timeNow(),
                                                                'modifiedTime':timeNow()
                                                            }
                                                        )
                                message = "Guest has been added"
                            except:
                                message = 'Guest is already added.'
                            result.append(
                                    {
                                        'touristProfileId': str(profileId),
                                        'touristAccountId': str(accountId)
                                    }
                                )
                            code = 2000
                            status = True
                        elif self.apiId == 402020:
                            code = 2000
                            status = True
                            message = "Guest has been added"
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

    async def put(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments1 = json.loads(self.request.body.decode())
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
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
                    if self.apiId in [ 402021, 402022, 402020]:
                        if self.apiId == 402021:
                            try:
                                serviceType = int(self.request.arguments['serviceType'][0].decode())
                                if serviceType not in [1,3]:
                                    raise Exception
                            except:
                                code = 8493
                                status = False
                                message = "Invalid Argument - ['serviceType']"
                                raise Exception
                            try:
                                touristAccountId = ObjectId(self.request.arguments1.get('touristAccountId'))
                            except:
                                code = 8392
                                status = False
                                messsage = "Invalid Tourist Account ID"
                                raise Exception
                            try:
                                touristProfileId = ObjectId(self.request.arguments1.get('touristProfileId'))
                            except:
                                code = 8391
                                status = False
                                messsage = "Invalid Tourist Profile ID"
                                raise Exception
                            accFindQ = self.account.find(
                                                {
                                                    '_id':touristAccountId,
                                                }
                                            )
                            accFind = []
                            async for i in accFindQ:
                                accFind.append(i)
                            if not len(accFind):
                                code = 9999
                                status = False
                                message = "Account Not Found"
                                raise Exception
                            proFindQ = self.profile.find(
                                                {
                                                    '_id':touristProfileId
                                                }
                                            )
                            proFind = []
                            async for i in proFindQ:
                                proFind.append(i)

                            serAccFindQ = self.serviceAccount.find(
                                            {
                                                'profileId':self.profileId,
                                                'entityId':self.entityId,
                                                'serviceType':serviceType,
                                                'disabled':False,
                                                'verified':True
                                            }
                                        )
                            serAccFind = []
                            async for i in serAccFindQ:
                                serAccFind.append(i)

                            if not len(serAccFind):
                                code = 2180
                                status = False
                                message = "Active Tour Operator Service Account Not Found"
                                raise Exception
                            if serviceType == 3:
                                serviceAccountInfo = serAccFind[0]['basicInfo']
                            elif serviceType == 1:
                                serviceAccountInfo = [
                                                        {
                                                            'organizationName':serAccFind[0]['propertyInfo'][0]['propertyName'],
                                                            'district':serAccFind[0]['hotelInfo'][0]['district'],
                                                            'mobileNumber':serAccFind[0]['hotelInfo'][0]['ownerNumber'],
                                                            'ownerName':serAccFind[0]['hotelInfo'][0]['ownerName'],
                                                            'address':serAccFind[0]['hotelInfo'][0]['hotelAddress'],
                                                            'emailAddress':serAccFind[0]['hotelInfo'][0]['ownerEmail']
                                                        }
                                                    ]

                            for res in proFind:
                                if res.get('lastSignInRequest') == None or res.get('lastSignInRequest') == 0:
                                    try:
                                        guestListInsert = await self.guestList.insert_one(
                                                            {
                                                                'touristProfileId':touristProfileId,
                                                                'touristAccountId':touristAccountId,
                                                                'touristContactDetails':[
                                                                                            {
                                                                                                'firstName':accFind[0]['firstName'],
                                                                                                'lastName':accFind[0]['lastName'],
                                                                                                'contact':accFind[0]['contact']
                                                                                            }
                                                                                        ],
                                                                'serviceAccountId':serAccFind[0]['_id'],
                                                                'serviceType':serviceType,
                                                                'serviceAccountInfo':serviceAccountInfo,
                                                                'profileId':self.profileId,
                                                                'accountId':self.accountId,
                                                                'entityId':self.entityId,
                                                                'disabled':False,
                                                                'activity':[
                                                                                {
                                                                                    'id':1,
                                                                                    'time':timeNow()
                                                                                }
                                                                            ],
                                                                'time':timeNow(),
                                                                'modifiedTime':timeNow()
                                                            }
                                                        )
                                        guestMessage = "Entry is active."
                                    except Exception as e:
                                        Log.i(str(e))
                                        if "duplicate" in str(e):
                                            code = 5600
                                            status = False
                                            message = "Guest already exists"
                                            raise Exception
                                        else:
                                            code = 5600
                                            status = False
                                            message = "Internal Error in submitting guest. Please contact Support"
                                            raise Exception
                                else:
                                    try:
                                        guestListInsert = await self.guestList.insert_one(
                                                            {
                                                                'touristProfileId':touristProfileId,
                                                                'touristAccountId':touristAccountId,
                                                                'serviceType':serviceType,
                                                                'touristContactDetails':[
                                                                                            {
                                                                                                'firstName':accFind[0]['firstName'],
                                                                                                'lastName':accFind[0]['lastName'],
                                                                                                'contact':accFind[0]['contact']
                                                                                            }
                                                                                        ],
                                                                'serviceAccountId':serAccFind[0]['_id'],
                                                                'serviceAccountInfo':serviceAccountInfo,
                                                                'profileId':self.profileId,
                                                                'accountId':self.accountId,
                                                                'entityId':self.entityId,
                                                                'disabled':False,
                                                                'activity':[
                                                                                {
                                                                                    'id':0,
                                                                                    'time':timeNow()
                                                                                }
                                                                            ],
                                                                'time':timeNow(),
                                                                'modifiedTime':timeNow()
                                                            }
                                                        )
                                        guestMessage = "Please wait for tourist approval."
                                    except Exception as e:
                                        Log.i(str(e))
                                        if "duplicate" in str(e):
                                            code = 5600
                                            status = False
                                            message = "Guest already exists"
                                            raise Exception
                                        else:
                                            code = 5600
                                            status = False
                                            message = "Internal Error in submitting guest. Please contact Support"
                                            raise Exception
                            code = 2000
                            status = True
                            message = "Guest has been added. " + guestMessage
                            result.append(
                                    {
                                        'touristProfileId': str(touristProfileId),
                                        'touristAccountId': str(touristAccountId)
                                    }
                                )
                        elif self.apiId == 402020:
                            try:
                                guestId = ObjectId(self.request.arguments1.get('guestId'))
                            except:
                                code = 8302
                                status = False
                                message = "Invalid Guest Id"
                                raise Exception

                            action = self.request.arguments1.get('action')
                            if type(action) != bool:
                                code = 3892
                                status = False
                                message = "Invalid Approval Status"
                                raise Exception

                            guestFindQ = self.guestList.find(
                                                    {
                                                        '_id':guestId,
                                                        'touristProfileId':self.profileId,
                                                        'touristAccountId':self.accountId,
                                                        'disabled':False
                                                    }
                                                )
                            guestFind = []
                            async for i in guestFindQ:
                                guestFind.append(i)

                            if not len(guestFind):
                                code = 3289
                                status = False
                                message = "Guest Entry Not Found"
                                raise Exception

                            if action == True:
                                statusMessage = "Entry has been approved"
                            elif action == False:
                                statusMessage = "Entry has been rejected"

                            if action == True:
                                guestApprovalUpdate = await self.guestList.update_one(
                                                    {
                                                        '_id':guestId,
                                                        'touristProfileId':self.profileId,
                                                        'touristAccountId':self.accountId,
                                                        'disabled':False
                                                    },
                                                    {
                                                    '$set':{
                                                                'modifiedTime':timeNow()
                                                            },
                                                    '$push':{
                                                                'activity':{
                                                                                'id':1,
                                                                                'time':timeNow()
                                                                            }
                                                            }
                                                    }
                                                )
                                if guestApprovalUpdate.modified_count != None:
                                    code = 2000
                                    status = True
                                    message = statusMessage
                                else:
                                    code = 3882
                                    status = False
                                    message = "Failure in Approval"
                            if action == False:
                                guestApprovalDelete = await self.guestList.delete_one(
                                                    {
                                                        '_id':guestId,
                                                        'touristProfileId':self.profileId,
                                                        'touristAccountId':self.accountId,
                                                        'disabled':False
                                                    }
                                                )
                                code = 2000
                                status = True
                                message = statusMessage
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
