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
import numpy as np
import pathlib

@xenSecureV1
class MtimeAccomodationNoregCheckinHandler(tornado.web.RequestHandler,
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

                            try:
                                aLatitude = float(self.request.headers.get('latitude'))
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
                                aLongitude = float(self.request.headers.get('longitude'))
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
                                            'applicationId': ObjectId('5e5611bcb0c34f3bb9c2cd36')
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
                                    primaryTouristId = await self.profile.insert_one(
                                        {
                                            'active': True,
                                            'locked': False,
                                            'closed': False,
                                            'entityId': self.entityId,
                                            'applicationId': ObjectId("5e5611bcb0c34f3bb9c2cd36"),
                                            'accountId': ObjectId(accountId),
                                            'data':[]
                                        }
                                    )
                                    Log.i(primaryTouristId, 'New Profile Created!')
                                    primaryTouristId = str(primaryTouristId.inserted_id)
                                else:
                                    primaryTouristId = proFind[0]['_id']
                            except:
                                code = 4560
                                status = False
                                message = "Internal Error. Please contact the Support Team"
                                raise Exception

                            sync = False
                            checkinTime = timeNow()

                            sync = self.request.headers.get('sync')
                            if sync == "true":
                                sync = True
                            elif sync == "false":
                                sync = False
                            if sync != None:
                                if type(sync) != bool:
                                    code = 2894
                                    status = False
                                    message = "Invalid argument - ['sync']"
                                    raise Exception
                                if sync == True:
                                    try:
                                        checkinTime = int(self.request.headers.get('time'))
                                    except:
                                        code = 8985
                                        status = False
                                        message = "Invalid argument - ['time']"
                                        raise Exception
                            ticketId = np.base_repr(checkinTime, base=36)

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
                            Log.i('Primary Tourist Id - ', primaryTouristId)
                            touristDetails = []


                            touristId = ObjectId(primaryTouristId)
                            if True:
                                touristCount = self.request.headers.get('touristDetails')
                                # print(touristCount)
                                touristCountStr = json.loads(touristCount)
                            else:
                                code = 5453
                                status = False
                                message = "Invalid Input"
                            # print (touristCount)
                            insSubKyc = []

                            # raise Exception
                            alBookingQuery = self.touristBook.find(
                                        {
                                            'time': checkinTime,
                                        },
                                        {
                                            '_id': 1,
                                            'time': 1,
                                            'touristDetails': 1
                                        }
                                    )
                            alBookingQ = []
                            async for b in alBookingQuery:
                                alBookingQ.append(b)
                                for j in b['touristDetails']:
                                    insSubKyc.append(j['id'])

                            if len(alBookingQ):
                                touristCountStr = []

                            for k,j in enumerate(touristCountStr):
                                Log.i('subTourist', j)
                                #Get info of each subtourist with media file
                                #Inside for loop, insert new subTourist table entry and push to touristBook entry
                                #write to image tag
                                try:
                                    idProofId = j['idProofType']
                                    code, message = Validate.i(
                                        idProofId,
                                        'Id Proof Type',
                                    )
                                    if code != 4100:
                                        raise Exception
                                except Exception as e:
                                    code = 4210
                                    message = 'Invalid Argument - [ idProofType ].'
                                    raise Exception
                                if idProofId == 'Voter ID Card':
                                    idProofId = 'Voter Id Card'

                                try:
                                    id1Proof = self.request.files['id1Proof_'+ str(k)][0]
                                    id1ProofType = id1Proof['content_type']
                                    id1ProofType = mimetypes.guess_extension(
                                    id1ProofType,
                                    strict=True
                                    )
                                    if id1ProofType == None:
                                        id1ProofType = pathlib.Path(id1Proof['filename']).suffix
                                except Exception as e:
                                    Log.i('EXC', e)
                                    code = 4102
                                    message = 'Need front side image of ID'
                                    raise Exception
                                try:
                                    id2Proof = self.request.files['id2Proof_' + str(k)][0]
                                    id2ProofType = id2Proof['content_type']
                                    id2ProofType = mimetypes.guess_extension(
                                    id2ProofType,
                                    strict=True
                                    )
                                    if id2ProofType == None:
                                        id2ProofType = pathlib.Path(id2Proof['filename']).suffix
                                except Exception as e:
                                    Log.i('EXC', e)
                                    code = 4102
                                    message = 'Need back side image of ID'
                                    raise Exception

                                liveProof = []
                                for x in range(0,6):
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
                                aTime = aTime + 1
                                id1Time = aTime
                                if str(id1ProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                    fName = id1Time
                                    fRaw = id1Proof['body']
                                    fp = self.fu.tmpPath
                                    if not os.path.exists(fp):
                                        Log.i('DRV-Profile', 'Creating Directories')
                                        os.system('mkdir -p ' + fp)
                                    fpm = fp + '/' + str(fName) + id1ProofType
                                    fh = open(fpm, 'wb')
                                    fh.write(fRaw)
                                    fh.close()
                                    img_tag.append([id1Time,id1ProofType])

                                    mainFile = ''
                                    filepath.append(fpm)
                                    os.system('chmod 755 -R ' + fpm + '*')
                                    mainFile = fpm

                                aTime = aTime + 1
                                id2Time = aTime
                                if str(id2ProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                    fName = id2Time
                                    fRaw = id2Proof['body']
                                    fp = self.fu.tmpPath
                                    if not os.path.exists(fp):
                                        Log.i('DRV-Profile', 'Creating Directories')
                                        os.system('mkdir -p ' + fp)
                                    fpm = fp + '/' + str(fName) + id2ProofType
                                    fh = open(fpm, 'wb')
                                    fh.write(fRaw)
                                    fh.close()
                                    img_tag.append([id2Time,id2ProofType])

                                    mainFile = ''
                                    filepath.append(fpm)
                                    os.system('chmod 755 -R ' + fpm + '*')
                                    mainFile = fpm

                                liveProofTime = []
                                liveProofType = []
                                livetime = aTime
                                for y in liveProof:
                                    livetime = livetime + 1
                                    fName = livetime
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



                                firstName = j['firstName']
                                if firstName == None or firstName == '':
                                    code = 4755
                                    status = False
                                    message = "First Name cannot be empty"
                                    raise Exception
                                code,message = Validate.i(
                                            firstName,
                                            'First Name',
                                            #notEmpty = True,
                                            maxLength = 50,
                                            #noSpecial = True,
                                            #noNumber = True
                                        )

                                if code != 4100:
                                    raise Exception

                                lastName = j['lastName']
                                if lastName == None or lastName == '':
                                    code = 4755
                                    status = False
                                    message = "Last Name cannot be empty"
                                    raise Exception
                                code,message = Validate.i(
                                            lastName,
                                            'Last Name',
                                            #notEmpty = True,
                                            maxLength = 50,
                                            #noSpecial = True,
                                            #noNumber = True
                                        )

                                if code != 4100:
                                    raise Exception

                                address = j['address']
                                if address == None or address == '':
                                    code = 4755
                                    status = False
                                    message = "Address cannot be empty"
                                    raise Exception
                                code,message = Validate.i(
                                            address,
                                            'Address',
                                            notEmpty = True,
                                            maxLength = 1000,
                                        )

                                if code != 4100:
                                    raise Exception

                                idNumber = j['idNumber']
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
                                dateOfBirth = j['dob']
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
                                gender = j['gender']
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

                                # TODO: primary tourist is disabled

                                '''
                                bookingPriFindQ = self.touristBook.find(
                                                    {
                                                        '_id':bookingId,
                                                        'touristId':primaryTouristId
                                                    }
                                                )
                                bookingPriFind = []
                                async for i in bookingPriFindQ:
                                    bookingPriFind.append(i)
                                if not len(bookingPriFind[0]['touristDetails']):
                                    primary = True
                                else:
                                    primary = False
                                '''
                                primary = False

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
                                                        'profileId': primaryTouristId,
                                                        'entityId':self.entityId,
                                                        'subTouristDetails.idNumber':idNumber
                                                    }
                                                )
                                subTouristFind = []
                                async for i in subTouristFindQ:
                                    subTouristFind.append(i)
                                subkycInsert = await self.subTourist.insert_one(
                                            {
                                                'faceProof':[
                                                                {
                                                                    'time':liveProofTime[3],
                                                                    'mimeType':liveProofType[3]
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
                                                'profileId':primaryTouristId,
                                                'entityId':self.entityId,
                                                'verified':True,
                                                'disabled':False,
                                                'primary':primary,
                                                'submitRequest':[0,1],
                                                'subTouristDetails':subTouristDetails
                                            }
                                    )
                                subkycId = subkycInsert.inserted_id
                                insSubKyc.append(str(subkycId))
                                #bookingUpdate = await self.touristBook.update_one(
                                #        {
                                #            '_id':bookingId,
                                #            'touristId':primaryTouristId
                                #        },
                                #        {
                                #        "$push":{
                                touristDetails.append(
                                                                {
                                                                            'id':str(subkycId),
                                                                            'note' : [ ],
                                                                            'time': j['time'],
                                                                            'faceProof':[
                                                                                            {
                                                                                                'time':liveProofTime[3],
                                                                                                'mimeType':liveProofType[3]
                                                                                            }
                                                                                        ],
                                                                            'primary' : primary,
                                                                            'liveProof':[
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
                                                                }
                                    )
                                #        "$inc":{
                                #                    'touristCount' : 1,
                                #                    'liveCheckOutCount':1
                                #               },
                                #        }

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

                            if not len(alBookingQ):
                                bookingId = await self.touristBook.insert_one(
                                            {
                                                'disabled':False,
                                                'ticketId':ticketId,
                                                'entityId':self.entityId,
                                                'serviceAccountId':serviceAccountId,
                                                'primaryTouristInfo':accountData,
                                                'touristId':primaryTouristId,
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
                                                'touristCount' : len(touristDetails),
                                                'liveCheckInCount': len(touristDetails),
                                                'liveCheckOutCount': len(touristDetails),
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
                                                                    'startTime':checkinTime,
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
                                                "bookType":2
                                            }
                                        )
                                bookingId = bookingId.inserted_id
                            else:
                                bookingId = alBookingQ[0]['_id']
                                Log.i('Booking Exists', len(alBookingQ))

                            res = {
                                    'bookingId':str(bookingId),
                                    'time':checkinTime,
                                    'subTouristKyc': insSubKyc
                                }
                            result.append(res)
                            code = 2000
                            status = True
                            message = "Booking has been submitted."
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

