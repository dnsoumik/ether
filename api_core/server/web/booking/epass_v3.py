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
import datetime
from jinja2 import Template
import pdfkit
from datetime import date
import pyqrcode
import png
from pyqrcode import QRCode


@xenSecureV1
class McovidEpassV3Handler(tornado.web.RequestHandler,
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

    entity = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][5]['name']
                ]

    serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][0]['name']
                ]
    v3serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][3]['name']
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
                    if app[0]['apiId'] in [ 602020, 602022]: # TODO: till here
                        if self.apiId == 602020:
                            try:
                                serviceAccountId = self.request.arguments['id'][0].decode()
                            except:
                                code = 5749
                                status = False
                                message = "Missing Argument - ['id']"
                                raise Exception

                            try:
                                serviceAccountId = ObjectId(serviceAccountId)
                            except:
                                code = 5749
                                status = False
                                message = "Invalid Argument - ['id']"
                                raise Exception

                            serAccFindQ = self.v3serviceAccount.find(
                                            {
                                                '_id':serviceAccountId,
                                                'profileId':self.profileId,
                                                'entityId':self.entityId
                                            }
                                        )
                            serAccFind = []
                            async for i in serAccFindQ:
                                serAccFind.append(i)

                            if not len(serAccFind):
                                code = 8932
                                status = False
                                message = "Registration not found"
                                raise Exception

                            print(serAccFind[0]['status'])

                            if serAccFind[0]['status'] != 2:
                                code = 8932
                                status = False
                                message = "Not yet approved"
                                raise Exception

                            applicationDate = serAccFind[0]['time'] / 1000000
                            applicationDate = datetime.datetime.fromtimestamp(applicationDate).strftime('%d %B, %Y')

                            arrivalDate = serAccFind[0]['travelInfo'][0]['arrivalDate'] / 1000000
                            arrivalDate = datetime.datetime.fromtimestamp(arrivalDate).strftime('%d %B, %Y')

                            try:
                                if serAccFind[0]['symptomInfo'][0]['fever'] == True \
                                    or serAccFind[0]['symptomInfo'][0]['cough'] == True \
                                    or serAccFind[0]['symptomInfo'][0]['breathingDifficulties'] == True:
                                    symptoms = "Yes"
                                else:
                                    symptoms = "No"
                            except:
                                symptoms = "N/A"


                            originProof = " "
                            if serAccFind[0]['travelInfo'][0]['travelMode'].upper() == "ROAD":
                                originProof = "Other Documents"

                            filepath = []
                            htmlfile = './../mtime_schedule/epass_template_v3.html'
                            checkFile = os.path.exists(htmlfile)
                            if checkFile == False:
                                code = 8938
                                status = False
                                message = "Internal Error. Please contact Support"
                                raise Exception
                            filepath.append(htmlfile)
                            uPath = self.fu.uploads + '/' + str(self.entityId)
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)
                            uPath = uPath + '/' + str(self.profileId)
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)
                            uPath = uPath + '/serviceAccount/'
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)
                            uPath = uPath + '/' + str(serviceAccountId)
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)
                            for i in filepath:
                                os.system('cp ' + i + ' ' + uPath)

                            userHtmlfile = uPath + '/' + 'epass_template_v3.html'
                            passId = serAccFind[0]['passId']
                            qrFile = uPath + '/' + 'epass_qr.png'
                            # Generate QR code
                            url = pyqrcode.create(passId)
                            # Create and save the png file naming "myqr.png"
                            url.png(qrFile, scale = 6)

                            Log.i(userHtmlfile)
                            if os.path.exists(userHtmlfile):
                                with open(userHtmlfile,"r") as f:
                                    t = Template(f.read())
                                    vals = {
                                                'passId':passId,
                                                'applicationDate':applicationDate,
                                                'applicantName':serAccFind[0]['basicInfo'][0]['name'] \
                                                        + ' ' + serAccFind[0]['basicInfo'][0]['surName'],
                                                'applicantAddress':serAccFind[0]['placeOutInfo'][0]['address'],
                                                'country':serAccFind[0]['placeOutInfo'][0]['country'],
                                                'state':serAccFind[0]['placeOutInfo'][0]['state'],
                                                'gender':serAccFind[0]['basicInfo'][0]['gender'],
                                                'age':serAccFind[0]['basicInfo'][0]['age'],
                                                'mobileNumber':serAccFind[0]['basicInfo'][0]['mobileNumber'],
                                                'idProof':serAccFind[0]['basicInfo'][0]['idType'],
                                                #'visitProof':serAccFind[0]['basicInfo'][0]['supportDocType'],
                                                'originProof':originProof,
                                                'stayDaysNum':serAccFind[0]['basicInfo'][0]['stayDaysNum'],
                                                'travelMode':serAccFind[0]['travelInfo'][0]['travelMode'],
                                                'arrivalDate':arrivalDate,
                                                'entryPoint':serAccFind[0]['travelInfo'][0]['entryPoint'],
                                                'symptoms':symptoms,
                                                'qrCodeImage':'epass_qr.png'
                                            }
                                    with open(userHtmlfile,"w") as f:
                                        f.write(t.render(vals))
                                f.close()
                            pdfPath = uPath + '/' + 'ePass_v3.pdf'
                            try:
                                pdfkit.from_file(userHtmlfile,pdfPath)
                                Log.i('PDF CONVERSION SUCCESS FOR ePASS')
                            except:
                                code = 4589
                                status = False
                                message = "Internal Error. Please contact Support"
                                raise Exception
                            os.system('rm ' + userHtmlfile)
                            os.system('rm ' + qrFile)
                            v = {
                                    'fileLink': self.fu.serverUrl + '/uploads/' + str(self.entityId) + '/'\
                                            + str(self.profileId) + '/serviceAccount/' + str(serviceAccountId) + '/' + 'ePass_v3.pdf'
                                }
                            result.append(v)
                            code = 2000
                            status = True
                            message = "ePass PDF file"
                        elif self.apiId == 602022:
                            try:
                                serviceAccountId = self.request.arguments['id'][0].decode()
                            except:
                                code = 5749
                                status = False
                                message = "Missing Argument - ['id']"
                                raise Exception

                            try:
                                serviceAccountId = ObjectId(serviceAccountId)
                            except:
                                code = 5749
                                status = False
                                message = "Invalid Argument - ['id']"
                                raise Exception

                            serAccFindQ = self.v3serviceAccount.find(
                                            {
                                                '_id':serviceAccountId,
                                                'entityId':self.entityId
                                            }
                                        )
                            serAccFind = []
                            async for i in serAccFindQ:
                                serAccFind.append(i)

                            if not len(serAccFind):
                                code = 8932
                                status = False
                                message = "Registration not found"
                                raise Exception

                            if serAccFind[0]['status'] != 2:
                                code = 8932
                                status = False
                                message = "Not yet approved"
                                raise Exception

                            applicationDate = serAccFind[0]['time'] / 1000000
                            applicationDate = datetime.datetime.fromtimestamp(applicationDate).strftime('%d %B, %Y')

                            arrivalDate = serAccFind[0]['travelInfo'][0]['arrivalDate'] / 1000000
                            arrivalDate = datetime.datetime.fromtimestamp(arrivalDate).strftime('%d %B, %Y')

                            try:
                                if serAccFind[0]['symptomInfo'][0]['fever'] == True \
                                    or serAccFind[0]['symptomInfo'][0]['cough'] == True \
                                    or serAccFind[0]['symptomInfo'][0]['breathingDifficulties'] == True:
                                    symptoms = "Yes"
                                else:
                                    symptoms = "No"
                            except:
                                symptoms = "N/A"


                            originProof = " "
                            if serAccFind[0]['travelInfo'][0]['travelMode'].upper() == "ROAD":
                                originProof = "Other Documents"

                            filepath = []
                            htmlfile = './../mtime_schedule/epass_template_v3.html'
                            checkFile = os.path.exists(htmlfile)
                            if checkFile == False:
                                code = 8938
                                status = False
                                message = "Internal Error. Please contact Support"
                                raise Exception
                            filepath.append(htmlfile)
                            uPath = self.fu.uploads + '/' + str(self.entityId)
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)
                            uPath = uPath + '/' + str(serAccFind[0]['profileId'])
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)
                            uPath = uPath + '/serviceAccount/'
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)
                            uPath = uPath + '/' + str(serviceAccountId)
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)
                            for i in filepath:
                                os.system('cp ' + i + ' ' + uPath)

                            userHtmlfile = uPath + '/' + 'epass_template_v3.html'
                            passId = serAccFind[0]['passId']
                            qrFile = uPath + '/' + 'epass_qr.png'
                            # Generate QR code
                            url = pyqrcode.create(passId)
                            # Create and save the png file naming "myqr.png"
                            url.png(qrFile, scale = 6)

                            Log.i(userHtmlfile)
                            if os.path.exists(userHtmlfile):
                                with open(userHtmlfile,"r") as f:
                                    t = Template(f.read())
                                    vals = {
                                                'passId':passId,
                                                'applicationDate':applicationDate,
                                                'applicantName':serAccFind[0]['basicInfo'][0]['name'] \
                                                        + ' ' + serAccFind[0]['basicInfo'][0]['surName'],
                                                'applicantAddress':serAccFind[0]['placeOutInfo'][0]['address'],
                                                'country':serAccFind[0]['placeOutInfo'][0]['country'],
                                                'state':serAccFind[0]['placeOutInfo'][0]['state'],
                                                'gender':serAccFind[0]['basicInfo'][0]['gender'],
                                                'age':serAccFind[0]['basicInfo'][0]['age'],
                                                'mobileNumber':serAccFind[0]['basicInfo'][0]['mobileNumber'],
                                                'idProof':serAccFind[0]['basicInfo'][0]['idType'],
                                                #'visitProof':serAccFind[0]['basicInfo'][0]['supportDocType'],
                                                'originProof':originProof,
                                                'stayDaysNum':serAccFind[0]['basicInfo'][0]['stayDaysNum'],
                                                'travelMode':serAccFind[0]['travelInfo'][0]['travelMode'],
                                                'arrivalDate':arrivalDate,
                                                'entryPoint':serAccFind[0]['travelInfo'][0]['entryPoint'],
                                                'symptoms':symptoms,
                                                'qrCodeImage':'epass_qr.png'
                                            }
                                    with open(userHtmlfile,"w") as f:
                                        f.write(t.render(vals))
                                f.close()
                            pdfPath = uPath + '/' + 'ePass_v3.pdf'
                            try:
                                pdfkit.from_file(userHtmlfile,pdfPath)
                                Log.i('PDF CONVERSION SUCCESS FOR ePASS')
                            except:
                                code = 4589
                                status = False
                                message = "Internal Error. Please contact Support"
                                raise Exception
                            os.system('rm ' + userHtmlfile)
                            os.system('rm ' + qrFile)
                            v = {
                                    'fileLink': self.fu.serverUrl + '/uploads/' + str(self.entityId) + '/'\
                                        + str(serAccFind[0]['profileId']) + '/serviceAccount/' + str(serviceAccountId) + '/' + 'ePass_v3.pdf'
                                }
                            result.append(v)
                            code = 2000
                            status = True
                            message = "ePass PDF file"
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
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return

