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
class PassInspectorHandler(tornado.web.RequestHandler, MongoMixin):

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
                    if app[0]['apiId'] in [402022,402023]: # TODO: till here
                        serviceProviderId = 402021
                        applIdQ = self.applications.find(
                                                            {
                                                                'apiId':serviceProviderId
                                                            }
                                                     )
                        applId = []
                        async for i in applIdQ:
                            applId.append(i)
                        if not len(applId):
                            code = 2929
                            status = False
                            message = "Application Not Found. Please contact support"
                            raise Exception
                        serviceAccountFindQ = self.serviceAccount.find(
                                                    {
                                                        'serviceType':7,
                                                        'disabled':False,
                                                        'entityId':self.entityId
                                                    }
                                                )
                        serviceAccountFind = []
                        async for i in serviceAccountFindQ:
                            serviceAccountFind.append(i)
                        if not len(serviceAccountFind):
                            code = 4004
                            status = False
                            message = "No Pass Inspectors Found"
                            raise Exception
                        for res in serviceAccountFind:
                            proFindQ = self.profile.find(
                                                {
                                                    '_id':res['profileId'],
                                                    'applicationId':applId[0]['_id'],
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
                                v = {
                                        'id':str(res['_id']),
                                        'fullName': accFind[0]['firstName'] + " " + accFind[0]['lastName'],
                                        'contact': accFind[0]['contact'],
                                        'location':res['location'],
                                        'profileId':str(res['profileId']),
                                        'verified':res['verified']
                                    }
                                result.append(v)
                        result.reverse()
                        code = 2000
                        status = True
                        message = "List of Pass Inspectors"
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
                    if app[0]['apiId'] == 402022: # TODO: till here

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

                        password = self.request.arguments.get('password')
                        if password == None or password == "":
                            code = 4739
                            status = False
                            message = "Please enter the password"
                            raise Exception
                        if len(str(password)) < 6 or len(str(password)) > 10:
                            code = 3838
                            status = False
                            message = "Password must be between 6 to 10 characters"
                            raise Exception

                        location = self.request.arguments.get('location')
                        if location == None or location == "":
                            code = 4739
                            status = False
                            message = "Please enter the location"
                            raise Exception
                        if len(str(location)) > 50:
                            code = 3838
                            status = False
                            message = "Location name cannot be more than 50 characters"
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


                        accPhoneFindQ = self.account.find(
                                        {
                                            'contact.0.value':phoneNumber
                                        }
                                    )
                        accPhoneFind = []
                        async for i in accPhoneFindQ:
                            accPhoneFind.append(i)
                        serviceProviderId = 402021
                        applIdQ = self.applications.find(
                                                            {
                                                                'apiId':serviceProviderId
                                                            }
                                                     )
                        applId = []
                        async for i in applIdQ:
                            applId.append(i)
                        if not len(applId):
                            code = 2929
                            status = False
                            message = "Application Not Found. Please contact support"
                            raise Exception
                        if len(accPhoneFind):
                            proFindQ = self.profile.find(
                                        {
                                            'accountId':accPhoneFind[0]['_id'],
                                            'applicationId':applId[0]['_id']
                                        }
                                    )
                            proFind = []
                            async for i in proFindQ:
                                proFind.append(i)
                            if len(proFind):
                                serAccFindQ = self.serviceAccount.find(
                                                {
                                                    'profileId':proFind[0]['_id'],
                                                    'serviceType':7
                                                }
                                            )
                                serAccFind = []
                                async for i in serAccFindQ:
                                    serAccFind.append(i)
                                if len(serAccFind):
                                    code = 4939
                                    status = False
                                    message = "Pass Inspector Account is already added for for this number"
                                    raise Exception
                                else:
                                    serviceAccountInsert = await self.serviceAccount.insert_one(
                                            {
                                                'serviceType':7,
                                                'entityId':self.entityId,
                                                'profileId':proFind[0]['_id'],
                                                'disabled': False,
                                                'verified': True,
                                                'location':location
                                            }
                                        )
                                    accPassUpdate = await self.account.update_one(
                                                        {
                                                            '_id':accPhoneFind[0]['_id']
                                                        },
                                                        {
                                                            '$set':{
                                                                        'privacy':[
                                                                                    {
                                                                                        'value':password
                                                                                    }
                                                                                ]
                                                                    }
                                                        }
                                                    )
                                    code = 2000
                                    status = True
                                    message = "Pass Inspector Account has been created"
                            else:
                                try:
                                    profileId = await self.profile.insert_one(
                                        {
                                            'active': False,
                                            'locked': False,
                                            'closed': False,
                                            'accountId': accPhoneFind[0]['_id'],
                                            'applicationId': applId[0]['_id'],
                                            'entityId': self.entityId,
                                            'insertTime':self.time,
                                            'organization':[],
                                            'data': []
                                        }
                                    )
                                except:
                                    code = 4855
                                    status = False
                                    message = "Internal Error. Please contact the Support"
                                    raise Exception
                                profId = profileId.inserted_id
                                serviceAccountInsert = await self.serviceAccount.insert_one(
                                            {
                                                'serviceType':7,
                                                'entityId':self.entityId,
                                                'profileId':profId,
                                                'disabled': False,
                                                'verified': True,
                                                'location':location
                                            }
                                    )
                                code = 2000
                                status = True
                                message = "Pass Inspector Account has been created"
                                accPassUpdate = await self.account.update_one(
                                                        {
                                                            '_id':accPhoneFind[0]['_id']
                                                        },
                                                        {
                                                            '$set':{
                                                                        'privacy':[
                                                                                    {
                                                                                        'value':password
                                                                                    }
                                                                                ]
                                                                    }
                                                        }
                                                )
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
                                        'applicationId': applId[0]['_id'],
                                        'entityId': self.entityId,
                                        'organization':[],
                                        'data': []
                                    }
                                )
                            profId = profileId.inserted_id
                            serviceAccountInsert = await self.serviceAccount.insert_one(
                                            {
                                                'serviceType':7,
                                                'entityId':self.entityId,
                                                'profileId':profId,
                                                'disabled': False,
                                                'verified': True,
                                                'location':location
                                            }
                                )
                            accPassUpdate = await self.account.update_one(
                                                        {
                                                            '_id':accountId
                                                        },
                                                        {
                                                            '$set':{
                                                                        'privacy':[
                                                                                    {
                                                                                        'value':password
                                                                                    }
                                                                                ]
                                                                    }
                                                        }
                                                )
                            code = 2000
                            message = 'Pass Inspector account has been created.'
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
                    if app[0]['apiId'] == 402022: # TODO: till here
                        try:
                            serviceAccountId = str(self.request.arguments.get('id'))
                            try:
                                serviceAccountId = ObjectId(serviceAccountId)
                            except:
                                raise Exception
                        except:
                            code = 8943
                            status = False
                            message = "Invalid ID"
                            raise Exception
                        location = self.request.arguments.get('location')
                        if location == None or location == "":
                            code = 8392
                            status = False
                            message = "Please enter the location"
                            raise Exception
                        if len(str(location)) > 50:
                            code = 2483
                            status = False
                            message = "Location name cannot be more than 50 characters"
                            raise Exception
                        serAccFindQ = self.serviceAccount.find(
                                        {
                                            '_id':serviceAccountId,
                                            'serviceType':7
                                        }
                                    )
                        serAccFind = []
                        async for i in serAccFindQ:
                            serAccFind.append(i)
                        if not len(serAccFind):
                            code = 9032
                            status = False
                            message = "Service Account Not Found"
                            raise Exception
                        serAccUpdate = await self.serviceAccount.update_one(
                                            {
                                                '_id':serviceAccountId,
                                                'serviceType':7
                                            },
                                            {
                                                '$set':{
                                                            'location':location
                                                        }
                                            }
                                        )
                        if serAccUpdate.modified_count != None:
                            code = 2000
                            status = True
                            message = "Location has been updated"
                        else:
                            code = 4004
                            status = False
                            message = "Location could not be updated"
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
                    if app[0]['apiId'] == 402022: # TODO: till here
                        try:
                            serviceAccountId = str(self.request.arguments['id'][0].decode())
                            try:
                                serviceAccountId = ObjectId(serviceAccountId)
                            except:
                                raise Exception
                        except:
                            code = 2838
                            status = False
                            message = "Invalid ID"
                            raise Exception

                        serAccFindQ = self.serviceAccount.find(
                                                                {
                                                                    '_id':serviceAccountId,
                                                                    'serviceType':7
                                                                }
                                                            )
                        serAccFind = []
                        async for i in serAccFindQ:
                            serAccFind.append(i)
                        if not len(serAccFind):
                            code = 4004
                            status = False
                            message = "Service Account Not Found"
                            raise Exception
                        disableStatus = serAccFind[0]['disabled']
                        if disableStatus == False:
                            statusMsg = "Service Account has been deleted"
                            statusUpdate = True
                        elif disableStatus == True:
                            statusMsg = "Service Account has been restored"
                            statusUpdate = False

                        serStatusUpdate = await self.serviceAccount.update_one(
                                                                {
                                                                    '_id':serviceAccountId,
                                                                    'serviceType':7
                                                                },
                                                                {
                                                                    '$set':{
                                                                                'disabled':statusUpdate
                                                                            }
                                                                }
                                                            )
                        if serStatusUpdate.modified_count != None:
                            code = 2000
                            status = True
                            message = statusMsg
                        else:
                            code = 4004
                            status = False
                            message = "Process Failure. Please contact Support"
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

