#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from os.path import basename

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cwd_name = basename(os.getcwd())
os.sys.path.insert(1, parent_dir)
mod = __import__(cwd_name)
sys.modules[cwd_name] = mod
__package__ = cwd_name

from .bigbase.country import CountryHandler


from .authorization.sign_in import SignInHandler
from .authorization.sign_up import SignUpHandler
from .authorization.sign_up_v2 import SignUpV2Handler
from .check.check_update import CheckUpdateHandler

from .resource.profile import MtimeProfileHandler

from .forms.forms import FormsHandler
from .forms.forms_data import FormsDataHandler

from .lib.lib import *
