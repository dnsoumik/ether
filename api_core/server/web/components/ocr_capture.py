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
import requests
import http.client
import datetime
import pathlib

@xenSecureV1
class MtimeOcrCaptureHandler(tornado.web.RequestHandler,
        MongoMixin):

    SUPPORTED_METHODS = ('POST', 'DELETE', 'OPTIONS')

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
            #Discussion to optimize
            # GET FILES FROM REQUEST BODY
            try:
                id1Proof = self.request.files['id1Proof'][0]
            except Exception as e:
                code = 4100
                message = 'ID-Front Image is missing'
                raise Exception

            try:
                id2Proof = self.request.files['id2Proof'][0]
            except:
                code = 4100
                message = 'ID-Back Image is missing'
                raise Exception


            try:
                idType = self.request.arguments['idType'][0].decode()
            except:
                code = 4855
                status = False
                message = "Missing Argument - [idType]"
                raise Exception

            if idType == 'Voter ID Card':
                idType = 'Voter Id Card'

            if idType == None or idType == '' or idType not in ['Aadhaar Card','Voter Id Card','Others','Other','Driving License', 'Passport','Others']:
                code = 4850
                status = False
                message = "Invalid idType"
                raise Exception

            filepath = []
            ocrData = {}
            ocrData['firstName'] = ''
            ocrData['lastName'] = ''
            ocrData['idNumber'] = ''
            ocrData['dateOfBirth'] = ''
            ocrData['address'] = ''
            ocrData['gender'] = ''
            ocrData['age'] = ''
            id1ProofType = id1Proof['content_type']
            id1ProofType = mimetypes.guess_extension(
                                    id1ProofType,
                                    strict=True
                        )
            if id1ProofType == None:
                id1ProofType = pathlib.Path(id1Proof['filename']).suffix
            if str(id1ProofType) in ['.jpeg', '.jpg', '.png', '.jpe']:
                fName = timeNow()
                fRaw = id1Proof['body']
                fp = self.fu.tmpPath
                if not os.path.exists(fp):
                    Log.i('DRV-Profile', 'Creating Directories')
                    os.system('mkdir -p ' + fp)
                fpm = fp + '/' + str(fName) + id1ProofType
                fh = open(fpm, 'wb')
                fh.write(fRaw)
                fh.close()
                mainFile = ''
                # Converting to PNG
                if str(id1ProofType) not in ['.png']:
                    id1ProofType = '.png'
                    fpx = fp + '/' + str(fName) + id1ProofType
                    filepath.append(fpx)
                    im = Image.open(fpm)
                    im.save(fpx, 'PNG')
                    os.system('rm ' + fpm)
                    os.system('chmod 755 -R ' + fp + '*')
                    mainFile = fpx
                else:
                    filepath.append(fpm)
                    os.system('chmod 755 -R ' + fp + '*')
                    mainFile = fpm


                if idType in ['Aadhaar Card','Voter Id Card']:
                    imgPath = mainFile
                    url = "http://localhost:2123/ocr"
                    data = {'imgPath': imgPath,'idType':idType}
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    res = requests.post(url, data=json.dumps(data), headers=headers)
                    data = res.text
                    try:
                        stat = json.loads(data)
                        if stat['status'] == True:
                            if 'front' in stat['result'][0]['side']:
                                ocrData['firstName'] = stat['result'][0]['firstName']
                                ocrData['lastName'] = stat['result'][0]['lastName']
                                ocrData['idNumber'] = stat['result'][0]['idNumber']
                                ocrData['dateOfBirth'] = stat['result'][0]['dateOfBirth']
                                ocrData['age'] = stat['result'][0]['age']
                                ocrData['gender'] = stat['result'][0]['gender'].lower()
                            else:
                                ocrData['address'] = stat['result'][0]['address']
                            Log.i('OCR CAPTURED:',ocrData)
                        else:
                            Log.i('OCR CAPTURE FAILURE')
                    except:
                        Log.i('Internal Error in OCR Request')
            else:
                message = 'Invalid File Type'
                code = 4011
                raise Exception

            if True:
                id2ProofType = id2Proof['content_type']
                id2ProofType = mimetypes.guess_extension(
                            id2ProofType,
                            strict=True
                    )
                if id2ProofType == None:
                    id2ProofType = pathlib.Path(id2Proof['filename']).suffix
                if str(id2ProofType) in ['.jpeg', '.jpg', '.png', '.jpe']:
                    fName = timeNow() + 1
                    fRaw = id2Proof['body']
                    fp = self.fu.tmpPath
                    if not os.path.exists(fp):
                        Log.i('DRV-Profile', 'Creating Directories')
                        os.system('mkdir -p ' + fp)
                    fpm = fp + '/' + str(fName) + id2ProofType
                    fh = open(fpm, 'wb')
                    fh.write(fRaw)
                    fh.close()

                    mainFile = ''
                    # Converting to PNG
                    if str(id2ProofType) not in ['.png']:
                        id2ProofType = '.png'
                        fpx = fp + '/' + str(fName) + id2ProofType
                        filepath.append(fpx)
                        im = Image.open(fpm)
                        im.save(fpx, 'PNG')
                        os.system('rm ' + fpm)
                        os.system('chmod 755 -R ' + fp + '*')
                        mainFile = fpx
                    else:
                        filepath.append(fpm)
                        os.system('chmod 755 -R ' + fp + '*')
                        mainFile = fpm


                    if idType in ['Aadhaar Card','Voter Id Card']:
                        imgPath = mainFile
                        url = "http://localhost:2123/ocr"
                        data = {'imgPath': imgPath,'idType':idType}
                        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                        res = requests.post(url, data=json.dumps(data), headers=headers)
                        data = res.text
                        try:
                            stat = json.loads(data)
                            if stat['status'] == True:
                                if 'front' in stat['result'][0]['side']:
                                    ocrData['firstName'] = stat['result'][0]['firstName']
                                    ocrData['lastName'] = stat['result'][0]['lastName']
                                    ocrData['idNumber'] = stat['result'][0]['idNumber']
                                    ocrData['dateOfBirth'] = stat['result'][0]['dateOfBirth']
                                    ocrData['age'] = stat['result'][0]['age']
                                    ocrData['gender'] = stat['result'][0]['gender'].lower()
                                else:
                                    ocrData['address'] = stat['result'][0]['address']
                                    Log.i('OCR CAPTURED:',ocrData)
                            else:
                                Log.i('OCR CAPTURE FAILURE')
                        except:
                            Log.i('Internal Error in OCR Request')
                else:
                    message = 'Invalid File Type'
                    code = 4011
                    raise Exception
            '''
            for i in filepath:
                if os.path.exists(i):
                    os.remove(i)
                    Log.i('Removal - File found')
                else:
                    Log.i('Removal - File Not Found')
            '''
            code = 2000
            status = True
            message = "OCR DATA"
            result.append(ocrData)
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
            Log.i('FNL', response)
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
