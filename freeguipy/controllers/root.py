"""
    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.

    Software distributed under the License is distributed on an "AS IS"
    basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
    License for the specific language governing rights and limitations
    under the License.

    The Original Code is TelephonyPy.

    The Initial Developer of the Original Code is Noel Morgan,
    Copyright (c) 2012 Noel Morgan. All Rights Reserved.

    http://www.telephonypy.org/

    You may not remove or alter the substance of any license notices (including
    copyright notices, patent notices, disclaimers of warranty, or limitations
    of liability) contained within the Source Code Form of the Covered Software,
    except that You may alter any license notices to the extent required to
    remedy known factual inaccuracies.
"""
import os
import time

import telephonypy
from telephonypy import tmpl_context as c, session
from telephonypy.decorators import xml, xml_render, htmlout, html_render, jsonify, authorize, credential

from freeguipy.model import User
from base import BaseController


class Root(BaseController):

    @authorize(credential('admin'))
    @xml("test.xml")
    def home(self, request, *args, **kwargs):
        session['test'] = "test value"
        c.test = User.query.filter_by(id=1).first().first_name
        return xml_render()

    @htmlout('base.html')
    def one(self, request, *args, **kwargs):
        return html_render(user="jim")

    @authorize(credential('admin root superuser'))
    @jsonify
    def login(self, request, *args, **kwargs):
        return {'ok':'not ok'}
