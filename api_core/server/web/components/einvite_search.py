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
from baseconvert import base
from ..lib.lib import *
from datetime import timezone
from datetime import date
import datetime


@xenSecureV1
class EinviteSearchHandler(tornado.web.RequestHandler,
        MongoMixin):

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

    serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][0]['name']
                ]
    touristKyc = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][16]['name']
                ]
    subTourist = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][17]['name']
                ]
    touristPassV2 = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][38]['name']
                ]
    touristPass = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][20]['name']
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



    async def get(self):

        status = False
        code = 4000
        result = []
        msgquery = []
        message = ''
        passCount = 0


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
                    Log.i('api-ID',self.apiId)
                    if app[0]['apiId'] in [ 402020, 402022, 402021, 402023]: # TODO: till here
                        if self.apiId in [402022,402023]:
                            passId = None
                            try:
                                aRegex = str(self.request.arguments['regex'][0].decode())
                            except:
                                code = 9302
                                status = False
                                message = "Please submit valid search keyword"
                                raise Exception
                            res = []
                            resQ = self.touristPassV2.find({"passIdn":aRegex.upper()})
                            async for i in resQ:
                                res.append(i)
                            profiles = []
                            if aRegex.isnumeric():
                                if len(aRegex) != 10:
                                    code = 2090
                                    status = False
                                    message = "Please enter valid 10-digit phone number"
                                    raise Exception
                                numCheck = int(910000000000 + int(aRegex))
                                accFind = await self.account.find_one({"contact.0.value":numCheck})
                                if accFind:
                                    proFind = await self.profile.find_one({"accountId":accFind['_id']})
                                    if proFind:
                                        profiles.append(proFind['_id'])
                            else:
                                accFindQ = self.account.find(
                                        {
                                            '$or': [
                                                {
                                                    "firstName": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                },
                                                {
                                                    "lastName": {
                                                        '$regex': aRegex,
                                                        '$options': 'i'
                                                    }
                                                }
                                            ]
                                        }
                                    )
                                accFind = []
                                async for i in accFindQ:
                                    accFind.append(i['_id'])
                                if len(accFind):
                                    proFindQ = self.profile.find(
                                                    {
                                                        'accountId':{'$in':accFind}
                                                    }
                                                )
                                    async for i in proFindQ:
                                        profiles.append(i['_id'])
                            try:
                                limit = int(self.get_arguments('limit')[0])
                                skip = int(self.get_arguments('skip')[0])
                                f_state = True
                            except:
                                f_state = False
                            if f_state == True:
                                resQ = self.touristPassV2.find({"profileId":{'$in':profiles}},limit=limit,skip=skip).sort('_id',-1)
                            else:
                                resQ = self.touristPassV2.find({"profileId":{'$in':profiles}})
                            async for i in resQ:
                                res.append(i)
                            passCount = await self.touristPassV2.count_documents({"profileId":{'$in':profiles}})
                            if len(res):
                                passCount = len(res)
                                for passInfo in res:
                                    v = {
                                            '_id':str(passInfo['_id']),
                                            'touristProfileId':str(passInfo['profileId']),
                                            'time':passInfo['time'],
                                            'modifiedTime':passInfo['modifiedTime'],
                                            'activity':passInfo['activity'],
                                            'itineraryInfo':passInfo['itineraryInfo'],
                                            'passIdn':passInfo.get('passIdn'),
                                            'touristMem':[]
                                        }
                                    if passId != None:
                                        for mem in passInfo['touristMem']:
                                            touDetailsQ = self.subTourist.find(
                                                        {
                                                            '_id':ObjectId(mem)
                                                        },
                                                        {
                                                            '_id':1,
                                                            'subTouristDetails':1,
                                                            'faceProof':1,
                                                            'documents':1
                                                        }
                                                    )
                                            touDetails = []
                                            async for i in touDetailsQ:
                                                touDetails.append(i)
                                            for tou in touDetails:
                                                acc = {
                                                        'id':str(tou['_id']),
                                                        'firstName':tou['subTouristDetails'][0]['firstName'],
                                                        'lastName':tou['subTouristDetails'][0]['lastName'],
                                                        'address':tou['subTouristDetails'][0]['address'],
                                                        'documents':tou['documents'],
                                                        'faceProof':tou['faceProof']
                                                     }
                                                for docx in tou['documents']:
                                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                       + str(self.entityId) + '/tourist_kyc/' \
                                                       + 'subtourist/' + str(tou['_id']) \
                                                       + '/' + str(docx['time']) + docx['mimeType']
                                                for docx in tou['faceProof']:
                                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                       + str(self.entityId) + '/tourist_kyc/' \
                                                       + 'subtourist/' + str(tou['_id']) \
                                                       + '/' + str(docx['time']) + docx['mimeType']
                                            if len(touDetails):
                                                v['touristMem'].append(acc)
                                    else:
                                        v['touristMem'] = passInfo['touristMem']
                                    proFindQ = self.profile.find(
                                                        {
                                                            '_id':passInfo['profileId']
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

                                        if len(accFind):
                                            touristDetails = []
                                            x = {
                                                'firstName':accFind[0]['firstName'],
                                                'lastName':accFind[0]['lastName'],
                                                'contact':accFind[0]['contact']
                                            }
                                            touristDetails.append(x)
                                            v['touristDetails'] = touristDetails
                                        else:
                                            v['touristDetails'] = []
                                    else:
                                        v['touristDetails'] = []
                                    result.append(v)
                                result.reverse()
                                code = 2000
                                status = True
                                message = ""
                            else:
                                code = 4650
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
                    'message': message,
                    'filterData':msgquery
                }
        Log.d('RSP', response)
        try:
            response['count'] = passCount
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
                if len(app):
                    self.apiId = app[0]['apiId']
                    if self.apiId in [ 402020, 402022, 402021]:
                        if self.apiId == 402020:

                            passDate = timeNow()

                            touMem = self.request.arguments.get('touristMembers')
                            if not len(touMem):
                                code = 4760
                                status = False
                                message = "No Tourist Added"
                                raise Exception

                            itineraryInfo = self.request.arguments.get('itineraryInfo')
                            if itineraryInfo == None:
                                code = 7392
                                status = False
                                message = "No Itinerary Info added"
                                raise Exception
                            if not len(itineraryInfo):
                                code = 4760
                                status = False
                                message = "No Itinerary Info added"
                                raise Exception

                            if type(itineraryInfo) != list:
                                code = 8922
                                status = False
                                message = "Invalid Argument - ['itineraryInfo']"
                                raise Exception

                            iD = 1
                            count = 0
                            itinerary = []
                            dayCheckIndex = 0
                            dayLimit = 0
                            accDocumentProof = None
                            #for i in itineraryInfo:
                            for k,i in enumerate(itineraryInfo):
                                #i = v
                                j = {}
                                try:
                                    startDate = int(i['startDate'])
                                except:
                                    code = 8392
                                    status = False
                                    message = "Invalid Argument - Itinerary Start Date"
                                    raise Exception
                                j['startDate'] = i['startDate']

                                try:
                                    noOfDays = int(i['noOfDays'])
                                except:
                                    code = 8392
                                    status = False
                                    message = "Invalid Argument - Number of Days"
                                    raise Exception
                                j['noOfDays'] = i['noOfDays']
                                dayLimit = dayLimit + noOfDays
                                if dayCheckIndex == 0:
                                    firstDayLimit = dayLimit

                                if noOfDays == 0:
                                    code = 3728
                                    status = False
                                    message = "No of days cannot be zero"
                                    raise Exception
                                if i['placeName'] == None or i['placeName'] == "":
                                    code = 7932
                                    status = False
                                    message = "Please enter the place name in all Itinerary"
                                    raise Exception
                                j['placeName'] = i['placeName']

                                #If checking from postman
                                '''
                                if count == 0:
                                    startDate = int(startDate/1000000) - timeOffsetIST
                                else:
                                    startDate = int(startDate/1000000)
                                '''
                                startDate = int(startDate/1000000) + 19800
                                st = datetime.datetime.fromtimestamp(startDate).strftime('%Y-%m-%d')
                                Log.i('TIME',st)
                                dateList = list(st.split ("-"))
                                dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                                startDate = int(timestamp * 1000000)
                                if count == 0:
                                    passDateCheck = int(passDate/1000000)
                                    st = datetime.datetime.fromtimestamp(passDateCheck).strftime('%Y-%m-%d')
                                    dateList = list(st.split ("-"))
                                    dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                                    passDateCheck = int(timestamp * 1000000)


                                    if startDate < passDateCheck:
                                        code = 8322
                                        status = False
                                        message = "Set Date lesser than current date time"
                                        raise Exception
                                    count = count + 1
                                else:
                                    Log.i('skpped')
                                    # TODO: for now
                                    #if startDate != endDate and startDate != nextStartDate:
                                    #    code = 9302
                                    #    status = False
                                    #    message = "Invalid dates set in the Itinerary"
                                    #    raise Exception

                                endDate = startDate + (((noOfDays) * 24 * 3600) * 1000000)
                                nextStartDate = startDate + ((noOfDays) * 24 * 3600 * 1000000)
                                i['endDate'] = endDate
                                i['startDate'] = startDate
                                j['startDate'] = i['startDate']
                                j['endDate'] = i['endDate']
                                '''
                                if not len(i['transport']):
                                    code = 9302
                                    status = False
                                    message = "Please fill the Transport Information in the Itinerary"
                                    raise Exception
                                '''
                                print("****************")
                                print(i['accommodation'])
                                print("****************")
                                if dayCheckIndex == 0:
                                    if not len(i['accommodation']):
                                        code = 9302
                                        status = False
                                        message = "Please declare your accommodation for the first two nights atleast."
                                        raise Exception
                                else:
                                    if firstDayLimit <= 1:
                                        firstDayLimit = firstDayLimit + 1
                                        if not len(i['accommodation']):
                                            code = 9302
                                            status = False
                                            message = "Please declare your accommodation for the first two nights atleast."
                                            raise Exception

                                j['accommodation'] = i['accommodation']
                                if len(j['accommodation']):
                                    for res in j['accommodation']:
                                        if res['type'] == 1:
                                            res['bookingId'] = ""
                                            res['name'] = ""
                                            res['documents'] = []
                                            res['startDate'] = 0
                                            res['endDate'] = 0
                                            if res['phoneNumber'] == None or res['phoneNumber'] == "" \
                                                or res['phoneNumber'] == 0:
                                                code = 9302
                                                status = False
                                                message = "Please enter valid phone number"
                                                raise Exception
                                            if res['address'] == None or res['address'] == "" or len(res['address']) < 5\
                                                or len(res['address']) > 300:
                                                code = 9303
                                                status = False
                                                message = "Please enter valid complete address"
                                                raise Exception



                                        elif res['type'] == 2:
                                            res['phoneNumber'] = 0
                                            res['address'] = ""
                                            res['documents'] = []
                                            res['startDate'] = 0
                                            res['endDate'] = 0
                                            try:
                                                bookingId = ObjectId(res['bookingId'])
                                            except:
                                                bookingId = None
                                            if bookingId == None:
                                                code = 3920
                                                status = False
                                                message = "Invalid Booking ID"
                                                raise Exception
                                            bookingFindQ = self.touristBook.find(
                                                        {
                                                            '_id':bookingId,
                                                            'touristId':self.profileId
                                                        }
                                                    )
                                            bookingFind = []
                                            async for i in bookingFindQ:
                                                bookingFind.append(i)

                                            if not len(bookingFind):
                                                code = 9302
                                                status = False
                                                message = "Booking Not Found"
                                                raise Exception

                                            serAccFindQ = self.serviceAccount.find(
                                                        {
                                                            '_id':bookingFind[0]['serviceAccountId'],
                                                            'serviceType':1
                                                        }
                                                    )
                                            serAccFind = []
                                            async for k in serAccFindQ:
                                                serAccFind.append(k)

                                            if not len(serAccFind):
                                                res['name'] = "Accomodation Name not Available"
                                            else:
                                                res['name'] = serAccFind[0]['propertyInfo'][0]['propertyName']

                                        elif res['type'] == 3:
                                            res['address'] = ""
                                            res['bookingId'] = ""
                                            res['documents'] = []
                                            try:
                                                res['name']
                                            except:
                                                res['name'] = ""
                                            res['phoneNumber'] = 0
                                            try:
                                                startD = int(res['startDate'])
                                            except:
                                                code = 7322
                                                status = False
                                                message = "Please set proper start Date"
                                                raise Exception

                                            try:
                                                endD = int(res['endDate'])
                                            except:
                                                code = 7322
                                                status = False
                                                message = "Please set proper end Date"
                                                raise Exception
                                            try:
                                                accDocumentProof = self.request.files['accDocument_'+ str(k)][0]
                                                accDocumentProofType = accDocumentProof['content_type']
                                                accDocumentProofType = mimetypes.guess_extension(
                                                accDocumentProofType,
                                                strict=True
                                                )
                                                if accDocumentProofType == None:
                                                    accDocumentProofType = pathlib.Path(accDocumentProof['filename']).suffix
                                            except Exception as e:
                                                accDocumentProof = None

                                            if accDocumentProof != None:
                                                filepath = []
                                                aTime = aTime + 1
                                                accDocumentTime = aTime
                                                if str(accDocumentProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                                    fName = accDocumentTime
                                                    fRaw = accDocumentProof['body']
                                                    fp = self.fu.tmpPath
                                                    if not os.path.exists(fp):
                                                        Log.i('DRV-Profile', 'Creating Directories')
                                                    os.system('mkdir -p ' + fp)
                                                    fpm = fp + '/' + str(fName) + accDocumentProofType
                                                    fh = open(fpm, 'wb')
                                                    fh.write(fRaw)
                                                    fh.close()
                                                    filepath.append(fpm)
                                                    os.system('chmod 755 -R ' + fpm + '*')
                                                else:
                                                    code = 3279
                                                    status = False
                                                    message = "File extension not supported"
                                                    raise Exception
                                                res['documents'] = [
                                                                {
                                                                    'time':accDocumentTime,
                                                                    'mimeType':accDocumentProofType
                                                                }
                                                            ]
                                            checkDate = timeNow()

                                            #Not confirmed for now
                                            '''
                                            if int(res['startDate']) < checkDate or int(res['endDate']) < checkDate:
                                                code = 8392
                                                status = False
                                                message = "Invalid Booking Dates"
                                                raise Exception
                                            '''

                                try:
                                    j['transport'] = i['transport']
                                    for res in j['transport']:
                                        if res['type'] == 1:
                                            if res['regNum'] == None or res['regNum'] == ""\
                                                    or res['regNum'] == 0:
                                                code = 8492
                                                status = False
                                                message = "Please enter valid vehicle registration number"
                                                raise Exception
                                except:
                                    j['transport'] = []


                                j['id'] = iD
                                Log.i('index', j)
                                i['noOfDays'] = int(j['noOfDays'])
                                itinerary.append(j)
                                iD = iD + 1
                                dayCheckIndex = dayCheckIndex + 1
                            if dayLimit < 2:
                                code = 9032
                                status = False
                                message = "Itinerary Information of atleast 2 nights must be submitted"
                                raise Exception


                            tmpPassId = base(passDate, 10, 36, string=True)
                            passId = await self.touristPassV2.insert_one(
                                    {
                                            'activity':[
                                                            {
                                                                'id':0,
                                                                'time':passDate
                                                            }
                                                        ],
                                            'profileId':self.profileId,
                                            'accountId':self.accountId,
                                            'entityId':self.entityId,
                                            'touristMem':touMem,
                                            'createdBy':[
                                                            {
                                                                'profileId':self.profileId,
                                                                'serviceType':0
                                                            }
                                                        ],
                                            'time':passDate,
                                            'modifiedTime':passDate,
                                            'itineraryInfo':itineraryInfo,
                                            'passIdn':tmpPassId
                                    }
                                )
                            if accDocumentProof != None:
                                passId = passId.inserted_id
                                uPath = self.fu.uploads + '/' + str(self.entityId)
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + '/itinerary/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + str(self.profileId) + '/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + str(passId) + '/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                for i in filepath:
                                    os.system('mv ' + i + ' ' + uPath)

                                Log.d(uPath)

                                os.system('chmod 755 -R ' + uPath + '*')
                            code = 2000
                            status = True
                            message = "Tourist Pass has been added."
                        elif self.apiId == 402021:
                            '''
                            serAccFindQ = self.serviceAccount.find(
                                                {
                                                    'profileId':self.profileId,
                                                    'serviceType':3,
                                                    'verified':True,
                                                }
                                            )
                            serAccFind = []
                            async for i in serAccFindQ:
                                serAccFind.append(i)
                            if not len(serAccFind):
                                code = 9819
                                status = False
                                message = "No Active Service Account Found for Tour Operator"
                                raise Exception
                            '''
                            passDate = timeNow()

                            try:
                                profileId = ObjectId(self.request.arguments.get('id'))
                            except:
                                code =9939
                                status = False
                                message = "Invalid Tourist Profile Id"
                                raise Exception

                            appFindQ = self.applications.find(
                                            {
                                                'apiId':402020
                                            }
                                        )
                            appFind = []
                            async for i in appFindQ:
                                appFind.append(i)

                            if not len(appFind):
                                code = 8921
                                status = False
                                message = "Internal Error in Finding Application. Please contact support"
                                raise Exception


                            proFindQ = self.profile.find(
                                            {
                                                '_id':profileId,
                                                'entityId':self.entityId,
                                                'applicationId':appFind[0]['_id']
                                            }
                                        )
                            proFind = []
                            async for i in proFindQ:
                                proFind.append(i)

                            if not len(proFind):
                                code = 8912
                                status = False
                                message = "User Profile Not Found"
                                raise Exception



                            accFindQ = self.account.find(
                                            {
                                                '_id':proFind[0]['accountId']
                                            }
                                        )
                            accFind= []
                            async for i in accFindQ:
                                accFind.append(i)

                            if not len(accFind):
                                code = 3102
                                status = False
                                message = "User Account Not Found"
                                raise Exception

                            accountId = accFind[0]['_id']

                            touMem = self.request.arguments.get('touristMembers')
                            if not len(touMem):
                                code = 4760
                                status = False
                                message = "No Tourist Added"
                                raise Exception

                            itineraryInfo = self.request.arguments.get('itineraryInfo')
                            if itineraryInfo == None:
                                code = 7392
                                status = False
                                message = "No Itinerary Info added"
                                raise Exception
                            if not len(itineraryInfo):
                                code = 4760
                                status = False
                                message = "No Itinerary Info added"
                                raise Exception

                            if type(itineraryInfo) != list:
                                code = 8922
                                status = False
                                message = "Invalid Argument - ['itineraryInfo']"
                                raise Exception

                            iD = 1
                            count = 0
                            itinerary = []
                            dayCheckIndex = 0
                            dayLimit = 0
                            accDocumentProof = None
                            for k,i in enumerate(itineraryInfo):
                            #for i in itineraryInfo:
                                #i = v
                                j = {}
                                try:
                                    startDate = int(i['startDate'])
                                except:
                                    code = 8392
                                    status = False
                                    message = "Invalid Argument - Itinerary Start Date"
                                    raise Exception
                                j['startDate'] = i['startDate']

                                try:
                                    noOfDays = int(i['noOfDays'])
                                except:
                                    code = 8392
                                    status = False
                                    message = "Invalid Argument - Number of Days"
                                    raise Exception

                                j['noOfDays'] = i['noOfDays']
                                dayLimit = dayLimit + noOfDays
                                if dayCheckIndex == 0:
                                    firstDayLimit = dayLimit

                                if noOfDays == 0:
                                    code = 3728
                                    status = False
                                    message = "No of days cannot be zero"
                                    raise Exception
                                if i['placeName'] == None or i['placeName'] == "":
                                    code = 7932
                                    status = False
                                    message = "Please enter the place name in all Itinerary"
                                    raise Exception
                                j['placeName'] = i['placeName']

                                #If checking from postman
                                '''
                                if count == 0:
                                    startDate = int(startDate/1000000) - timeOffsetIST
                                else:
                                    startDate = int(startDate/1000000)
                                '''
                                Log.i(startDate)
                                startDate = int(startDate/1000000) + 19800
                                Log.i(startDate)
                                st = datetime.datetime.fromtimestamp(startDate).strftime('%Y-%m-%d')
                                Log.i('TIME',st)
                                dateList = list(st.split ("-"))
                                dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                                startDate = int(timestamp * 1000000)
                                if count == 0:
                                    passDateCheck = int(passDate/1000000)
                                    st = datetime.datetime.fromtimestamp(passDateCheck).strftime('%Y-%m-%d')
                                    dateList = list(st.split ("-"))
                                    dt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), 0, 0, 0)
                                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                                    passDateCheck = int(timestamp * 1000000)


                                    if startDate < passDateCheck:
                                        code = 8322
                                        status = False
                                        message = "Set Date lesser than current date time"
                                        raise Exception
                                    count = count + 1
                                else:
                                    Log.i('skpped')
                                Log.i(startDate)
                                    # TODO: for now
                                    #if startDate != endDate and startDate != nextStartDate:
                                    #    code = 9302
                                    #    status = False
                                    #    message = "Invalid dates set in the Itinerary"
                                    #    raise Exception

                                endDate = startDate + (((noOfDays) * 24 * 3600) * 1000000)
                                nextStartDate = startDate + ((noOfDays) * 24 * 3600 * 1000000)
                                i['endDate'] = endDate
                                i['startDate'] = startDate
                                j['startDate'] = i['startDate']
                                j['endDate'] = i['endDate']
                                '''
                                if not len(i['transport']):
                                    code = 9302
                                    status = False
                                    message = "Please fill the Transport Information in the Itinerary"
                                    raise Exception
                                '''
                                if dayCheckIndex == 0:
                                    if not len(i['accommodation']):
                                        code = 9302
                                        status = False
                                        message = "Please declare your accommodation for the first two nights atleast."
                                        raise Exception
                                else:
                                    if firstDayLimit <= 1:
                                        firstDayLimit = firstDayLimit + 1
                                        if not len(i['accommodation']):
                                            code = 9302
                                            status = False
                                            message = "Please declare your accommodation for the first two nights atleast."
                                            raise Exception
                                j['accommodation'] = i['accommodation']
                                if len(j['accommodation']):
                                    for res in j['accommodation']:
                                        if res['type'] == 1:
                                            res['bookingId'] = ""
                                            res['name'] = ""
                                            res['documents'] = []
                                            res['startDate'] = 0
                                            res['endDate'] = 0
                                            if res['phoneNumber'] == None or res['phoneNumber'] == "" \
                                                or res['phoneNumber'] == 0:
                                                code = 9302
                                                status = False
                                                message = "Please enter valid phone number"
                                                raise Exception
                                            try:
                                                if res['address'] == None or res['address'] == "" or len(res['address']) < 5\
                                                    or len(res['address']) > 300:
                                                        raise Exception
                                            except:
                                                code = 9303
                                                status = False
                                                message = "Please enter complete address if Own Accomodation(5-300 characters) is set"
                                                raise Exception



                                        elif res['type'] == 2:
                                            res['phoneNumber'] = 0
                                            res['address'] = ""
                                            res['documents'] = []
                                            res['startDate'] = 0
                                            res['endDate'] = 0
                                            #TODO check for booking entry within the date range
                                            try:
                                                bookingId = ObjectId(res['bookingId'])
                                            except:
                                                bookingId = None
                                            if bookingId == None:
                                                code = 3920
                                                status = False
                                                message = "Invalid Booking ID"
                                                raise Exception
                                            bookingFindQ = self.touristBook.find(
                                                        {
                                                            '_id':bookingId,
                                                            'touristId':profileId
                                                        }
                                                    )
                                            bookingFind = []
                                            async for i in bookingFindQ:
                                                bookingFind.append(i)

                                            if not len(bookingFind):
                                                code = 9302
                                                status = False
                                                message = "Booking Not Found"
                                                raise Exception

                                            serAccFindQ = self.serviceAccount.find(
                                                        {
                                                            '_id':bookingFind[0]['serviceAccountId'],
                                                            'serviceType':1
                                                        }
                                                    )
                                            serAccFind = []
                                            async for k in serAccFindQ:
                                                serAccFind.append(k)

                                            if not len(serAccFind):
                                                res['name'] = "Accomodation Name not Available"
                                            else:
                                                res['name'] = serAccFind[0]['propertyInfo'][0]['propertyName']

                                        elif res['type'] == 3:
                                            res['address'] = ""
                                            res['bookingId'] = ""
                                            res['documents'] = []
                                            try:
                                                hotelName = res['name']
                                            except:
                                                res['name'] = ""
                                                hotelName = None
                                            res['name'] = ""
                                            res['phoneNumber'] = 0
                                            try:
                                                startD = int(res['startDate'])
                                            except:
                                                code = 7322
                                                status = False
                                                message = "Please set proper start Date"
                                                raise Exception

                                            try:
                                                endD = int(res['endDate'])
                                            except:
                                                code = 7322
                                                status = False
                                                message = "Please set proper end Date"
                                                raise Exception
                                            try:
                                                accDocumentProof = self.request.files['accDocument_'+ str(k)][0]
                                                accDocumentProofType = accDocumentProof['content_type']
                                                accDocumentProofType = mimetypes.guess_extension(
                                                accDocumentProofType,
                                                strict=True
                                                )
                                                if accDocumentProofType == None:
                                                    accDocumentProofType = pathlib.Path(accDocumentProof['filename']).suffix
                                            except Exception as e:
                                                accDocumentProof = None

                                            if accDocumentProof != None:
                                                if hotelName == None:
                                                    code = 9032
                                                    status = False
                                                    message = "Please enter the name of the hotel or upload the receipt"
                                                    raise Exception
                                                filepath = []
                                                aTime = aTime + 1
                                                accDocumentTime = aTime
                                                if str(accDocumentProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                                    fName = accDocumentTime
                                                    fRaw = accDocumentProof['body']
                                                    fp = self.fu.tmpPath
                                                    if not os.path.exists(fp):
                                                        Log.i('DRV-Profile', 'Creating Directories')
                                                    os.system('mkdir -p ' + fp)
                                                    fpm = fp + '/' + str(fName) + accDocumentProofType
                                                    fh = open(fpm, 'wb')
                                                    fh.write(fRaw)
                                                    fh.close()
                                                    filepath.append(fpm)
                                                    os.system('chmod 755 -R ' + fpm + '*')
                                                else:
                                                    code = 3279
                                                    status = False
                                                    message = "File extension not supported"
                                                    raise Exception
                                                res['documents'] = [
                                                                {
                                                                    'time':accDocumentTime,
                                                                    'mimeType':accDocumentProofType
                                                                }
                                                            ]

                                            checkDate = timeNow()
                                            #Not confirmed for now
                                            '''
                                            if int(res['startDate']) < checkDate or int(res['endDate']) < checkDate:
                                                code = 8392
                                                status = False
                                                message = "Invalid Booking Dates"
                                                raise Exception
                                            '''
                                try:
                                    j['transport'] = i['transport']
                                    for res in j['transport']:
                                        if res['type'] == 1:
                                            if res['registrationNumber'] == None or res['registrationNumber'] == ""\
                                                    or res['registrationNumber'] == 0:
                                                code = 8492
                                                status = False
                                                message = "Please enter valid vehicle registration number"
                                                raise Exception
                                except:
                                    j['transport'] = []


                                j['id'] = iD
                                Log.i('index', j)
                                i['noOfDays'] = int(j['noOfDays'])
                                itinerary.append(j)
                                iD = iD + 1
                                dayCheckIndex = dayCheckIndex + 1

                            if dayLimit < 2:
                                code = 9032
                                status = False
                                message = "Itinerary Information of atleast 2 nights must be submitted"
                                raise Exception

                            tmpPassId = base(passDate, 10, 36, string=True)
                            passId = await self.touristPassV2.insert_one(
                                    {
                                            'activity':[
                                                            {
                                                                'id':0,
                                                                'time':passDate
                                                            }
                                                        ],
                                            'profileId':profileId,
                                            'accountId':accountId,
                                            'entityId':self.entityId,
                                            'touristMem':touMem,
                                            'createdBy':[
                                                            {
                                                                'profileId':self.profileId,
                                                                'serviceType':3
                                                            }
                                                        ],
                                            'time':passDate,
                                            'modifiedTime':passDate,
                                            'itineraryInfo':itineraryInfo,
                                            'passIdn':tmpPassId
                                    }
                                )
                            if accDocumentProof != None:
                                passId = passId.inserted_id
                                uPath = self.fu.uploads + '/' + str(self.entityId)
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + '/itinerary/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + str(profileId) + '/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + str(passId) + '/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                for i in filepath:
                                    os.system('mv ' + i + ' ' + uPath)

                                Log.d(uPath)
                                os.system('chmod 755 -R ' + uPath + '*')
                            code = 2000
                            status = True
                            message = "Tourist Pass has been added."
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

    async def delete(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            passId = str(self.request.arguments['id'][0].decode())
            try:
                passId = ObjectId(passId)
            except:
                raise Exception
        except:
            code = 4650
            status = False
            message = "Invalid PassId"

        try:
            # TODO: this need to be moved in a global class, from here
            profileQ = self.profile.find(
                            {
                                'closed': False,
                                'accountId': self.accountId,
                                'entityId': self.entityId,
                                'applicationId': self.applicationId
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
                    if app[0]['apiId'] == 402020:# TODO: till here
                        passUpdate = await self.touristPassV2.update_one(
                                {
                                    '_id':passId
                                },
                                {
                                '$push': {
                                            'activity': {
                                                            'id':4,
                                                            'time':timeNow()
                                                        }
                                        }
                                }
                        )
                        if passUpdate.modified_count != None:
                            code = 2000
                            status = True
                            message = "Pass has been cancelled"
                        else:
                            code = 4650
                            status = False
                            message = "Pass cancellation not successful"
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

