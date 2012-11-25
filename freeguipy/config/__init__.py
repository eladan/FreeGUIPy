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

from telephonypy.router import RouteFactory
from telephonypy import config

from telephonypy.middleware import CSRFMiddleware, make_eval_exception, make_error_middleware
from .route_map import make_routes
from .env import make_config

from beaker.middleware import SessionMiddleware
from paste.cascade import Cascade
from paste.registry import RegistryManager, make_registry_manager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool


def app_factory(global_conf, static_files=True, **app_conf):
    """ App factory
    """
    # Set environment
    _config = make_config(global_conf, app_conf)
    routes = make_routes()

    app = RouteFactory(routes)

    # CSRF Middleware (turn off for remote testing from local machine Ajax calls)
#    if _config['csrf']:
#        app = CSRFMiddleware(app, _config)

    # Session Middleware
    app = SessionMiddleware(app, _config)

    # Custom Middleware Below:
    # app = SomeCoolMiddlewareOfMine(app, _config)

    # Establish the Registry for this application
    app = make_registry_manager(app, _config)

    # Error Middleware
    if _config['debug']:
        app = make_eval_exception(app, _config)
    else:
        app = make_error_middleware(app, _config)

    if asbool(static_files):
        # Serve static files
        static_app = StaticURLParser(_config['telephonypy.paths']['static'])
        app = Cascade([static_app, app])
    app.config = _config
    config.push_process_config(_config)

    return app