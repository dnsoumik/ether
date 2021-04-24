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
class MtimeProfileHandler(tornado.web.RequestHandler, MongoMixin):

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
                Log.i('PID', self.profileId)
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
                    self.apiId = app[0]['apiId']
                    Log.i(self.apiId)
                    if self.apiId in [ 402020, 402021, 402022, 402023]: # TODO: till here
                        organization = []
                        pAccountQ = self.account.find(
                                    {
                                        '_id': profile[0]['accountId']
                                    },
                                    limit=1
                                )
                        pAccount = []
                        async for i in pAccountQ:
                            pAccount.append(i)
                        if self.apiId == 402020:
                            touCountQ = self.subTourist.find(
                                {
                                    'profileId':self.profileId,
                                    'disabled':False
                                }
                            )
                            touCount = []
                            async for i in touCountQ:
                                touCount.append(i)
                            touCount = len(touCount)

                            passCountQ = self.touristPassV2.find(
                                {
                                    'profileId': self.profileId,
                                    #'$where': 'this.stage == 1'
                                }
                            )
                            passCount = []
                            async for i in passCountQ:
                                passCount.append(i)
                            passCount = len(passCount)
                        elif self.apiId == 402021:
                            #if profile[0].get('organization') == list and len(profile[0].get('organization')) > 0:
                            if profile[0].get('organization'):
                                for res in profile[0]['organization']:
                                    b = bytes(str(res['serviceAccountId']), 'utf-8')
                                    b = FN_ENCRYPT(b)
                                    serviceAccountKey = b.decode('utf-8')
                                    r = {
                                            'serviceAccountKey':serviceAccountKey,
                                            'role':res['role'],
                                            'name':'',
                                            'serviceType':res.get('serviceType')
                                        }
                                    if res.get('serviceType') == 1 or True:
                                        serviceFindQ = self.serviceAccount.find(
                                                        {
                                                            'profileId':res.get('serviceAccountId'),
                                                            'serviceType':1
                                                        },
                                                        {
                                                            '_id':0,
                                                            'propertyInfo':1
                                                        }
                                                    )
                                        serviceFind = []
                                        async for i in serviceFindQ:
                                            serviceFind.append(i)
                                        if len(serviceFind):
                                            r['name'] = serviceFind[0]['propertyInfo'][0]['propertyName']
                                    '''
                                    if res.get('serviceType') == 6:
                                        serviceFind = yield self.serviceAccount.find(
                                                        {
                                                            'profileId':res.get('serviceAccountId'),
                                                            'serviceType':1
                                                        },
                                                        {
                                                            '_id':0,
                                                            'basicInfo':1
                                                        }
                                                    )
                                        if len(serviceFind):
                                            r['name'] = serviceFind[0]['basicInfo'][0]['touristSpotName']
                                    '''

                                    organization.append(r)
                            else:
                                r = {
                                            'serviceAccountKey':FN_ENCRYPT(str(self.profileId)),
                                            'role':0,
                                            'name':'',
                                            'serviceType':0
                                    }
                                serviceFindQ = self.serviceAccount.find(
                                                {
                                                    'profileId':self.profileId,
                                                    'serviceType':1
                                                },
                                                {
                                                    '_id':0,
                                                    'propertyInfo':1,
                                                    'serviceType':1
                                                }
                                            )
                                serviceFind = []
                                async for i in serviceFindQ:
                                    serviceFind.append(i)
                                if len(serviceFind):
                                    r['name'] = serviceFind[0]['propertyInfo'][0]['propertyName']
                                    r['serviceType'] = serviceFind[0]['serviceType']
                                else:
                                    checkIndex = 0
                                    serviceTypes = [2,3,4,5,6,8]
                                    for j in serviceTypes:
                                        serviceFindQ = self.serviceAccount.find(
                                                {
                                                    'profileId':self.profileId,
                                                    'serviceType':j
                                                }
                                            )
                                        serviceFind = []
                                        async for i in serviceFindQ:
                                            serviceFind.append(i)
                                        if len(serviceFind):
                                            try:
                                                if checkIndex == 0:
                                                    r['serviceType'] = serviceFind[0]['serviceType']
                                                    checkIndex = checkIndex + 1
                                                    if r['serviceType'] in [2,4,5]:
                                                        r['name'] = serviceFind[0]['contactInfo'][0]['propertyName']
                                                    elif r['serviceType'] == 3:
                                                        r['name'] == serviceFind[0]['basicInfo'][0]['organizationName']
                                                    elif r['serviceType'] in [6,8]:
                                                        r['name'] = serviceFind[0]['basicInfo'][0]['touristSpotName']
                                                    checkIndex = checkIndex + 1
                                            except:
                                                Log.i("Organization Check")
                            organization.append(r)

                        if len(pAccount):
                            v = {}
                            if self.apiId == 402020:
                                profilePic = {
                                                'link': self.fu.serverUrl + '/uploads/' + 'placeholder_person.png'
                                              }
                                if pAccount[0].get('image') == None or profile[0].get('image') == []:
                                    primaryFindQ = self.subTourist.find(
                                                                        {
                                                                            'profileId':self.profileId,
                                                                            'primary':True
                                                                        }
                                                                    )
                                    primaryFind = []
                                    async for i in primaryFindQ:
                                        primaryFind.append(i)
                                    if len(primaryFind):
                                        if len(primaryFind[0]['faceProof']):
                                            for docx in primaryFind[0]['faceProof']:
                                                profilePic = {
                                                                'link': self.fu.serverUrl + '/uploads/' \
                                                                + str(self.entityId) + '/tourist_kyc/' \
                                                                + 'subtourist/' + str(res['_id']) \
                                                                + '/' + str(docx['time']) + docx['mimeType']
                                                            }
                                else:
                                    try:
                                        profilePic = {
                                                            'link': self.fu.serverUrl + '/uploads/' \
                                                            + str(self.entityId) + '/profile_pictures/' \
                                                            + str(self.accountId) \
                                                            + '/' + str(pAccount[0]['image'][0]['time']) + pAccount[0]['image'][0]['mimeType']
                                                    }
                                    except:
                                        Log.i('Failure in capturing profile pic')
                                v['subtouristCount'] = touCount
                                v['passCount'] = passCount
                                v['image'] = profilePic
                            elif self.apiId == 402021:
                                v['organization'] = organization

                            v['closed'] = profile[0]['closed']
                            v['locked'] = profile[0]['locked']
                            v['active'] = profile[0]['active']
                            v['id'] = str(profile[0].get('_id'))
                            v['firstName'] = pAccount[0].get('firstName')
                            v['lastName'] = pAccount[0].get('lastName')
                            v['contact'] = pAccount[0].get('contact')

                            # Adding Unread Message Count
                            if profile[0].get('unreadCount'):
                                v['unreadCount'] = int(profile[0]['unreadCount'])
                            else:
                                v['unreadCount'] = 0

                            #v['time'] = profile[0]['time']
                            pServiceAccountQ = self.serviceAccount.find(
                                    {
                                            'profileId': profile[0]['_id'],
                                            'entityId': self.entityId
                                    },
                                    limit=1
                                )
                            pServiceAccount = []
                            async for i in pServiceAccountQ:
                                pServiceAccount.append(i)
                            # TODO: need to verify
                            '''
                            if len(pServiceAccount):
                                v['firstName'] = pServiceAccount[0].get('firstName')
                                v['lastName'] = pServiceAccount[0].get('lastName')
                            '''
                            fpu = self.fu.uploads + str(self.entityId) + '/profile/' + str(v['id']) + '/profile.png'
                            v['profilePicture'] = fpu.replace(self.fu.uploads, self.fu.uploadsPath)
                            result.append(v)
                            status = True
                            code = 2000
                        else:
                            code = 3002
                            message = 'No Account Found.'
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

