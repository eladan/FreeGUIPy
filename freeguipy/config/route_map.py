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

# Routing for URL to controller/method translation
from telephonypy.router import Map


def make_routes():
    routes = []

    routes.append(Map(template='/', handler='freeguipy.controllers.root:Root', action='home'))
    routes.append(Map(template='/login', handler='freeguipy.controllers.root:Root', action='login'))
    routes.append(Map(template='/{action}', handler='freeguipy.controllers.root:Root'))
    routes.append(Map(template='/{action}/{id}', handler='freeguipy.controllers.root:Root'))

    return routes