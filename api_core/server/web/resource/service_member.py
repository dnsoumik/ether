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
class ServiceMemberHandler(tornado.web.RequestHandler, MongoMixin):

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
                self.profileId = profile[0]['_id']
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
                    if app[0]['apiId'] == 402021: # TODO: till here
                        self.apiId = app[0]['apiId']
                        Log.i(self.apiId)
                        '''
                        try:
                            aClosed = bool(int(self.get_arguments('closed')[0]))
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ closed ].'
                            raise Exception
                        try:
                            profileId = ObjectId(self.get_arguments('id')[0])
                        except:
                            profileId = None
                        serviceAccFind = yield self.serviceAccount.find(
                                                {
                                                    'profileId':self.profileId,
                                                    'serviceType':1
                                                }
                                            )
                        if not len(serviceAccFind):
                            code = 4555
                            status = False
                            message = "No Data Found"
                            raise Exception
                        serviceAccountId = serviceAccFind[0]['_id']
                        '''

                        if profile[0].get('organization') == None or profile[0].get('organization') == []:
                            proUpdate = await self.profile.update_one(
                                            {
                                                '_id':self.profileId
                                            },
                                            {
                                            '$set':{
                                                        'organization':[
                                                                {
                                                                    'serviceAccountId':self.profileId,
                                                                    'role':0,
                                                                    'serviceType':1
                                                                }
                                                        ]
                                                    }
                                            }
                                        )
                        memFindQ = self.profile.find(
                                            {
                                                'organization.0.serviceAccountId':self.profileId
                                            }
                                        )
                        memFind = []
                        async for i in memFindQ:
                            memFind.append(i)
                        if not len(memFind):
                            code = 4555
                            status = False
                            message = "No Data Found"
                            raise Exception
                        roleList = ['Primary','Primary','Secondary']
                        for res in memFind:
                            accFindQ = self.account.find(
                                            {
                                                '_id':res['accountId']
                                            }
                                        )
                            accFind = []
                            async for i in accFindQ:
                                accFind.append(i)
                            if len(accFind):
                                role = res['organization'][0]['role']
                                v = {
                                        'profileId': str(res['_id']),
                                        'fullName': accFind[0]['firstName'] + ' ' + accFind[0]['lastName'],
                                        'firstName': accFind[0]['firstName'],
                                        'lastName': accFind[0]['lastName'],
                                        'contact': accFind[0]['contact'],
                                        'role': res['organization'][0]['role'],
                                        'roleName': roleList[role],
                                        'accountId': str(accFind[0]['_id'])
                                    }
                                result.append(v)
                                result.reverse()
                                code = 2000
                                status = True
                                message = "List of Members"
                            else:
                                code = 4863
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
                self.profileId = profile[0]['_id']
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
                    if app[0]['apiId'] == 402021: # TODO: till here

                        firstName = self.request.arguments.get('firstName')
                        code, message = Validate.i(
                                    firstName,
                                    'First Name',
                                    notEmpty=True,
                                    noSpecial=True,
                                    noNumber=True,
                                    maxLength=50,
                                    noSpace=True
                                )
                        if code != 4100:
                            raise Exception
                        lastName = self.request.arguments.get('lastName')
                        code, message = Validate.i(
                                    lastName,
                                    'Last Name',
                                    notEmpty=True,
                                    noSpecial=True,
                                    noNumber=True,
                                    maxLength=50,
                                    noSpace=True
                                )
                        if code != 4100:
                            raise Exception

                        phoneNumber = self.request.arguments.get('phoneNumber')
                        if phoneNumber == None:
                            code = 4251
                            message = 'Phone number cannot be empty'
                            raise Exception
                        elif type(phoneNumber) != int or len(str(phoneNumber)) != 10:
                            code = 4552
                            message = 'Invalid phone number'
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
                        if email == None:
                            email = ''
                        if len(email):
                            code, message = Validate.i(
                                    email,
                                    'Email',
                                    inputType='email',
                                    maxLength=80,
                                    noSpace=True
                                )
                            if code != 4100:
                                raise Exception

                        #role = 2
                        #'''
                        try:
                            role = int(self.request.arguments.get('role'))
                        except:
                            role = 2

                        if role == None:
                            code = 4251
                            message = 'Please select the role'
                            raise Exception
                        elif role not in [1,2]:
                            code = 4552
                            message = 'Invalid role for member.'
                            raise Exception
                        code, message = Validate.i(
                                    role,
                                    'Role',
                                    dataType=int,
                                )
                        if code != 4100:
                            raise Exception
                        #'''

                        profileApplicationQ = self.applications.find(
                            {
                                'apiId': 402021,
                                'entityId': self.entityId
                            },
                            limit=1
                        )
                        profileApplication = []
                        async for i in profileApplicationQ:
                            profileApplication.append(i)
                        if not len(profileApplication):
                            code = 4655
                            status = False
                            message = "Invalid Application. Please contact Support"
                            raise Exception
                        profileApplicationId = profileApplication[0]['_id']
                        '''
                        serviceAccountFind = yield self.serviceAccount.find(
                                                {
                                                    'profileId':self.profileId,
                                                    'serviceType':1
                                                }
                                            )
                        if not len(serviceAccountFind):
                            code = 2550
                            status = False
                            message = "Accomodation Service Account is not registered."
                            raise Exception
                        serviceAccountId = serviceAccountFind[0]['_id']
                        '''

                        if email:
                            accEmailFindQ = self.account.find(
                                        {
                                            'contact.1.value':email,
                                        }
                                    )
                            accEmailFind = []
                            async for i in accEmailFindQ:
                                accEmailFind.append(i)
                            if len(accEmailFind):
                                if phoneNumber != accEmailFind[0]['contact'][0]['value']:
                                    code = 4955
                                    status = False
                                    message = "Member already registered but the email address does not match\
                                            with the phone number"
                                    raise Exception
                        accPhoneFindQ = self.account.find(
                                        {
                                            'contact.0.value':phoneNumber
                                        }
                                    )
                        accPhoneFind = []
                        async for i in accPhoneFindQ:
                            accPhoneFind.append(i)
                        if len(accPhoneFind):
                            proFindQ = self.profile.find(
                                        {
                                            'accountId':accPhoneFind[0]['_id'],
                                            'applicationId':profileApplication[0]['_id']
                                        }
                                    )
                            proFind = []
                            async for i in proFindQ:
                                proFind.append(i)
                            if len(proFind):
                                if str(self.profileId) == str(proFind[0]['_id']):
                                    code = 4355
                                    status = False
                                    message = "You cannot enter your own number for member"
                                    raise Exception
                                if proFind[0].get('organization') != None:
                                    if proFind[0].get('organization') != []:
                                        code = 2500
                                        status = False
                                        message = "Phone Number already registered as employee to an organization"
                                        raise Exception
                                proUpdate = await self.profile.update_one(
                                                {
                                                    '_id':proFind[0]['_id']
                                                },
                                                {
                                                '$set':{
                                                            'organization':[
                                                                {
                                                                    'serviceAccountId':self.profileId,
                                                                    'role':role,
                                                                    #'serviceType':1
                                                                }
                                                            ]
                                                        }
                                                }
                                            )
                                if proUpdate.modified_count != None:
                                    code = 2555
                                    status = True
                                    message = "Phone number is already registered. Role is assigned"
                                else:
                                    code = 2560
                                    status = False
                                    message = "Invalid setup"
                            else:
                                try:
                                    profileId = await self.profile.insert_one(
                                        {
                                            'active': False,
                                            'locked': False,
                                            'closed': False,
                                            'accountId': accPhoneFind[0]['_id'],
                                            'applicationId': profileApplicationId,
                                            'entityId': self.entityId,
                                            'organization':[
                                                        {
                                                            'serviceAccountId':self.profileId,
                                                            'role': role,
                                                            #'serviceType':1
                                                        }
                                                    ],
                                            'data': []
                                        }
                                    )
                                    code = 4850
                                    status = True
                                    message = "Member has been created"
                                except:
                                    code = 4855
                                    status = False
                                    message = "Internal Error. Please contact the Support"
                                    raise Exception
                        else:
                            accountData =   {
                                            'firstName': firstName,
                                            'lastName': lastName,
                                            'contact':  [
                                                            {
                                                                'verified': False,
                                                                'value': phoneNumber
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

                            accountId = await self.account.insert_one(accountData)
                            accountId = accountId.inserted_id
                            profileId = await self.profile.insert_one(
                                    {
                                        'active': False,
                                        'locked': False,
                                        'closed': False,
                                        'accountId': accountId,
                                        'applicationId': profileApplicationId,
                                        'entityId': self.entityId,
                                        'organization':[
                                                        {
                                                            'serviceAccountId':self.profileId,
                                                            'role': role,
                                                            #'serviceType':1
                                                        }
                                                    ],
                                        'data': []
                                    }
                                )
                            code = 2000
                            message = 'Member has been created.'
                            status = True
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


    async def delete(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
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
                    if app[0]['apiId'] == 402021: # TODO: till here
                        try:
                            profileId = str(self.request.arguments['id'][0].decode())
                            try:
                                profileId = ObjectId(profileId)
                            except:
                                raise Exception
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ id ].'
                            raise Exception
                        '''
                        proFindQ = self.profile.find(
                                        {
                                            '_id':profileId,
                                            'entityId': self.entityId
                                        }
                                    )
                        proFind = []
                        async for i in proFindQ:
                            proFind.append(i)
                        if proFind[0]['organization'][0]['role'] in [0,1]:
                                code = 9322
                                status = False
                                message = "Primary User cannot be deleted"
                                raise Exception
                        '''
                        updateResult = await self.profile.update_one(
                                        {
                                            '_id': profileId,
                                            'entityId': self.entityId,
                                            'closed': False
                                        },
                                        {
                                        '$pop': {
                                                    'organization': -1,
                                                }
                                        }
                                )
                        if updateResult.modified_count != None:
                            status = True
                            code = 2000
                            message = 'Member has been removed'
                        else:
                            code = 4210
                            message = 'Member does not exist'
                    else:
                        code = 4003
                        message = 'You are not Authorized.'
                        self.set_status(401)
                else:
                    code = 4003
                    message = 'You are not Authorized.'
                    self.set_status(401)
            else:
                code = 4003
                message = 'You are not Authorized.'
                self.set_status(401)
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

