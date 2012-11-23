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
import copy
import logging
import telephonypy

from genshi.template import TemplateLoader
from sqlalchemy import engine_from_config
from freeguipy.model import init_model
from freeguipy.lib import helpers, app_globals
from paste.deploy.converters import asbool
from webhelpers.mimehelper import MIMETypes
from telephonypy.configuration import TelephonyPyConfig

log = logging.getLogger(__name__)

def make_config(global_conf, app_conf):
    config = TelephonyPyConfig()

    # App paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
        controllers=os.path.join(root, 'controllers'),
        static=os.path.join(root, 'static'),
        templates=[os.path.join(root, 'templates')])

    # Initialize config with the defaults
    config.init_defaults(global_conf, app_conf, package='freeguipy', paths=paths)
    config['telephonypy.app_globals'] = app_globals.Globals(config)
    config['telephonypy.h'] = helpers

    # Setup cache object as early as possible
    import telephonypy
    telephonypy.cache._push_object(config['telephonypy.app_globals'].cache)

    # Setup the SQLAlchemy database engine
    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)

    return config

