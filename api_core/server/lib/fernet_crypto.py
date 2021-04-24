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
	  b'ISO-KJH&%$*%^&(*(*^&*((&*JGHFGKHJL^(*&liUHK^^J)*T&T',
	  b'ISO-K^%$#&*&^%&()*FYTKGUTLYIY*(&^*O(&%^O*&IULG)*T&T'
	  b'ISO-KJHGI&%^$(&*OP(YHGLHUKHLI*(&^*OLY&^%&TO*&7)*T&T',
          b'ISO-K&^%$^IKTYFUGUTYTIUYGH<JB>H:O765765756587%)*T&T',
	  b'ISO-L&^%957676%(^&%&^IYKUGUHGVK<YUYIUTI^67%*&^)*T&T',
	  b'ISO-M^$**^%RJ^%RFUJTYFJHGuyfgjhkti76576hgkKU^_)*T&T',
	  b'ISO-N*^%&^%*&^IGYUTUYiyutiuytiu65%%%%766()#$@^)*T&T',
	  b'ISO-O&^%$&^%TFKTFKYTGTfkytgfftfuytfvkfkhgvjhgf)*T&X',
	  b'ISO-P8654865^%RUJTYFTGFJYMTyktru5^%$&$%^$&^%&^)*T&T',
	  b'ISO-Q5^$&U%TJF^%U$UTFRKUFKutfkhgfghgfjh@@@@%%%)*T&T',
	  b'ISO-R&^%$$7654765476547654765#####^%DHTFK^%&$&)*T&T',
	  b'ISO-S^%$EURJTCFTIY%$%$^%$45636543654tfcjfttyt%)*T&T',
	  b'ISO-&^%RTFYKUIKUGY^%65476547654tyjfjytoiuoijhh)*T&T',
	  b'ISO-1&65r65ujfR^%R765&&^*&)^*~~#@#$RUTFYTFVghf)*T&T',
	  b'ISO-2&^%$E&^UJTFYTFU%$76547654r87978756fvjhf#%)*T&T',
	  b'ISO-3*^&%&^Itktg658&658765KYUTUYTIUT865876#*&))*T&T',
	  b'ISO-4^$%RDJRDurte754745&^%*&^(*&^&^(*&^&^%$#%%)*T&T',
	  b'ISO-5&^%%865r76u5rtf6utrrryryt@@#$$$$$$$$%34t&)*T&T',
	  b'ISO-6UYTRUYTF5#^%$^%$&(^)))*&^&^&^*&^*&^%%trrr)*C&T',
	  b'ISO-7*IUYTG&^%47654&^%$&%%%%%%^54eydhtrrjiyity)*E&T',
	  b'ISO-X&*##&%^$^&%&^&())*&^)*&^)&&^*&*&^TYytittt)*T&T',
	  b'ISO-x1^^876t876t7ikgki7tgiuygkuyguytiut65#####)*T&T',
	  b'ISO-A765rujTYF&^%$&$&^%$&%$&^%$&^%$&^%$&^%TJFF)*T&T',
	  b'ISO-27%$%&^%UTJFJYTFYTRUYTRTp987698769876987^^)*T&T',
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

