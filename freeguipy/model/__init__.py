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
from hashlib import sha1
import datetime
from datetime import datetime
import transaction
import sqlalchemy
from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.types import Integer, DateTime, Boolean, Unicode, UnicodeText, Float
from sqlalchemy.orm import relation, synonym, relationship, backref
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import and_, or_, not_
from zope.sqlalchemy import ZopeTransactionExtension


__all__ = ['User', 'Group', 'Permission', 'db', 'DataBase']

# DBSession Object
db =  scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

from freeguipy.model.base import DBBase
DataBase = declarative_base(cls=DBBase)
metadata = DataBase.metadata

def init_model(engine):
    db.configure(bind=engine)

    def insert():
        DataBase.metadata.drop_all(engine)
        DataBase.metadata.create_all(engine)

        with transaction.manager:
            # Create the groups for two types of users (for now)
            auth_group = Group(u'auth', u'Regular user account.')
            admin_group = Group(u'admin', u'Administrative user account.')
            auth_group.permissions.append(Permission(u'auth'))
            admin_group.permissions.append(Permission(u'admin'))

            # add them to the db session
            db.add(auth_group)
            db.add(admin_group)
            transaction.commit()

            # Create the admin user so we can always access the system as admin.
            su = User(first_name=u'Admin', last_name=u'User', username=u'nobody@domain.com',
                email=u'nobody@domain.com')
            su._set_password('admin')
            su.groups.append(admin_group)
            db.add(su)
            transaction.commit()


    insert()

from freeguipy.model.core import User, Group, Permission
