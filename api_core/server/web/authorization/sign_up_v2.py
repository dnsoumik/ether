#!/usr/bin/VtsAdminSignInHandler
# -*- coding: utf-8 -*-

'''
'''


from typing import Optional, Awaitable

from ..lib.lib import *
from ..lib.xen_protocol import noXenSecureV1

@noXenSecureV1
class SignUpV2Handler(tornado.web.RequestHandler, MongoMixin):

    SUPPORTED_METHODS = ('POST','OPTIONS')

    account = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][0]['name']
                ]

    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]

    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]

    oneTimePassword = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][3]['name']
                ]

    phoneCountry = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][6]['name']
                ]

    entity = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][5]['name']
                ]


    def options(self):
        self.set_status(200)
        self.write({})
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
                code = 4002
                message = 'Expected Request Type JSON.'
                raise Exception

            applicationId = self.request.arguments.get('applicationId')
            if applicationId == None:
                code = 4100
                message = 'Missing Argument - [ applicationId ].'
                raise Exception
            appQ = self.applications.find(
                    {
                        'applicationId': applicationId
                    },
                    limit=1
                )
            app = []
            async for i in appQ:
                app.append(i)
            if len(app) and app[0]['selfRegister']:
                entityQ = self.entity.find(
                                {
                                    '_id': self.entityId
                                },
                                limit=1
                            )
                entity = []
                async for i in entityQ:
                    entity.append(i)
                if not len(entity):
                    entityQ = self.entity.find(
                                {
                                    'origin': []
                                },
                                limit=1
                            )
                    entity = []
                    async for i in entityQ:
                        entity.append(i)
                    if not len(entity):
                        code = 5050
                        message = 'Internal Error Please Contact the Support Team.'
                        raise Exception
                method = self.request.arguments.get('method')
                if method == None:
                    code = 4130
                    message = 'Missing Argument - [ method ].'
                    raise Exception
                elif type(method) != int:
                    code = 4131
                    message = 'Invalid Argument - [ method ].'
                    raise Exception
                if method == 0:
                    try:
                        userId = str(self.request.arguments['userId'])
                        password = str(self.request.arguments['password'])
                        status = True
                    except Exception as e:
                        status = False
                        code = 4110
                        template = "Exception: {0}. Argument: {1!r}"
                        message = template.format(type(e).__name__, e.args)
                elif method == 1:
                    try:
                        regexSp = re.compile('[@_`+!#$%^&*()<>?/\-|}{~:,.]')
                        regexEm = re.compile('[@`+!#$%^&*()<>?/\|}{~:],')
                        regexNp = re.compile('[1234567890]')

                        firstName = self.request.arguments.get('firstName')
                        if firstName == None:
                            code = 4510
                            message = 'Missing Argument - [ firstName ].'
                            raise Exception
                        elif type(firstName) != str:
                            code = 4511
                            message = 'Invalid Argument - [ firstName ].'
                            raise Exception
                        elif not len(str(firstName)):
                            code = 4512
                            message = 'Please enter the First Name.'
                            raise Exception
                        elif regexSp.search(firstName) != None:
                            code = 4513
                            message = 'First name should not contain any special character.'
                            raise Exception
                        elif regexNp.search(firstName) != None:
                            code = 4514
                            message = 'First name should not contain any number.'
                            raise Exception
                        elif len(firstName) > 50:
                            code = 4515
                            message = 'First name should be less than 50 characters.'
                            raise Exception
                        elif ' ' in firstName:
                            code = 4516
                            message = 'First name should not contain any white space.'
                            raise Exception

                        firstName = firstName.title()

                        lastName = self.request.arguments.get('lastName')
                        if lastName == None:
                            code = 4520
                            message = 'Missing Argument - [ lastName ].'
                            raise Exception
                        elif type(lastName) != str:
                            code = 4521
                            message = 'Invalid Argument - [ lastName ].'
                            raise Exception
                        elif not len(str(lastName)):
                            code = 4522
                            message = 'Please enter the Last Name.'
                            raise Exception
                        elif regexSp.search(lastName) != None:
                            code = 4523
                            message = 'Last name should not contain any special character.'
                            raise Exception
                        elif regexNp.search(lastName) != None:
                            code = 4524
                            message = 'Last name should not contain any number.'
                            raise Exception
                        elif len(lastName) > 50:
                            code = 4525
                            message = 'Last name should be less than 50 characters.'
                            raise Exception
                        elif ' ' in lastName:
                            code = 4526
                            message = 'Last name should not contain any white space.'
                            raise Exception

                        lastName = lastName.title()

                        phoneNumber = self.request.arguments.get('phoneNumber')
                        if phoneNumber == None:
                            code = 4241
                            message = 'Missing Argument - [ phoneNumber ].'
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
                            orgPhoneNumber = int(phoneNumber)
                            phoneNumber = int(str(countryCode) + str(phoneNumber))

                        email = self.request.arguments.get('email')
                        if email != None and type(email) != str:
                            code = 4531
                            message = 'Invalid Argument - [ email ].'
                            raise Exception
                        elif email != None and len(email) == 0:
                            email = None
                        elif email != None and (len(email.split('@')) != 2 or '.' not in email \
                                or len(email) < 5):
                            code = 4532
                            message = 'Please enter a valid email.'
                            raise Exception
                        elif email != None and regexEm.search(lastName) != None:
                            code = 4533
                            message = 'Email name should not contain any special characters.'
                            raise Exception
                        elif email != None and len(email) > 60:
                            code = 4525
                            message = 'Email name should be less than 60 characters.'
                            raise Exception
                        elif email != None and ' ' in email:
                            code = 4526
                            message = 'Email should not contain any white space.'
                            raise Exception

                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        Log.d('FILE: ' + str(fname), 'LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                        if not len(message):
                            code = 4210
                            template = "Exception: {0}. Argument: {1!r}"
                            message = template.format(type(e).__name__, e.args)
                        raise Exception

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
                        code = 4560
                        message = 'Phone Number is already registerd.'
                        raise Exception

                    accountData =   {
                                        'firstName': firstName,
                                        'lastName': lastName,
                                        'insertTime': self.time,
                                        'time': timeNow(),
                                        'country': [
                                                {
                                                    'code': country[0]['isoAlpha3Code'],
                                                    'name': country[0]['name'],
                                                    '_id': country[0]['cId'],
                                                }
                                        ],
                                        'contact':  [
                                                        {
                                                            'verified': False,
                                                            'value': phoneNumber,
                                                            'dialCode': countryCode,
                                                            'sDialCode': country[0]['sCode'],
                                                            'phoneNumber': orgPhoneNumber,
                                                            'countryCode': country[0]['isoAlpha3Code']
                                                        }
                                                    ]
                                    }
                    if email != None:
                        email = email.lower()
                        accountData['contact'].append(
                                    {
                                        'verified': False,
                                        'value': email
                                    }
                                )
                    try:
                        accountId = await self.account.insert_one(accountData)
                    except Exception as e:
                        exe = str(e).split(':')
                        if len(exe) < 2:
                            status = False
                            code = 4280
                            message = 'Internal Error Please Contact the Support Team.'
                        elif 'contact.0.value_1' in exe[2]:
                            status = False
                            code = 4281
                            message = 'This Phone Number is already Registered.'
                        elif 'contact.1.value_1' in exe[2]:
                            status = False
                            code = 4282
                            message = 'This Email is already Registered.'
                        else:
                            status = False
                            code = 4283
                            message = 'Internal Error Please Contact the Support Team.'
                        raise Exception
                    try:
                        accountId = accountId.inserted_id
                        profileId = await self.profile.insert_one(
                                    {
                                        'active': False,
                                        'locked': False,
                                        'closed': False,
                                        'time': timeNow(),
                                        'insertTime': self.time,
                                        'accountId': accountId,
                                        'applicationId': app[0]['_id'],
                                        'entityId': entity[0]['_id'],
                                        'data': [],
                                    }
                                )
                    except:
                        code = 5830
                        message = 'Internal Error Please Contact the Support Team.'
                        raise Exception
                    nOtp = random.randint(100000, 999999)
                    profileId = profileId.inserted_id
                    await self.oneTimePassword.insert_one(
                                {
                                    'createdAt': dtime.now(),
                                    'profileId': profileId,
                                    'insertTime': self.time,
                                    'phoneNumber':  phoneNumber,
                                    'value': nOtp
                                }
                            )
                    Log.i('Phone Number: ', str(phoneNumber) + ' OTP: ' + str(nOtp))
                    gwResp = MSG91_GW.send(str(phoneNumber), str(entity[0]['smsGwId']), nOtp)
                    Log.i(gwResp)
                    code = 2000
                    message = 'A 6-digit One Time Password has been sent to your Phone Number.'
                    status = True
                else:
                    code = 4110
                    message = 'Sign In method not supported.'
                    raise Exception
            else:
                message = 'Application ID not found.'
                code = 4200
                raise Exception
        except Exception as e:
            status = False
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                Log.w('EXC', iMessage)
                Log.d('FILE: ' + str(fname), 'LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
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


