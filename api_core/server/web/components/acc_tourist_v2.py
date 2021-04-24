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
import pathlib

@xenSecureV1
class MtimeWebAccTouristV2Handler(tornado.web.RequestHandler,
                                MongoMixin):

    SUPPORTED_METHODS = ('GET', 'POST', 'PUT','OPTIONS')

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
    touristPass = MongoMixin.serviceDb[
        CONFIG['database'][1]['table'][20]['name']
    ]
    touristPassV2 = MongoMixin.serviceDb[
        CONFIG['database'][1]['table'][38]['name']
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
                    if app[0]['apiId'] in [402021, 402022, 402023]:  # TODO: till here
                        if self.apiId == 402021:
                            try:
                                pNum = int(self.request.arguments['pNum'][0])
                            except:
                                pNum = None

                            try:
                                passId = str(self.request.arguments['id'][0].decode())
                            except:
                                passId = None


                            if pNum != None:
                                if len(str(pNum)) != 12:
                                    code = 4500
                                    status = False
                                    message = "Invalid Phone Number"
                                    raise Exception

                                accFindQ = self.account.find(
                                    {
                                        'contact.0.value': pNum
                                    },
                                    {
                                        '_id': 1,
                                        'firstName': 1,
                                        'lastName': 1,
                                        'contact': 1
                                    },
                                    limit=1
                                )
                                accFind = []
                                async for i in accFindQ:
                                    accFind.append(i)
                                if not len(accFind):
                                    status = False
                                    code = 4550
                                    message = "No Account found"
                                    raise Exception
                                proFindQ = self.profile.find(
                                    {
                                        'accountId': accFind[0]['_id'],
                                        'entityId': self.entityId,
                                        'applicationId': ObjectId('5e5611bcb0c34f3bb9c2cd36')
                                    }
                                )
                                proFind = []
                                async for i in proFindQ:
                                    proFind.append(i)
                                if not len(proFind):
                                    status = False
                                    code = 4560
                                    message = "No Account found"
                                    raise Exception

                            if passId:
                                passFindQ = self.touristPassV2.find(
                                            {
                                                'entityId':self.entityId,
                                                'passIdn':passId,
                                            }
                                        )
                                passFind = []
                                async for i in passFindQ:
                                    passFind.append(i)
                                if not len(passFind):
                                    code = 4655
                                    status = False
                                    message = "No Pass Found"
                                    raise Exception

                                proFindQ = self.profile.find(
                                    {
                                        '_id': passFind[0]['profileId'],
                                        'entityId': self.entityId,
                                        'applicationId': ObjectId('5e5611bcb0c34f3bb9c2cd36')
                                    }
                                )
                                proFind = []
                                async for i in proFindQ:
                                    proFind.append(i)
                                if not len(proFind):
                                    status = False
                                    code = 4560
                                    message = "No Account Profile found"
                                    raise Exception
                                accFindQ = self.account.find(
                                    {
                                        '_id': proFind[0]['accountId']
                                    },
                                    {
                                        '_id': 1,
                                        'firstName': 1,
                                        'lastName': 1,
                                        'contact': 1
                                    },
                                    limit=1
                                )
                                accFind = []
                                async for i in accFindQ:
                                    accFind.append(i)
                                if not len(accFind):
                                    status = False
                                    code = 4550
                                    message = "No Account found"
                                    raise Exception


                            touMemQ = self.subTourist.find(
                                {
                                    'profileId': proFind[0]['_id'],
                                    '$where': 'this.subTouristDetails != null',
                                    'disabled':False
                                },
                                {
                                    '_id': 1,
                                    'verified': 1,
                                    'disabled': 1,
                                    'primary': 1,
                                    'subTouristDetails': 1,
                                    'documents': 1,
                                    'faceProof': 1,
                                    'location': 1,
                                    'submitRequest': 1
                                }
                            )
                            touMem = []
                            async for i in touMemQ:
                                touMem.append(i)
                            if not len(touMem):
                                status = False
                                code = 4570
                                message = "No tourist member found"
                                raise Exception
                            for res in touMem:
                                for docx in res['documents']:
                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                        + str(self.entityId) + '/tourist_kyc/' \
                                        + 'subtourist/' + str(res['_id']) \
                                        + '/' + \
                                        str(docx['time']) + docx['mimeType']
                                for docx in res['faceProof']:
                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                        + str(self.entityId) + '/tourist_kyc/' \
                                        + 'subtourist/' + str(res['_id']) \
                                        + '/' + \
                                        str(docx['time']) + docx['mimeType']
                                res['id'] = str(res['_id'])
                                res['touristProfile'] = str(proFind[0]['_id'])
                                del res['_id']
                                result.append(res)

                            accFind[0]['_id'] = str(accFind[0]['_id'])
                            accFind[0]['profileId'] = str(proFind[0]['_id'])
                            result = [
                                {
                                    'account': accFind[0],
                                    'members': result
                                }
                            ]
                            status = True
                            code = 2000
                            message = "List of tourist members"
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
            # self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.w('EXC', iMessage)
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' +
                      str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response = {
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
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' +
                  str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response = {
                'code': code,
                'status': status,
                'message': message
            }
            self.write(response)
            self.finish()
            return
    '''
    async def put(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            # URL PARAMS:
            sourceWeb1 = False
            sourceWeb2 = False
            sourceWeb3 = False

            try:
                if (type(self.get_arguments('bookingId')[0]) != str):
                    bookingId = ObjectId(self.get_arguments('bookingId')[0].decode())
                else:
                    bookingId = ObjectId(self.get_arguments('bookingId')[0])
            except Exception as e:
                code = 5670
                Log.i('EXC', e)
                message = "Invalid Booking Id"
                raise Exception

            try:
                if (type(self.get_arguments('subId')[0]) != str):
                    subId = ObjectId(self.get_arguments('subId')[0].decode())
                else:
                    subId = ObjectId(self.get_arguments('subId')[0])
            except:
                code = 5670
                message = "Invalid Tourist Id"
                raise Exception

            if True:
                try:
                    image1 = self.request.files['image1'][0]
                except Exception as e:
                    Log.i('EXC', e)
                    code = 4100
                    message = 'Image Proof-1 Missing'
                    raise Exception
                try:
                    image2 = self.request.files['image2'][0]
                except Exception as e:
                    Log.i('EXC', e)
                    code = 4100
                    message = 'Image Proof-2 Missing'
                    raise Exception
                try:
                    image3 = self.request.files['image3'][0]
                except Exception as e:
                    Log.i('EXC', e)
                    code = 4100
                    message = 'Image Proof-3 Missing'
                    raise Exception
                try:
                    image4 = self.request.files['image4'][0]
                except Exception as e:
                    Log.i('EXC', e)
                    code = 4100
                    message = 'Image Proof-4 Missing'
                    raise Exception
                try:
                    image5 = self.request.files['image5'][0]
                except Exception as e:
                    Log.i('EXC', e)
                    code = 4100
                    message = 'Image Proof-5 Missing'
                    raise Exception
                try:
                    image6 = self.request.files['image6'][0]
                except Exception as e:
                    Log.i('EXC', e)
                    code = 4100
                    message = 'Image Proof-6 Missing'
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
                    if self.apiId in [ 402021, 30216, 20216 ]:
                        if self.apiId == 402021: # TODO: till here
                            #idProofId = "Aadhaar Card"
                            #aLongitude = 88.4386982
                            #aLatitude = 22.5825182
                            #aTime = timeNow()
                            try:
                                aLongitude = float(self.get_arguments('longitude')[0])
                                code, message = Validate.i(
                                         aLongitude,
                                         'longitude',
                                         maxNumber=180,
                                         minNumber=-180
                                    )
                                if code != 4100:
                                    raise Exception
                            except:
                                aLongitude = 0.0
                            try:
                                aLatitude = float(self.get_arguments('latitude')[0])
                                code, message = Validate.i(
                                         aLatitude,
                                         'latitude',
                                         maxNumber=90,
                                         minNumber=-90
                                    )
                                if code != 4100:
                                    raise Exception
                            except:
                                aLatitude = 0.0

                            try:
                                aTime = int(self.get_arguments('time')[0])
                                code, message = Validate.i(
                                    aTime,
                                    'time',
                                    maxNumber=(timeNow() + 3600000000),
                                    minNumber=(timeNow() - 3600000000)
                                )
                                if code != 4100:
                                    raise Exception
                            except:
                                aTime = timeNow()

                            if True:
                                aTime = aTime + 1
                                if str(image1Type) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                    fName = a
                                    fRaw = image1['body']
                                    fp = self.fu.tmpPath
                                    if not os.path.exists(fp):
                                        Log.i('DRV-Profile', 'Creating Directories')
                                        os.system('mkdir -p ' + fp)
                                    fpm = fp + '/' + str(fName) + image1Type
                                    fh = open(fpm, 'wb')
                                    fh.write(fRaw)
                                    fh.close()
                                    img_tag.append([id1Time,id1ProofType])

                                    mainFile = ''
                                    filepath.append(fpm)
                                    os.system('chmod 755 -R ' + fpm + '*')
                                    mainFile = fpm
                                else:
                                    code = 3920
                                    status = False
                                    message = "Invalid File Type"
                                    raise Exception



                            bookingPriFindQ = self.touristBook.find(
                                                    {
                                                        '_id':bookingId,
                                                        'touristId':touristId
                                                    },
                                                    {
                                                        '_id':0,
                                                        'touristDetails':1,
                                                        'bookType':1,
                                                        'activity':1
                                                    }
                                                )
                            bookingPriFind = []
                            async for i in bookingPriFindQ:
                                bookingPriFind.append(i)
                            if not len(bookingPriFind[0]['touristDetails']):
                                primary = True
                            else:
                                primary = False
                            if bookingPriFind[0]['bookType'] in [0,1] and len(bookingPriFind[0]['activity']) == 1:
                                activityUpdate = await self.touristBook.update_one(
                                                    {
                                                        '_id':bookingId,
                                                        'touristId':touristId
                                                    },
                                                    {
                                                        '$push':{
                                                                    'activity':{
                                                                                    'id':1,
                                                                                    'time':timeNow()
                                                                                }
                                                                }
                                                    }
                                                )
                            subTouristDetails = []
                            v = {
                                    'firstName':firstName,
                                    'lastName':lastName,
                                    'address':address,
                                    'dateOfBirth':dateOfBirth,
                                    'gender':gender,
                                    'idNumber':idNumber
                                }
                            subTouristDetails.append(v)
                            subTouristFindQ = self.subTourist.find(
                                                    {
                                                        'time':aTime,
                                                        'profileId':touristId,
                                                        'entityId':self.entityId
                                                    }
                                            )
                            subTouristFind = []
                            async for i in subTouristFindQ:
                                subTouristFind.append(i)
                            if len(subTouristFind):
                                code = 8493
                                status = True
                                message = "Subtourist is already added"
                                response =  {
                                                'code': code,
                                                'status': status,
                                                'message': message
                                            }
                                Log.d('RSP', response)
                                response['result'] = result
                                self.write(response)
                                self.finish()
                                return

                            try:
                                subkycInsert = await self.subTourist.insert_one(
                                            {
                                                'faceProof':[
                                                                {
                                                                    'time':faceTime,
                                                                    'mimeType':faceProofType
                                                                }
                                                            ],
                                                'documents':[
                                                                {
                                                                    'time':id1Time,
                                                                    'mimeType':id1ProofType,
                                                                    'idType':idProofId
                                                                },
                                                                {
                                                                    'time':id2Time,
                                                                    'mimeType':id2ProofType,
                                                                    'idType':idProofId
                                                                }
                                                            ],
                                                'location': [
                                                                {
                                                                    'type': 'Point',
                                                                    'coordinates': [aLongitude, aLatitude]
                                                                }
                                                            ],
                                                'time':aTime,
                                                'modifiedTime':aTime,
                                                'expireAt': dtime.now(),
                                                'profileId':touristId,
                                                'entityId':self.entityId,
                                                'verified':True,
                                                'disabled':False,
                                                'primary':primary,
                                                'submitRequest':[0,1],
                                                'subTouristDetails':subTouristDetails
                                            }
                                    )
                                subkycFindQ = self.subTourist.find(
                                                {
                                                    'profileId':touristId,
                                                    'entityId':self.entityId,
                                                    'primary':primary,
                                                    'subTouristDetails':subTouristDetails
                                                }
                                            )
                                subkycFind = []
                                async for i in subkycFindQ:
                                    subkycFind.append(i)
                                subkycId = subkycFind[0]['_id']
                            except:
                                code = 4550
                                status = False
                                message = "Error in creating member. Please contact Support"
                                raise Exception
                            #TODO::Need to give expired time.
                            bookingUpdate = await self.touristBook.update_one(
                                        {
                                            '_id':bookingId,
                                            'touristId':touristId
                                        },
                                        {
                                        "$push":{
                                                    'touristDetails':
                                                                        {
                                                                            'id':str(subkycId),
                                                                            'note' : [ ],
                                                                            'faceProof':[
                                                                                            {
                                                                                                'time':faceTime,
                                                                                                'mimeType':faceProofType
                                                                                            }
                                                                                        ],
                                                                            'primary' : primary,
                                                                            'liveProof':[
                                                                                            {
                                                                                                'time':image1Time,
                                                                                                'mimeType':image1ProofType
                                                                                            },
                                                                                            {
                                                                                                'time':image2Time,
                                                                                                'mimeType':image2ProofType
                                                                                            },
                                                                                            {
                                                                                                'time':image3Time,
                                                                                                'mimeType':image3ProofType
                                                                                            },
                                                                                            {
                                                                                                'time':image4Time,
                                                                                                'mimeType':image4ProofType
                                                                                            },
                                                                                            {
                                                                                                'time':image5Time,
                                                                                                'mimeType':image5ProofType
                                                                                            },
                                                                                            {
                                                                                                'time':image6Time,
                                                                                                'mimeType':image6ProofType
                                                                                            },
                                                                                        ],
                                                                            'liveProof2':[],
                                                                            'documents':[
                                                                                            {
                                                                                                'time':id1Time,
                                                                                                'mimeType':id1ProofType,
                                                                                                'idType':idProofId
                                                                                            },
                                                                                            {
                                                                                                'time':id2Time,
                                                                                                'mimeType':id2ProofType,
                                                                                                'idType':idProofId
                                                                                            }
                                                                                        ],
                                                                            'firstName':firstName,
                                                                            'lastName':lastName,
                                                                            'address':address,
                                                                            'idNumber':idNumber,
                                                                            'gender':gender,
                                                                            'dateOfBirth':dateOfBirth
                                                                            },
                                                    },
                                        "$inc":{
                                                    'touristCount' : 1,
                                                    'liveCheckOutCount':1
                                               },
                                        }

                                    )
                            if True:
                                for time_a in img_tag:
                                    imgUpdate = await self.imgWrite.insert_one(
                                                {
                                                    'type':'id',
                                                    'entityId':self.entityId,
                                                    'subkycId':subkycId,
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
                                # Moving Temp dir to booking dir
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

                                uPath = uPath + str(subkycId) + '/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                for i in filepath:
                                    os.system('mv ' + i + ' ' + uPath)

                                Log.d(uPath)

                                os.system('chmod 755 -R ' + uPath + '*')
                                result.append(
                                    {'bookingId': str(bookingId),
                                     'subtouristId': str(subkycId),
                                     'ocrData':ocrData
                                    }
                                    )
                                code = 2000
                                status = True
                                message = "Tourist Entry has been uploaded."
                            else:
                                code = 5730
                                status = False
                                message = "Invalid Booking"
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
                                'disabled': False,
                                '_id': self.applicationId
                            },
                            {
                                'apiId': 1
                            },
                            limit=1
                        )
                app = []
                async for i in appQ:
                    app.append(i)
                if len(app):
                    self.apiId = app[0]['apiId']
                    if self.apiId in [ 402020, 402021, 402022 ]: # TODO: till here
                        if self.apiId == 402021:
                            try:
                                bookingId = ObjectId(self.request.arguments.get('bookingId'))
                            except:
                                code = 4560
                                status = False
                                message = "Invalid Booking Id"
                                raise Exception
                            try:
                                subtouristId = ObjectId(self.request.arguments.get('subtouristId'))
                            except:
                                code = 4570
                                status = False
                                message = "Invalid Tourist Id"
                                raise Exception

                            cFirstName = self.request.arguments.get('firstName')
                            if cFirstName == None or cFirstName == '':
                                code = 4755
                                status = False
                                message = "First Name cannot be empty"
                                raise Exception
                            code,message = Validate.i(
                                            cFirstName,
                                            'First Name',
                                            notEmpty = True,
                                            maxLength = 50,
                                            noSpecial = True,
                                            noNumber = True
                                        )

                            if code != 4100:
                                raise Exception



                            cLastName = self.request.arguments.get('lastName')
                            if cLastName == None or cLastName == '':
                                code = 4755
                                status = False
                                message = "Last Name cannot be empty"
                                raise Exception
                            code,message = Validate.i(
                                            cLastName,
                                            'Last Name',
                                            notEmpty = True,
                                            maxLength = 50,
                                            noSpecial = True,
                                            noNumber = True
                                        )

                            if code != 4100:
                                raise Exception

                            cAddress = self.request.arguments.get('address')
                            if cAddress == None or cAddress == '':
                                code = 4755
                                status = False
                                message = "Address cannot be empty"
                                raise Exception
                            code,message = Validate.i(
                                            cAddress,
                                            'Address',
                                            notEmpty = True,
                                            maxLength = 1000,
                                        )

                            if code != 4100:
                                raise Exception

                            idNumber = self.request.arguments.get('idNumber')
                            if idNumber == None or idNumber == '':
                                code = 4755
                                status = False
                                message = "Id Number cannot be empty"
                                raise Exception
                            code,message = Validate.i(
                                            idNumber,
                                            'idNumber',
                                            notEmpty = True,
                                            maxLength = 1000,
                                        )

                            if code != 4100:
                                raise Exception

                            dateOfBirth = self.request.arguments.get('dob')
                            if dateOfBirth == None or dateOfBirth == '':
                                code = 4755
                                status = False
                                message = "Date of birth cannot be empty"
                                raise Exception
                            code,message = Validate.i(
                                            dateOfBirth,
                                            'dateOfBirth',
                                            notEmpty = True,
                                            maxLength = 1000,
                                        )

                            if code != 4100:
                                raise Exception

                            gender = self.request.arguments.get('gender')
                            if gender == None or gender == '':
                                code = 4755
                                status = False
                                message = "Gender cannot be empty"
                                raise Exception
                            if gender.upper() not in ['MALE','FEMALE','M','F','OTHER']:
                                code = 4755
                                status = False
                                message = "Invalid Gender"
                                raise Exception
                            code,message = Validate.i(
                                            gender,
                                            'gender',
                                            notEmpty = True,
                                            maxLength = 1000,
                                        )

                            if code != 4100:
                                raise Exception
                            touDetailsUpdate = await self.touristBook.update_one(
                                                                {
                                                                    '_id':bookingId,
                                                                    'touristDetails.id': str(subtouristId)
                                                                },
                                                                {
                                                                '$set': {
                                                                            'touristDetails.$.firstName': cFirstName,
                                                                            'touristDetails.$.lastName': cLastName,
                                                                            'touristDetails.$.address': cAddress,
                                                                            'touristDetails.$.idNumber': idNumber,
                                                                            'touristDetails.$.dateOfBirth': dateOfBirth,
                                                                            'touristDetails.$.gender': gender,
                                                                        }
                                                                }
                                                    )
                            if True:
                                v = {
                                        'bookingId':str(bookingId)
                                    }
                                result.append(v)
                                subTouristDetails = []
                                v = {
                                        'firstName':cFirstName,
                                        'lastName':cLastName,
                                        'address':cAddress,
                                        'idNumber':idNumber,
                                        'dateOfBirth':dateOfBirth,
                                        'gender':gender
                                    }
                                subTouristDetails.append(v)
                                kycUpdate = await self.subTourist.update_one(
                                    {
                                        '_id':subtouristId
                                    },
                                    {
                                    '$set': {
                                                'subTouristDetails':subTouristDetails,
                                                'expireAt': None
                                            }
                                    }
                                    )
                                code = 2000
                                status = True
                                message = "Tourist contact information has been updated"
                            else:
                                code = 2002
                                status = False
                                message = "Invalid Booking."

                        else:
                            code = 4003
                            self.set_status(401)
                            message = 'You are not Authorized'
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
    '''
    #@defer.inlineCallbacks
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
                    if self.apiId in [402021, 402022]:
                        if self.apiId == 402021:
                            touMem = self.request.arguments.get(
                                'touristMembers')
                            if not len(touMem):
                                code = 4760
                                status = False
                                message = "No Tourist Added"
                                raise Exception
                            try:
                                touristId = ObjectId(
                                    self.request.arguments.get('touristId'))
                            except:
                                code = 4770
                                status = False
                                message = "Invalid Tourist Id"
                                raise Exception
                            try:
                                #numOfRoom = self.request.arguments.get('numOfRoom')
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
                            touCount = len(touMem)
                            touProQ  = self.profile.find(
                                {
                                    '_id': touristId
                                }
                            )
                            touPro = []
                            async for i in touProQ:
                                touPro.append(i)
                            if not len(touPro):
                                code = 4500
                                status = False
                                message = "Tourist Profile Not Found"
                                raise Exception
                            touAccQ = self.account.find(
                                    {
                                        '_id': touPro[0]['accountId']
                                    }
                                )
                            touAcc = []
                            async for i in touAccQ:
                                touAcc.append(i)
                            if not len(touAcc):
                                code = 4555
                                status = False
                                message = "Account not Found"
                                raise Exception

                            primaryTouristInfo = []
                            v = {
                                    'firstName':touAcc[0]['firstName'],
                                    'lastName':touAcc[0]['lastName'],
                                    'contact':touAcc[0]['contact']
                                }
                            primaryTouristInfo.append(v)

                            serAccQ = self.serviceAccount.find(
                                {
                                    'profileId': self.profileId
                                }
                            )
                            serAcc = []
                            async for i in serAccQ:
                                serAcc.append(i)
                            serviceAccountId = serAcc[0]['_id']
                            touristDetails = []
                            for resId in touMem:
                                touAccQ = self.subTourist.find(
                                    {
                                        '_id': ObjectId(resId)
                                    },
                                    {
                                        '_id': 1,
                                        'subTouristDetails': 1,
                                        'faceProof': 1,
                                        'documents': 1,
                                        'primary': 1
                                    }
                                )
                                touAcc = []
                                async for i in touAccQ:
                                    touAcc.append(i)
                                v = {
                                    'id': str(touAcc[0]['_id']),
                                    'firstName': touAcc[0]['subTouristDetails'][0]['firstName'],
                                    'lastName': touAcc[0]['subTouristDetails'][0]['lastName'],
                                    'address': touAcc[0]['subTouristDetails'][0]['address'],
                                    'documents': touAcc[0]['documents'],
                                    'faceProof': touAcc[0]['faceProof'],
                                    'liveProof': [],
                                    'liveProof2':[],
                                    'note': [],
                                    'primary': touAcc[0]['primary']
                                }
                                touristDetails.append(v)
                            if self.serviceAccountId == None:
                                serAccQ = self.serviceAccount.find(
                                        {
                                            'profileId':self.profileId,
                                            'serviceType':1
                                        },
                                        {
                                            '_id':1
                                        },
                                        limit = 1
                                    )
                                serAcc = []
                                async for i in serAccQ:
                                    serAcc.append(i)
                                if not len(serAcc):
                                    code = 6785
                                    status = False
                                    message = "Service Account Not Found"
                                    raise Exception
                                serviceAccountId = serAcc[0]['_id']
                                serviceProfileId = self.profileId
                                accountId = self.accountId
                            else:
                                serAccQ = self.serviceAccount.find(
                                        {
                                            'profileId':self.serviceAccountId,
                                            'serviceType':1
                                        },
                                        {
                                            'profileId':1
                                        },
                                        limit = 1
                                    )
                                serAcc = []
                                async for i in serAccQ:
                                    serAcc.append(i)
                                if len(serAcc):
                                    serviceAccountId = serAcc[0]['_id']
                                    serviceProfileId = serAcc[0]['profileId']
                                else:
                                    code = 3555
                                    status = False
                                    message = "Service Account Not available"
                                    raise Exception
                                accFindQ = self.profile.find(
                                            {
                                                '_id':serviceProfileId
                                            },
                                            {
                                                '_id':1
                                            },
                                            limit = 1
                                        )
                                accFind = []
                                async for i in accFindQ:
                                    accFind.append(i)
                                if len(accFind):
                                    accountId = accFind[0]['_id']
                                else:
                                    code = 3555
                                    status = False
                                    message = "Account Not available"
                                    raise Exception

                            bookingId = await self.touristBook.insert_one(
                                {
                                    'touristCount': touCount,
                                    'liveCheckInCount': touCount,
                                    'liveCheckOutCount': touCount,
                                    'serviceAccountId': serviceAccountId,
                                    'serviceType': 1,
                                    'touristDetails': touristDetails,
                                    'disabled': False,
                                    'primaryTouristInfo' : primaryTouristInfo,
                                    'providerDetails': [
                                        {
                                            'id': serviceProfileId,
                                            'accountId': accountId
                                        }
                                    ],
                                    "entityId": self.entityId,
                                    "sendSmsCounter": 0,
                                    "time": timeNow(),
                                    "activity": [
                                        {
                                            "id": 0,
                                            "startTime": 0,
                                            "endTime": 0,
                                            "time": timeNow()
                                        },
                                        {
                                            "id": 1,
                                            "time": timeNow()
                                        }
                                    ],
                                    "location": [],
                                    "inventory": [
                                        {
                                            "numOfRoom": numOfRoom,
                                            "numOfAdult": numOfAdult,
                                            "numOfChild": numOfChild
                                        }
                                    ],
                                    'touristId': touristId,
                                    'bookType':1
                                }
                            )
                            bookingId = bookingId.inserted_id
                            result.append(str(bookingId))
                            code = 2000
                            status = True
                            message = "Booking Initiated"
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
            # self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' +
                      str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response = {
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
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' +
                  str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response = {
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
                image1 = self.request.files['image1'][0]
            except Exception as e:
                code = 4100
                message = 'Image Proof-1 Missing'
                raise Exception
            try:
                image2 = self.request.files['image2'][0]
            except Exception as e:
                code = 4100
                message = 'Image Proof-2 Missing'
                raise Exception
            try:
                image3 = self.request.files['image3'][0]
            except Exception as e:
                code = 4100
                message = 'Image Proof-3 Missing'
                raise Exception
            try:
                image4 = self.request.files['image4'][0]
            except Exception as e:
                code = 4100
                message = 'Image Proof-4 Missing'
                raise Exception
            try:
                image5 = self.request.files['image5'][0]
            except Exception as e:
                code = 4100
                message = 'Image Proof-5 Missing'
                raise Exception
            try:
                image6 = self.request.files['image6'][0]
            except Exception as e:
                code = 4100
                message = 'Image Proof-6 Missing'
                raise Exception
            '''
            try:
                liveProof = self.request.files['liveProof'][0]
            except Exception as e:
                code = 4100
                message = 'Need a live video proof.'
                raise Exception
            '''
            try:
                bookingId = ObjectId(self.request.arguments['bookingId'][0].decode())
            except:
                code == 4310
                message = 'Invalid Argument - [ Booking Id ].'
                raise Exception
            try:
                subId = ObjectId(self.request.arguments['subId'][0].decode())
            except:
                code == 4320
                message = 'Invalid Argument - [ Subtourist Id ].'
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
                    if self.apiId in [402021, 402022]:
                        if self.apiId == 402021:
                            priTouQ = self.touristBook.find(
                                {
                                    '_id': bookingId

                                }
                            )
                            priTou = []
                            async for i in priTouQ:
                                priTou.append(i)
                            if not len(priTou):
                                code = 4620
                                status = False
                                message = "Invalid Booking"
                                raise Exception

                            filepath = []
                            '''
                            liveProofType = liveProof['content_type']
                            liveProofType = yield mimetypes.guess_extension(
                                liveProofType,
                                strict=True
                            )
                            liveTime = timeNow()
                            if str(liveProofType) in ['.mp4']:
                                fName = liveTime
                                fRaw = liveProof['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + liveProofType
                                filepath.append(fpm)
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()

                            else:
                                message = 'Invalid File Type for Video Proof.'
                                code = 4040
                                raise Exception
                            '''
                            image1ProofType = image1['content_type']
                            image1ProofType = mimetypes.guess_extension(
                                            image1ProofType,
                                            strict=True
                                )
                            if image1ProofType == None:
                                image1ProofType = pathlib.Path(image1['filename']).suffix
                            image2ProofType = image2['content_type']
                            image2ProofType = mimetypes.guess_extension(
                                            image2ProofType,
                                            strict=True
                                )
                            if image2ProofType == None:
                                image2ProofType = pathlib.Path(image2['filename']).suffix
                            image3ProofType = image3['content_type']
                            image3ProofType = mimetypes.guess_extension(
                                            image3ProofType,
                                            strict=True
                                )
                            if image3ProofType == None:
                                image3ProofType = pathlib.Path(image3['filename']).suffix
                            image4ProofType = image4['content_type']
                            image4ProofType = mimetypes.guess_extension(
                                            image4ProofType,
                                            strict=True
                                )
                            if image4ProofType == None:
                                image4ProofType = pathlib.Path(image4['filename']).suffix
                            image5ProofType = image5['content_type']
                            image5ProofType = mimetypes.guess_extension(
                                            image5ProofType,
                                            strict=True
                                )
                            if image5ProofType == None:
                                image5ProofType = pathlib.Path(image5['filename']).suffix
                            image6ProofType = image6['content_type']
                            image6ProofType = mimetypes.guess_extension(
                                            image6ProofType,
                                            strict=True
                                )
                            if image6ProofType == None:
                                image6ProofType = pathlib.Path(image6['filename']).suffix
                            filepath = []
                            img_tag = []
                            aTime = timeNow()
                            image1Time = aTime
                            img_tag.append(image1Time)
                            if str(image1ProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                fName = image1Time
                                fRaw = image1['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + image1ProofType
                                fh = open(fpm, 'wb')
                                fh.write(fRaw)
                                fh.close()

                                mainFile = ''
                                # Converting to PNG
                                if str(image1ProofType) not in ['.png']:
                                    image1ProofType = '.png'
                                    fpx = fp + '/' + str(fName) + image1ProofType
                                    filepath.append(fpx)
                                    im = Image.open(fpm)
                                    im.save(fpx, 'PNG')
                                    os.system('rm ' + fpm)
                                    os.system('chmod 755 -R ' + fp + '*')
                                    mainFile = fpx
                                else:
                                    filepath.append(fpm)
                                    os.system('chmod 755 -R ' + fpm + '*')
                                    mainFile = fpm

                            aTime = aTime + 1
                            image2Time = aTime
                            img_tag.append(image2Time)
                            if str(image2ProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                fName = image2Time
                                fRaw = image2['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + image2ProofType
                                fh = open(fpm, 'wb')
                                fh.write(fRaw)
                                fh.close()

                                mainFile = ''
                                # Converting to PNG
                                if str(image2ProofType) not in ['.png']:
                                    image2ProofType = '.png'
                                    fpx = fp + '/' + str(fName) + image2ProofType
                                    filepath.append(fpx)
                                    im = Image.open(fpm)
                                    im.save(fpx, 'PNG')
                                    os.system('rm ' + fpm)
                                    os.system('chmod 755 -R ' + fp + '*')
                                    mainFile = fpx
                                else:
                                    filepath.append(fpm)
                                    os.system('chmod 755 -R ' + fpm + '*')
                                    mainFile = fpm

                            aTime = aTime + 1
                            faceTime = aTime
                            faceProofType = ".png"
                            image3Time = aTime
                            img_tag.append(image3Time)
                            if str(image3ProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                fName = image3Time
                                fRaw = image3['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + image3ProofType
                                fh = open(fpm, 'wb')
                                fh.write(fRaw)
                                fh.close()

                                mainFile = ''
                                # Converting to PNG
                                if str(image3ProofType) not in ['.png']:
                                    image3ProofType = '.png'
                                    fpx = fp + '/' + str(fName) + image3ProofType
                                    filepath.append(fpx)
                                    im = Image.open(fpm)
                                    im.save(fpx, 'PNG')
                                    os.system('rm ' + fpm)
                                    os.system('chmod 755 -R ' + fp + '*')
                                    mainFile = fpx
                                else:
                                    filepath.append(fpm)
                                    os.system('chmod 755 -R ' + fpm + '*')
                                    mainFile = fpm
                            aTime = aTime + 1
                            image4Time = aTime
                            img_tag.append(image4Time)
                            if str(image4ProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                fName = image4Time
                                fRaw = image4['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + image4ProofType
                                fh = open(fpm, 'wb')
                                fh.write(fRaw)
                                fh.close()

                                mainFile = ''
                                # Converting to PNG
                                if str(image4ProofType) not in ['.png']:
                                    image4ProofType = '.png'
                                    fpx = fp + '/' + str(fName) + image4ProofType
                                    filepath.append(fpx)
                                    im = Image.open(fpm)
                                    im.save(fpx, 'PNG')
                                    os.system('rm ' + fpm)
                                    os.system('chmod 755 -R ' + fp + '*')
                                    mainFile = fpx
                                else:
                                    filepath.append(fpm)
                                    os.system('chmod 755 -R ' + fpm + '*')
                                    mainFile = fpm
                            aTime = aTime + 1
                            image5Time = aTime
                            img_tag.append(image5Time)
                            if str(image5ProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                fName = image5Time
                                fRaw = image5['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + image5ProofType
                                fh = open(fpm, 'wb')
                                fh.write(fRaw)
                                fh.close()

                                mainFile = ''
                                # Converting to PNG
                                if str(image5ProofType) not in ['.png']:
                                    image5ProofType = '.png'
                                    fpx = fp + '/' + str(fName) + image5ProofType
                                    filepath.append(fpx)
                                    im = Image.open(fpm)
                                    im.save(fpx, 'PNG')
                                    os.system('rm ' + fpm)
                                    os.system('chmod 755 -R ' + fp + '*')
                                    mainFile = fpx
                                else:
                                    filepath.append(fpm)
                                    os.system('chmod 755 -R ' + fpm + '*')
                                    mainFile = fpm
                            aTime = aTime + 1
                            image6Time = aTime
                            img_tag.append(image6Time)
                            if str(image6ProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                fName = image6Time
                                fRaw = image6['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + image6ProofType
                                fh = open(fpm, 'wb')
                                fh.write(fRaw)
                                fh.close()

                                mainFile = ''
                                # Converting to PNG
                                if str(image6ProofType) not in ['.png']:
                                    image6ProofType = '.png'
                                    fpx = fp + '/' + str(fName) + image6ProofType
                                    filepath.append(fpx)
                                    im = Image.open(fpm)
                                    im.save(fpx, 'PNG')
                                    os.system('rm ' + fpm)
                                    os.system('chmod 755 -R ' + fp + '*')
                                    mainFile = fpx
                                else:
                                    filepath.append(fpm)
                                    os.system('chmod 755 -R ' + fpm + '*')
                                    mainFile = fpm

                            subUpdate = await self.touristBook.update_one(
                                {
                                    '_id': bookingId,
                                    'touristDetails.id': str(subId)
                                },
                                {
                                    '$set': {
                                        'touristDetails.$.liveProof': [
                                                                        {
                                                                            'time':image1Time,
                                                                            'mimeType':image1ProofType
                                                                        },
                                                                        {
                                                                            'time':image2Time,
                                                                            'mimeType':image2ProofType
                                                                        },
                                                                        {
                                                                            'time':image3Time,
                                                                            'mimeType':image3ProofType
                                                                        },
                                                                        {
                                                                            'time':image4Time,
                                                                            'mimeType':image4ProofType
                                                                        },
                                                                        {
                                                                            'time':image5Time,
                                                                            'mimeType':image5ProofType
                                                                        },
                                                                        {
                                                                            'time':image6Time,
                                                                            'mimeType':image6ProofType
                                                                        },
                                                                    ],
                                            },
                                    '$inc': {
                                        'liveCheckInCount': -1,
                                    }
                                }

                            )
                            if subUpdate.modified_count != None:
                                result.append(str(bookingId))
                                code = 2000
                                status = True
                                message = "Live Proof has been added"

                                uPath = self.fu.uploads + \
                                    '/' + str(self.entityId)
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

                            else:
                                code = 2002
                                status = False
                                message = "Invalid Booking"
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
            # self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' +
                      str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response = {
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
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' +
                  str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response = {
                'code': code,
                'status': status,
                'message': message
            }
            self.write(response)
            self.finish()
