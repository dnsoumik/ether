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
from datetime import timezone
from datetime import date
import datetime

@xenSecureV1
class MtimeAccountHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ('POST', 'PUT', 'GET', 'OPTIONS','DELETE')

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



    fu = FileUtil()

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
            '''
            try:
                # GET JSON FROM REQUEST BODY
                self.request.arguments = json.loads(self.request.body.decode())

            except Exception as e:
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                code = 4100
                message = 'Expected Request Type FormData.'
                raise Exception
            '''

            try:
                image = self.request.files['image'][0]
            except:
                image = None

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
                try:
                    self.serviceAccountId = FN_DECRYPT(self.request.headers.get('service-Account-Key'))
                    if not len(self.serviceAccountId):
                        raise Exception
                    self.serviceAccountId = ObjectId(self.serviceAccountId)
                except Exception as e:
                    self.serviceAccountId = None
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
                if len(app):
                    self.apiId = app[0]['apiId']
                    if self.apiId in [ 402021, 402022, 402020, 402023]:
                        if self.apiId == 402022 or self.apiId == 402020 or self.apiId == 402021 or self.apiId == 402023: # TODO: till here
                            regexSp = re.compile('[@_`+!#$%^&*()<>?/\-|}{~:,.]')
                            regexEm = re.compile('[@`+!#$%^&*()<>?/\|}{~:],')
                            regexNp = re.compile('[1234567890]')
                            try:
                                firstName = str(self.request.arguments['firstName'][0].decode())
                            except:
                                firstName = None
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
                            try:
                                lastName = str(self.request.arguments['lastName'][0].decode())
                            except:
                                lastName = None
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

                            filepath = []
                            imageName = timeNow()
                            imageUpdateStatus = False
                            if image != None:
                                print(image)
                                imageType = image['content_type']
                                imageType = mimetypes.guess_extension(
                                    imageType,
                                    strict=True
                                )
                                if imageType == None:
                                    imageType = pathlib.Path(image['filename']).suffix
                                if str(imageType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                    fName = imageName
                                    fRaw = image['body']
                                    fp = self.fu.tmpPath
                                    if not os.path.exists(fp):
                                        Log.i('DRV-Profile', 'Creating Directories')
                                        os.system('mkdir -p ' + fp)
                                    fpm = fp + '/' + str(fName) + imageType
                                    fh = open(fpm, 'wb')
                                    fh.write(fRaw)
                                    fh.close()
                                    filepath.append(fpm)
                                    os.system('chmod 755 -R ' + fpm + '*')
                                    imageUpdateStatus = True
                                else:
                                    message = 'Invalid File Type has been uploaded'
                                    code = 4011
                                    raise Exception
                            accFindQ = self.account.find(
                                            {
                                                '_id':self.accountId
                                            }
                                        )
                            accFind = []
                            async for i in accFindQ:
                                accFind.append(i)
                            if not len(accFind):
                                code = 4803
                                status = False
                                message = "Profile Not Found"
                                raise Exception
                            accUpdate = await self.account.update_one(
                                                {
                                                    '_id':self.accountId
                                                },
                                                {
                                                    '$set':{
                                                                'firstName':firstName,
                                                                'lastName':lastName
                                                            }
                                                }
                                            )
                            if imageUpdateStatus:
                                accImageUpdate = await self.account.update_one(
                                                {
                                                    '_id':self.accountId
                                                },
                                                {
                                                    '$set':{
                                                                'image':[
                                                                            {
                                                                                'time':imageName,
                                                                                'mimeType':imageType
                                                                            }
                                                                        ]
                                                            }
                                                }
                                            )
                                if accImageUpdate.modified_count == None:
                                    code = 3222
                                    status = False
                                    message = "Image upload Failure"
                                    raise Exception
                                uPath = self.fu.uploads + str(self.entityId)
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + '/profile_pictures/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + str(self.accountId) + '/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                for i in filepath:
                                    os.system('mv ' + i + ' ' + uPath)

                                Log.d(uPath)

                                os.system('chmod 755 -R ' + uPath + '*')

                            if accUpdate.modified_count != None:
                                code = 2000
                                status = True
                                message = "Profile has been updated"
                            else:
                                code = 9432
                                status = False
                                message = "Profile could not be updated"
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

