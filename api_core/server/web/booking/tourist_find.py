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
class MtimeTouristFindHandler(tornado.web.RequestHandler,
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
                    if app[0]['apiId'] in [ 402020, 402021, 402022]: # TODO: till here
                        if self.apiId == 402021:
                            try:
                                phoneNumber = int(self.request.arguments['phoneNumber'][0])
                            except:
                                code = 3920
                                status = False
                                message = "Invalid Phone Number"
                                raise Exception

                            accFindQ = self.account.find(
                                            {
                                                "contact.0.value":phoneNumber
                                            }
                                        )
                            accFind = []
                            async for i in accFindQ:
                                accFind.append(i)
                            if not len(accFind):
                                code = 3222
                                status = False
                                message = "Account Not Found"
                                raise Exception
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

                            proFindQ = self.profile.find(
                                        {
                                            'accountId':accFind[0]['_id'],
                                            'applicationId':appFind[0]['_id']
                                        }
                                    )
                            proFind = []
                            async for i in proFindQ:
                                proFind.append(i)
                            if not len(proFind):
                                code = 8302
                                status = False
                                message = "Account Not Found"
                                raise Exception

                            guestListFindQ = self.guestList.find(
                                                {
                                                    'profileId':self.profileId,
                                                    'touristProfileId':proFind[0]['_id'],
                                                    'serviceType':3,
                                                    'entityId':self.entityId
                                                }
                                            )
                            guestListFind = []
                            async for i in guestListFindQ:
                                guestListFind.append(i)

                            if not len(guestListFind):
                                approvedStatus = False
                            else:
                                try:
                                    length = len(guestListFind[0]['activity'])
                                    if guestListFind[0]['activity'][length - 1]['id'] == 1:
                                        approvedStatus = True
                                    else:
                                        approvedStatus = False
                                except:
                                    approvedStatus = False
                            v = {
                                    'approved':approvedStatus,
                                    'accountId':str(accFind[0]['_id']),
                                    'profileId':str(proFind[0]['_id']),
                                    'firstName':accFind[0]['firstName'],
                                    'lastName':accFind[0]['lastName'],
                                    'contact':accFind[0]['contact']
                                }
                            result.append(v)
                            if len(result):
                                result.reverse()
                                code = 2000
                                status = True
                                message = "Data Found"
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
                            firstName = self.request.headers.get('firstName')
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
                            lastName = self.request.headers.get('lastName')
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

                            phoneNumber = self.request.headers.get('phoneNumber')
                            if phoneNumber == None or phoneNumber == "":
                                code = 2909
                                status = False
                                message = "Phone number cannot be empty"
                                raise Exception
                            try:
                                phoneNumber = int(phoneNumber)
                                if phoneNumber not in range(1000000000,9999999999):
                                    raise Exception
                            except:
                                code = 8392
                                status = False
                                message = "Invalid Phone Number"
                                raise Exception

                            countryCode = self.request.headers.get('countryCode')
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
                                            'code': countryCode
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
                            if len(str(phoneNumber)) != country[0]['telMaxLength']:
                                code = 4252
                                message = 'Please enter a valid Phone Number.'
                                raise Exception('phoneNumber')
                            else:
                                phoneNumber = int(str(countryCode) + str(phoneNumber))


                            email = self.request.headers.get('email')
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
                            accFindQ = self.account.find(
                                        {
                                            'contact.0.value':phoneNumber,
                                        }
                                    )
                            accFind = []
                            async for i in accFindQ:
                                accFind.append(i)
                            if len(accFind):
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
                                                    'firstName': firstName,
                                                    'lastName': lastName,
                                                    'contact':  [
                                                                    {
                                                                        'verified': False,
                                                                        'value': phoneNumber
                                                                    }
                                                                ]
                                                }]
                                if len(email):
                                    accountData[0]['contact'].append(
                                            {
                                                'verified': False,
                                                'value': email
                                            }
                                        )

                            try:
                                if not len(accFind):
                                    accountId = await self.account.insert_one(accountData[0])
                                    accountId = str(accountId.inserted_id)
                                    Log.i(accountId, 'New Account Created!')
                                else:
                                    accountId = str(accFind[0]['_id'])
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
                                            'accountId': ObjectId(accountId),
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
                            v = {
                                    'accountId':accountId,
                                    'profileId':profileId
                                }
                            result.append(v)
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
                self.request.arguments = json.loads(self.request.body.decode())
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
                            try:
                                touristAccountId = ObjectId(self.request.arguments.get('touristAccountId'))
                            except:
                                code = 8392
                                status = False
                                messsage = "Invalid Tourist Account ID"
                                raise Exception
                            try:
                                touristProfileId = ObjectId(self.request.arguments.get('touristProfileId'))
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
                                                'entityId':self.entitytId,
                                                'serviceType':3,
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

                            for res in proFind:
                                if res.get('lastSignInRequest') == None or res.get('lastSignInRequest') == 0:
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
                                                                'serviceType':3,
                                                                'serviceAccountName':serAccFind[0]['basicInfo'][0]['organizationName'],
                                                                'profileId':self.profileId,
                                                                'accountId':self.accountId,
                                                                'entityId':self.entityId,
                                                                'disabled':False,
                                                                'active':True,
                                                                'time':timeNow(),
                                                                'modifiedTime':timeNow()
                                                            }
                                                        )
                                    guestMessage = "Entry is active."
                                else:
                                    guestListInsert = await self.guestList.insert_one(
                                                            {
                                                                'touristProfileId':touristProfileId,
                                                                'touristAccountId':touristAccountId,
                                                                'serviceType':3,
                                                                'touristContactDetails':[
                                                                                            {
                                                                                                'firstName':accFind[0]['firstName'],
                                                                                                'lastName':accFind[0]['lastName'],
                                                                                                'contact':accFind[0]['contact']
                                                                                            }
                                                                                        ],
                                                                'serviceAccountId':serAccFind[0]['_id'],
                                                                'serviceAccountName':serAccFind[0]['basicInfo'][0]['organizationName'],
                                                                'profileId':self.profileId,
                                                                'accountId':self.accountId,
                                                                'entityId':self.entityId,
                                                                'disabled':False,
                                                                'active':False,
                                                                'time':timeNow(),
                                                                'modifiedTime':timeNow()
                                                            }
                                                        )
                                    guestMessage = "Please wait for tourist approval."
                            code = 2000
                            status = True
                            message = "Guest has been added. " + guestMessage
                        elif self.apiId == 402020:
                            try:
                                guestId = ObjectId(self.request.arguments.get('guestId'))
                            except:
                                code = 8302
                                status = False
                                message = "Invalid Guest Id"
                                raise Exception

                            statusValue = self.request.arguments.get('statusValue')
                            if type(statusValue) != bool:
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

                            if statusValue == True:
                                statusMessage = "Entry has been approved"
                            elif statusValue == False:
                                statusMessage = "Entry has been rejected"

                            guestApprovalUpdate = await self.guestList.update_one(
                                                    {
                                                        '_id':guestId,
                                                        'touristProfileId':self.profileId,
                                                        'touristAccountId':self.accountId,
                                                        'disabled':False
                                                    },
                                                    {
                                                    '$set':{
                                                                'active':statusValue,
                                                                'modifiedTime':timeNow()
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
