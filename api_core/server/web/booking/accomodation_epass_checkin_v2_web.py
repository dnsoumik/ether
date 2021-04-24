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
from PIL import Image
from ..lib.lib import *
import numpy
import base64
@xenSecureV1
class MtimeAccomodationePassCheckinV2WebHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ('GET','POST','PUT','OPTIONS')

    account = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][0]['name']
                ]

    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]

    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]
    phoneCountry = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][6]['name']
                ]
    entity = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][5]['name']
                ]

    serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][0]['name']
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

        '''
        try:
            self.request.arguments = json.loads(self.request.headers)
            print(self.request.arguments)
        except Exception as e:
            Log.i(str(e))
            code = 4300
            status = False
            message = "Invalid Booking Request"
            self.write({
                        'result':[],
                        'code':code,
                        'message':message,
                        'status':status
                    })
            self.finish()
            return
        '''
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
                            try:
                                sourceWeb = self.request.arguments['sourceWeb'][0].decode()
                            except:
                                sourceWeb = True
                            if sourceWeb == "true":
                                sourceWeb = True

                            try:
                                touristId = str(self.request.arguments['touristId'][0].decode())
                                try:
                                    touristId = ObjectId(touristId)
                                except:
                                    raise Exception
                            except:
                                code = 7832
                                status = False
                                message = "Invalid Argument - ['touristId']"
                                raise Exception
                            try:
                                aLatitude = float(self.request.arguments['latitude'][0])
                                code, message = Validate.i(
                                                    aLatitude,
                                                    'latitude',
                                                    maxNumber=90,
                                                    minNumber=-90
                                                )
                                if code != 4100:
                                    raise Exception
                            except:
                                code = 4210
                                message = 'Invalid Argument - [ latitude ].'
                                raise Exception


                            try:
                                aLongitude = float(self.request.arguments['longitude'][0])
                                code, message = Validate.i(
                                                    aLongitude,
                                                    'longitude',
                                                    maxNumber=180,
                                                    minNumber=-180
                                                )
                                if code != 4100:
                                    raise Exception
                            except:
                                code = 4210
                                message = 'Invalid Argument - [ longitude ].'
                                raise Exception

                            try:
                                touristMembers = str(self.request.arguments['touristMembers'][0].decode())
                                touristMembers = touristMembers.strip('][').split(', ')
                                if touristMembers == None or touristMembers == [] or type(touristMembers) != list:
                                    raise Exception
                            except:
                                code = 5453
                                status = False
                                message = "Invalid Input- ['touristMembers']"
                                raise Exception


                            try:
                                #numOfAdult = self.request.arguments.get('numOfAdult')
                                numOfRoom = 0
                                code, message = Validate.i(
                                        numOfRoom,
                                        'numOfRoom',
                                        dataType=int,
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ numOfRoom ].'
                                raise Exception

                            try:
                                #numOfAdult = self.request.arguments.get('numOfAdult')
                                numOfAdult = 0
                                code, message = Validate.i(
                                        numOfAdult,
                                        'numOfAdult',
                                        dataType=int,
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ numOfAdult ].'
                                raise Exception
                            try:
                                #numOfChild = self.request.arguments.get('numOfChild')
                                numOfChild = 0
                                code, message = Validate.i(
                                        numOfChild,
                                        'numOfChild',
                                        dataType=int,
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ numOfChild ].'
                                raise Exception

                            proFindQ = self.profile.find(
                                        {
                                            '_id':touristId,
                                            'entityId':self.entityId
                                        }
                                    )
                            proFind = []
                            async for i in proFindQ:
                                proFind.append(i)
                            if not len(proFind):
                                code = 2350
                                status = False
                                message = "Tourist App User Profile not found"
                                raise Exception

                            accFindQ = self.account.find(
                                        {
                                            '_id':proFind[0]['accountId']
                                        }
                                    )
                            accFind = []
                            async for i in accFindQ:
                                accFind.append(i)

                            if not len(accFind):
                                code = 6727
                                status = False
                                message = "Tourist App User Account not found"
                                raise Exception

                            accountData =   [{
                                                    'firstName': accFind[0]['firstName'],
                                                    'lastName': accFind[0]['lastName'],
                                                    'contact':  accFind[0]['contact']
                                            }]

                            sync = False
                            checkinTime = timeNow()

                            serAccQ = self.serviceAccount.find(
                                        {
                                            'profileId':self.profileId,
                                            'serviceType':1,
                                            'disabled':False
                                        },
                                        {
                                            '_id':1
                                        },
                                        limit = 1
                                    )
                            serAcc= []
                            async for i in serAccQ:
                                serAcc.append(i)
                            if not len(serAcc):
                                code = 5660
                                status = False
                                message = "Accomodation Service Account Not Valid"
                                raise Exception
                            serviceAccountId = serAcc[0]['_id']
                            serviceProfileId = self.profileId
                            accountId = self.accountId
                            touristDetails = []
                            # raise Exception
                            bookingId = await self.touristBook.insert_one(
                                            {
                                                'disabled':False,
                                                'entityId':self.entityId,
                                                'serviceAccountId':serviceAccountId,
                                                'primaryTouristInfo':accountData,
                                                'touristId':touristId,
                                                'serviceType':1,
                                                'time':checkinTime,
                                                'modifiedTime':timeNow(),
                                                'providerDetails':
                                                                    [
                                                                        {
                                                                            'id':serviceProfileId,
                                                                            'accountId':accountId
                                                                        }
                                                                    ],
                                                'touristDetails':touristDetails,
                                                'touristCount' : 0,
                                                'liveCheckInCount': 0,
                                                'liveCheckOutCount': 0,
                                                'sendSmsCounter': 0,
                                                'location': [
                                                                {
                                                                    'type': 'Point',
                                                                    'coordinates': [aLongitude, aLatitude]
                                                                }
                                                            ],
                                                'activity': [
                                                                {
                                                                    'id':0,
                                                                    'startTime':0,
                                                                    'endTime':0,
                                                                    'time':checkinTime,
                                                                    'sync':sync
                                                                },
                                                                {
                                                                    'id':1,
                                                                    'time':checkinTime,
                                                                    'sync':sync
                                                                }
                                                            ],
                                                "inventory": [
                                                                {
                                                                    "numOfRoom": numOfRoom,
                                                                    "numOfAdult": numOfAdult,
                                                                    "numOfChild": numOfChild
                                                                }
                                                            ],
                                                "bookType":1
                                            }
                                        )
                            bookingId = bookingId.inserted_id
                            touristIndex = 0
                            for k,j in enumerate(touristMembers):
                                subTouristFindQ = self.subTourist.find(
                                                    {
                                                        '_id':ObjectId(j),
                                                        'profileId':touristId,
                                                    }
                                                )
                                subTouristFind = []
                                async for i in subTouristFindQ:
                                    subTouristFind.append(i)

                                if not len(subTouristFind):
                                    code = 3500
                                    status = False
                                    message = "One of the member entry in ePass is missing/deleted."
                                    raise Exception

                                subId = subTouristFind[0]['_id']

                                if touristIndex == 0:
                                    liveProof = []
                                    for x in range(0,6):
                                        if sourceWeb == True:
                                            try:
                                                liveProof1 = base64.b64decode(self.get_body_argument\
                                                    ('liveProof_' + str(k) + '_' + str(x), default=None, strip=False))
                                                liveProof1Type = ".jpg"
                                            except Exception as e:
                                                Log.i('EXC', e)
                                                code = 4100
                                                message = 'Live Proof Missing'
                                                raise Exception
                                            liveProof.append([liveProof1,liveProof1Type])
                                        else:
                                            try:
                                                liveProof1 = self.request.files['liveProof_' + str(k) + '_' + str(x)][0]
                                                liveProof1Type = liveProof1['content_type']
                                                liveProof1Type = mimetypes.guess_extension(
                                                liveProof1Type,
                                                strict=True
                                                )
                                                if liveProof1Type == None:
                                                    liveProof1Type = pathlib.Path(liveProof1['filename']).suffix
                                            except Exception as e:
                                                Log.i('EXC', e)
                                                code = 4100
                                                message = 'Live Proof Missing'
                                                raise Exception
                                            liveProof.append([liveProof1,liveProof1Type])

                                    img_tag = []
                                    filepath = []
                                    aTime = checkinTime
                                    liveProofTime = []
                                    liveProofType = []

                                    Log.i(sourceWeb)

                                    if sourceWeb:
                                        for y in liveProof:
                                            livetime = aTime + 1
                                            fName = aTime
                                            fp = self.fu.tmpPath
                                            if not os.path.exists(fp):
                                                Log.i('DRV-Profile', 'Creating Directories')
                                                os.system('mkdir -p ' + fp)
                                            fpm = fp + '/' + str(fName) + y[1]
                                            fh = open(fpm, 'w+b')
                                            fh.write(bytearray(y[0]))
                                            fh.close()
                                            img_tag.append([livetime,y[1]])

                                            mainFile = ''
                                            filepath.append(fpm)
                                            os.system('chmod 755 -R ' + fpm + '*')
                                            mainFile = fpm
                                            liveProofTime.append(livetime)
                                            liveProofType.append(y[1])
                                    else:
                                        for y in liveProof:
                                            livetime = aTime + 1
                                            fName = aTime
                                            fRaw = y[0]['body']
                                            fp = self.fu.tmpPath
                                            if not os.path.exists(fp):
                                                Log.i('DRV-Profile', 'Creating Directories')
                                                os.system('mkdir -p ' + fp)
                                            fpm = fp + '/' + str(fName) + y[1]
                                            fh = open(fpm, 'wb')
                                            fh.write(fRaw)
                                            fh.close()
                                            img_tag.append([livetime,y[1]])

                                            mainFile = ''
                                            filepath.append(fpm)
                                            os.system('chmod 755 -R ' + fpm + '*')
                                            mainFile = fpm
                                            liveProofTime.append(livetime)
                                            liveProofType.append(y[1])


                                    liveProof = [
                                                    {
                                                        'time':liveProofTime[0],
                                                        'mimeType':liveProofType[0]
                                                    },
                                                    {
                                                        'time':liveProofTime[1],
                                                        'mimeType':liveProofType[1]
                                                    },
                                                    {
                                                        'time':liveProofTime[2],
                                                        'mimeType':liveProofType[2]
                                                    },
                                                    {
                                                        'time':liveProofTime[3],
                                                        'mimeType':liveProofType[3]
                                                    },
                                                    {
                                                        'time':liveProofTime[4],
                                                        'mimeType':liveProofType[4]
                                                    },
                                                    {
                                                        'time':liveProofTime[5],
                                                        'mimeType':liveProofType[5]
                                                    }
                                            ]

                                else:
                                    aTime = aTime + 1
                                    liveProof = [
                                                    {
                                                        'time': aTime + 1,
                                                        'mimeType': None,
                                                    },
                                                    {
                                                        'time': aTime + 2,
                                                        'mimeType': None,
                                                    },
                                                    {
                                                        'time': aTime + 3,
                                                        'mimeType': None,
                                                    },
                                                    {
                                                        'time': aTime + 4,
                                                        'mimeType': None,
                                                    },
                                                    {
                                                        'time': aTime + 5,
                                                        'mimeType': None,
                                                    },
                                                    {
                                                        'time': aTime + 6,
                                                        'mimeType': None,
                                                    }
                                            ]

                                bookingUpdate = await self.touristBook.update_one(
                                        {
                                            '_id':bookingId,
                                            'touristId':touristId
                                        },
                                        {
                                        "$set":{
                                                    'modifiedTime':timeNow()
                                                },
                                        "$push":{
                                                    'touristDetails':
                                                    {
                                                        'id':str(subId),
                                                        'note' : [ ],
                                                        'faceProof':subTouristFind[0]['faceProof'],
                                                        'primary' : subTouristFind[0]['primary'],
                                                        'liveProof':liveProof,
                                                        'liveProof2':[],
                                                        'documents':subTouristFind[0]['documents'],
                                                        'firstName':subTouristFind[0]['subTouristDetails'][0].get('firstName'),
                                                        'lastName':subTouristFind[0]['subTouristDetails'][0].get('lastName'),
                                                        'address':subTouristFind[0]['subTouristDetails'][0].get('address'),
                                                        'idNumber':subTouristFind[0]['subTouristDetails'][0].get('idNumber'),
                                                        'gender':subTouristFind[0]['subTouristDetails'][0].get('gender'),
                                                        'dateOfBirth':subTouristFind[0]['subTouristDetails'][0].get('dateOfBirth')
                                                            },
                                                    },
                                        "$inc":{
                                                    'touristCount' : 1,
                                                    'liveCheckOutCount':1
                                               },
                                        }

                                    )
                                touristIndex =touristIndex + 1
                                for time_a in img_tag:
                                    imgUpdate = await self.imgWrite.insert_one(
                                                {
                                                    'type':'id',
                                                    'entityId':self.entityId,
                                                    'subkycId':subId,
                                                    'time':time_a[0],
                                                    'mimeType':time_a[1],
                                                    'location': [
                                                                    {
                                                                        'type': 'Point',
                                                                        'coordinates': [aLongitude, aLatitude]
                                                                    }
                                                                ],
                                                    'expireAt': dtime.now()
                                                }
                                            )
                                uPath = self.fu.uploads + '/' + str(self.entityId)
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + '/tourist_kyc'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + '/subtourist/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + str(subId) + '/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                for i in filepath:
                                    os.system('mv ' + i + ' ' + uPath)

                                Log.d(uPath)

                                os.system('chmod 755 -R ' + uPath + '*')
                            res = {
                                    'bookingId':str(bookingId),
                                    'time':checkinTime
                                }
                            result.append(res)
                            code = 2000
                            status = True
                            message = "Primary Tourist is added and booking is initiated."
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

