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


from ..lib.lib import *

@xenSecureV1
class AdminHandler(tornado.web.RequestHandler, MongoMixin):

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

    phoneCountry = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][6]['name']
                ]

    serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][0]['name']
                ]

    vehicleCategory = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][1]['name']
                ]

    vehicleSubCategory = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][2]['name']
                ]


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
                                'accountId': self.accountId,
                                'applicationId': self.applicationId,
                                'entityId': self.entityId
                            },
                            limit=1
                        )
            profile = []
            async for i in profileQ:
                profile.append(i)
            if len(profile):
                appQ = self.applications.find(
                            {
                                '_id': self.applicationId
                            },
                            limit=1
                        )
                app = []
                async for i in appQ:
                    app.append(i)
                if len(app):
                    if app[0]['apiId'] == 402022: # TODO: till here
                        self.apiId = app[0]['apiId']
                        Log.i(self.apiId)
                        profileApplicationQ = self.applications.find(
                            {
                                #'apiId': 402022,
                                'apiId': {"$in":[402022,402023]},
                                'entityId': self.entityId
                            },
                            #limit=1
                        )
                        profileApplication = []
                        async for i in profileApplicationQ:
                            profileApplication.append(i)
                        if not len(profileApplication):
                            raise Exception
                        else:
                            profileApplicationId = []
                            for k in profileApplication:
                                profileApplicationId.append(k['_id'])

                        try:
                            aClosed = bool(int(self.get_arguments('closed')[0]))
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ closed ].'
                            raise Exception

                        try:
                            profileId = ObjectId(self.get_arguments('id')[0].decode())
                        except:
                            profileId = None
                        if profileId != None:
                            aProfileQ = self.profile.find(
                                {
                                    '_id': profileId,
                                    'closed': aClosed,
                                    'entityId': self.entityId,
                                    #'applicationId': profileApplicationId
                                    'applicationId': {"$in":profileApplicationId},
                                },
                                limit=1
                            )
                            aProfile = []
                            async for i in aProfileQ:
                                aProfile.append(i)
                            if len(aProfile):
                                pAccountQ = self.account.find(
                                            {
                                                '_id': aProfile[0]['accountId']
                                            },
                                            limit=1
                                        )
                                pAccount = []
                                async for i in pAccountQ:
                                    pAccount.append(i)
                                if len(pAccount):
                                    v = {}
                                    v['closed'] = aProfile[0]['closed']
                                    v['locked'] = aProfile[0]['locked']
                                    v['active'] = aProfile[0]['active']
                                    v['id'] = str(aProfile[0].get('_id'))
                                    v['firstName'] = pAccount[0].get('firstName')
                                    v['lastName'] = pAccount[0].get('lastName')
                                    v['contact'] = pAccount[0].get('contact')
                                    pServiceAccountQ = self.serviceAccount.find(
                                                {
                                                    'profileId': aProfile[0]['_id'],
                                                    'entityId': self.entityId
                                                },
                                                limit=1
                                            )
                                    pServiceAccount = []
                                    async for i in pServiceAccountQ:
                                        pServiceAccount.append(i)
                                    if len(pServiceAccount):
                                        v['firstName'] = pServiceAccount[0].get('firstName')
                                        v['lastName'] = pServiceAccount[0].get('lastName')
                                    result.append(v)
                                else:
                                    code = 3002
                                    message = 'No Admin Account Found.'
                            else:
                                code = 3001
                                message = 'No Admin Account Found.'
                        else:
                            try:
                                limit = int(self.get_arguments('limit')[0])
                            except:
                                limit = None

                            try:
                                skip = int(self.get_arguments('skip')[0])
                            except:
                                skip = 0
                            if limit != None:
                                aProfilesQ = self.profile.find(
                                    {
                                        'closed': aClosed,
                                        'entityId': self.entityId,
                                        #'applicationId': profileApplicationId
                                        'applicationId': {"$in":profileApplicationId},
                                    },
                                    limit=limit,
                                    skip=skip
                                )
                                aProfiles =[]
                                async for i in aProfilesQ:
                                    aProfiles.append(i)
                                if len(aProfiles):
                                    for p in aProfiles:
                                        pAccountQ = self.account.find(
                                                {
                                                    '_id': p['accountId']
                                                },
                                                limit=1
                                            )
                                        pAccount = []
                                        async for i in pAccountQ:
                                            pAccount.append(i)
                                        if len(pAccount):
                                            v = {}
                                            v['closed'] = p['closed']
                                            v['locked'] = p['locked']
                                            v['active'] = p['active']
                                            v['role'] = p['role']
                                            v['id'] = str(p.get('_id'))
                                            v['firstName'] = pAccount[0].get('firstName')
                                            v['lastName'] = pAccount[0].get('lastName')
                                            v['contact'] = pAccount[0].get('contact')
                                            pServiceAccountQ = self.serviceAccount.find(
                                                    {
                                                        'profileId': p['_id'],
                                                        'entityId': self.entityId
                                                    },
                                                    limit=1
                                                )
                                            pServiceAccount = []
                                            async for i in pServiceAccountQ:
                                                pServiceAccount.append(i)
                                            if len(pServiceAccount):
                                                v['firstName'] = pServiceAccount[0].get('firstName')
                                                v['lastName'] = pServiceAccount[0].get('lastName')
                                            result.append(v)
                                    if len(result):
                                        status = True
                                        code = 2000
                                        result.reverse()
                                    else:
                                        code = 3030
                                        message = 'No Admin Account Found.'
                                else:
                                    code = 3030
                                    message = 'No Admin Account Found.'
                            else:
                                aProfilesQ = self.profile.find(
                                    {
                                        'closed': aClosed,
                                        'entityId': self.entityId,
                                        #'applicationId': profileApplicationId
                                        'applicationId': {"$in":profileApplicationId},
                                    }
                                )
                                aProfiles = []
                                async for i in aProfilesQ:
                                    aProfiles.append(i)
                                if len(aProfiles):
                                    for p in aProfiles:
                                        '''
                                        districts = ['East Khasi Hills','East Jaintia Hills','South West Garo Hills','West Garo Hills'\
                                                ,'North Garo Hills','East Garo Hills','South Garo Hills','West Khasi Hills'\
                                                ,'South West Khasi Hills','Ri Bhoi','West Jaintia Hills', '']
                                        pUpdate = await self.profile.update_many(
                                                        {
                                                            '_id':p['_id']
                                                        },
                                                        {
                                                        '$set':{
                                                            'districts':districts
                                                             }
                                                        }
                                                    )
                                        '''
                                        pAccountQ = self.account.find(
                                                {
                                                    '_id': p['accountId']
                                                },
                                                limit=1
                                            )
                                        pAccount = []
                                        async for i in pAccountQ:
                                            pAccount.append(i)
                                        if len(pAccount):
                                            v = {}
                                            v['closed'] = p['closed']
                                            v['locked'] = p['locked']
                                            v['active'] = p['active']
                                            v['role'] = p['role']
                                            v['districts'] = p['districts']
                                            v['id'] = str(p.get('_id'))
                                            v['firstName'] = pAccount[0].get('firstName')
                                            v['lastName'] = pAccount[0].get('lastName')
                                            v['contact'] = pAccount[0].get('contact')
                                            pServiceAccountQ = self.serviceAccount.find(
                                                    {
                                                        'profileId': p['_id'],
                                                        'entityId': self.entityId
                                                    },
                                                    limit=1
                                                )
                                            pServiceAccount = []
                                            async for i in pServiceAccountQ:
                                                pServiceAccount.append(i)
                                            if len(pServiceAccount):
                                                v['firstName'] = pServiceAccount[0].get('firstName')
                                                v['lastName'] = pServiceAccount[0].get('lastName')
                                            result.append(v)
                                    if len(result):
                                        status = True
                                        code = 2000
                                        result.reverse()
                                    else:
                                        code = 3030
                                        message = 'No Admin Account Found.'
                                else:
                                    code = 3030
                                    message = 'No Admin Account Found.'
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
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error, Please Contact the Support Team.'
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
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error, Please Contact the Support Team.'
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
                self.request.arguments = json.loads(self.request.body.decode())
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
            # TODO: this need to be moved in a global class, from here
            profileQ = self.profile.find(
                            {
                                'accountId': self.accountId,
                                'applicationId': self.applicationId,
                                'entityId': self.entityId
                            },
                            limit=1
                        )
            profile = []
            async for i in profileQ:
                profile.append(i)
            if len(profile):
                appQ = self.applications.find(
                            {
                                '_id': profile[0]['applicationId']
                            },
                            limit=1
                        )
                app = []
                async for i in appQ:
                    app.append(i)
                if len(app):
                    if app[0]['apiId'] == 402022: # TODO: till here
                        firstName = self.request.arguments.get('firstName')
                        if firstName == None or firstName == "":
                            code = 3289
                            status = False
                            message = "Please enter the first Name"
                            raise Exception
                        code, message = Validate.i(
                                    firstName,
                                    'First Name',
                                    noSpecial=True,
                                    noNumber=True,
                                    maxLength=50,
                                    noSpace=True
                                )
                        if code != 4100:
                            raise Exception
                        lastName = self.request.arguments.get('lastName')
                        if lastName == None or lastName == "":
                            code = 3289
                            status = False
                            message = "Please enter the last Name"
                            raise Exception
                        code, message = Validate.i(
                                    lastName,
                                    'Last Name',
                                    noSpecial=True,
                                    noNumber=True,
                                    maxLength=50,
                                    noSpace=True
                                )
                        if code != 4100:
                            raise Exception

                        phoneNumber = self.request.arguments.get('phoneNumber')
                        code, message = Validate.i(
                                    phoneNumber,
                                    'Phone Number',
                                    dataType=int,
                                )
                        if code != 4100:
                            raise Exception

                        countryCode = self.request.arguments.get('countryCode')
                        if countryCode == None:
                            code = 4251
                            message = 'Missing Argument - [ countryCode ].'
                            raise Exception
                        elif type(countryCode) != int:
                            code = 4552
                            message = 'Invalid Argument - [ countryCode ].'
                            raise Exception
                        else:
                            countryCode = int(countryCode)
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

                        email = self.request.arguments.get('email')
                        if email != None and email != "":
                            code, message = Validate.i(
                                    email,
                                    'Email',
                                    inputType='email',
                                    maxLength=80,
                                    noSpace=True
                                )
                            if code != 4100:
                                raise Exception

                        try:
                            role = int(self.request.arguments.get('role'))
                            if role not in [0,1,2,3]:
                                raise Exception
                        except:
                            code = 4389
                            status = False
                            message = "Please specify the proper role"
                            raise Exception

                        password = ""
                        districts = []
                        if role in [0,1,2]:
                            if role == 0:
                                apiId = 402022
                            if role in [1,2]:
                                apiId = 402023
                            password = self.request.arguments.get('password')
                            if password == None or password == "":
                                code = 8932
                                status = False
                                message = "Please enter the password"
                                raise Exception
                            code, message = Validate.i(
                                    password,
                                    'Password',
                                    maxLength=50,
                                )
                            if code != 4100:
                                raise Exception


                            districts = self.request.arguments.get('districts')
                            if districts == None:
                                code = 8932
                                status = False
                                message = "Please select the districts assigned for the role"
                                raise Exception
                            if type(districts) != list:
                                code = 8492
                                status = False
                                message = "Invalid Argument - ['districts']"
                                raise Exception
                            districtList = ['East Khasi Hills','East Jaintia Hills','South West Garo Hills','West Garo Hills'\
                                    ,'North Garo Hills','East Garo Hills','South Garo Hills','West Khasi Hills'\
                                    ,'South West Khasi Hills','Ri Bhoi','West Jaintia Hills', '']
                            for i in districts:
                                if i == "All":
                                    districts = districtList
                                elif i not in districtList:
                                    code = 3289
                                    status = False
                                    message = "Invalid district selected"
                                    raise Exception


                        profileApplicationQ = self.applications.find(
                            {
                                'apiId': apiId,
                                'entityId': self.entityId
                            },
                            limit=1
                        )
                        profileApplication = []
                        async for i in profileApplicationQ:
                            profileApplication.append(i)
                        if not len(profileApplication):
                            raise Exception
                        else:
                            profileApplicationId = profileApplication[0]['_id']
                            accountData =   {
                                                'firstName': firstName,
                                                'lastName': lastName,
                                                'contact':  [
                                                        {
                                                            'verified': False,
                                                            'value': phoneNumber
                                                        }
                                                    ],
                                                'privacy': [
                                                        {
                                                            'value':password
                                                        }
                                                    ]
                                            }
                            if email:
                                accountData['contact'].append(
                                    {
                                        'verified': False,
                                        'value': email
                                    }
                                )
                            try:
                                acState = 0
                                try:
                                    accountId = await self.account.insert_one(accountData)
                                    accountId = accountId.inserted_id
                                except:
                                    pAccountQ = self.account.find(
                                            {
                                                'contact.0.value': phoneNumber
                                            },
                                            limit=1
                                        )
                                    pAccount = []
                                    async for i in pAccountQ:
                                        pAccount.append(i)
                                    if len(pAccount):
                                        acState = 1
                                        accountId = pAccount[0]['_id']
                                    if email:
                                        pAccountQ = self.account.find(
                                            {
                                                'contact.1.value': email
                                            },
                                            limit=1
                                        )
                                        pAccount = []
                                        async for i in pAccountQ:
                                            pAccount.append(i)
                                        if len(pAccount):
                                            acState = 2
                                            accountId = pAccount[0]['_id']
                                profileId = await self.profile.insert_one(
                                    {
                                        'active': False,
                                        'locked': False,
                                        'closed': False,
                                        'accountId': accountId,
                                        'applicationId': profileApplicationId,
                                        'entityId': self.entityId,
                                        'role':role,
                                        'districts':districts,
                                        'data': []
                                    }
                                )
                                '''
                                passUpdate = await self.account.update_one(
                                            {
                                                'accountId':accountId,
                                                'contact.0.value': phoneNumber
                                            },
                                            {
                                                '$set':{
                                                            'privacy': [
                                                                        {
                                                                            'value':password
                                                                        }
                                                                    ]
                                                        }
                                            }
                                        )
                                '''
                                profileId = profileId.inserted_id
                                code = 2000
                                message = 'Account has been created.'
                                status = True
                            except:
                                code = 5833
                                message = 'Internal Error, Please Contact the Support Team.'
                                if acState == 1:
                                    code = 4281
                                    message = 'Phone Number is already Registered.'
                                elif acState == 2:
                                    code = 4282
                                    message = 'Email is already Registered.'
                                raise Exception
                            passUpdate = await self.account.update_one(
                                            {
                                                'contact.0.value': phoneNumber
                                            },
                                            {
                                                '$set':{
                                                            'privacy': [
                                                                        {
                                                                            'value':password
                                                                        }
                                                                    ]
                                                        }
                                            }
                                        )
                    else:
                        self.set_status(401)
                        code = 4003
                        message = 'You are not Authorized.'
                else:
                    self.set_status(401)
                    code = 4003
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
                message = 'Internal Error, Please Contact the Support Team.'
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
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error, Please Contact the Support Team.'
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
