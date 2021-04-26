#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import calendar
import datetime as dtime
import os
import sys
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .log_util import Log

CODES = [
	  b'ISO-KJHGI&^IK&*&^%T^RYKUT&LIY*(OUIYUYFTYFUTY&&)*T&T',
	  b'ISO-@%$#4ertyr8765867*^&%%$@#%$#@898767997^%$#$*T&T',
	  b'ISO-**I&^587657i5786%@$#%$#@$%%$%%%%%%%####^%$#*T&T',
	  b'ISO-^%$EYRTHFKYUt6758765%%%%$#%$#@%$@#%$#@%$#%$*T&T',
	  b'ISO-^&%$#^%$EYrtdyutrut75647####&543654365436*@*T&T',
	  b'ISO-^%4354rdtfjouy876(&^654365436543$#@@#@@@@@@*T&T',
	  b'ISO-LJHGKJHGFKGKJHGO*&&(^%$&^%$&^%$&^%$&^%TJFF)*T&T',
	  b'ISO-&^%TGGLUIYOIYOIYOKGKH%$&^%$&^%$&^%$&^%TJFF)*T&T',
	  b'ISO-5423fYTUIYIUyiluhljhpiyoiuy^&*^87%$&^%TJFF)*T&T',
	  b'ISO-OLIU98708iouioupuipoiupoiujkhljh^%$&^%TJFF)*T&T',
	  b'ISO-Okkhgi5643654rt1#$$$$ujtytryffff^%$&^%TJFF)*T&T',
	  b'ISO-Pkhguy111111111!!!!!!!!!ikuytuyt^%$&^%TJFF)*T&T',
	  b'ISO-EEoiuyiuhlu&^%$^^^^^^^^^^^^^khfg)%$&^%TJFF)*T&T',
	  b'ISO-*^$%$$#^%$Erdjcgliuyoiy9876976))7%$&^%TJFF)*T&T',
	  b'ISO-#$@%$T#edkyugtuytwieuyrtwieuyrweirytwtei981*T&T',
	  b'ISO-2394769&*^YOUIYHOIUYYOIYOIUY457654@@@@@@((&*T&T',
	  b'ISO-T&T365465*%^$&6////////sdfsdsdfsdfsd8765486*T&T',
	  b'ISO-$32543u6ytfUYOTYUt76547654@@@^$366754365436*T&T',
	  b'ISO-(&^%*&657iygfiytq2763521637123i12yashdgas22*T&T',
	  b'ISO-%^5465rujytfytr#####658767697698769876&^%$8*T&T',
	  b'ISO-#@%$#fgyut765658765876%$#^%$#^%$*$%^*$&GHKG*T&T',
	  b'ISO-%$#@%$#Wjyutiuytiuytgiuyt765476547654765475*T&T',
	  b'ISO-^%43rtdutruytitwiuyasiduyastiudt12321312312*T&T',
	  b'ISO-1283765tksuhgdas%$#^###sd2##%^4765476547112*T&T',
	]

# Monday, July 15, 2019 15:34:17
SALT = b'1563204857'
FERNETS = []

for c in CODES:
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=SALT,
            iterations=100000,
            backend=default_backend()
          )
    key = base64.urlsafe_b64encode(kdf.derive(c))
    f = Fernet(key)
    FERNETS.append(f)


def FN_ENCRYPT(payload=str, encode=False):

    try:
        if len(FERNETS):
            index = random.randint(0, len(FERNETS) - 1)
            f = FERNETS[index]
            if (encode):
                return f.encrypt(payload.encode())
            else:
                return f.encrypt(payload)
    except Exception as e:
        Log.i(e)
        return False
    return False

def FN_DECRYPT(token=str):

    try:
        if len(FERNETS):
            for f in FERNETS:
                try:
                    d_token = f.decrypt(token.encode())
                    return d_token
                except Exception as e:
                    #Log.i(e)
                    continue
    except Exception as e:
        Log.i(e)
        return False
    return False

