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
from freeguipy.model import DataBase
from mapping import user_groups, group_permissions



class Group(DataBase):
    """
    Groups
    """
    __tablename__ = 'groups'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(64), unique=True, nullable=False)
    description = Column(UnicodeText)
    created_date = Column(DateTime, default=datetime.now())

    @property
    def permissions(self):
        perms = []
        for perm in self.permissions:
            perms.append(perm.name)
        return perms

    def __init__(self, name, description=None, date=None):
        self.name = name
        self.description = description or name
        self.created_date = datetime.now()

    def __repr__(self):
        return "<Group({0},{1},{2})>".format(self.name, self.description, self.created_date)

    def __unicode__(self):
        return self.name


class Permission(DataBase):
    """
    Permissions
    """
    __tablename__='permissions'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(32), default=u'Unknown')
    description = Column(Unicode(255), default=u'Unknown')

    groups =  relationship("Group", secondary=group_permissions, backref='permissions')

    def __unicode__(self):
        return self.name

    def __init__(self, name, description=None):
        self.name = name
        self.description = description or name

    def __repr__(self):
        return "<Permission({0})>".format(self.name)


class User(DataBase):
    """
    User model
    """
    __tablename__='users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(Unicode(128), unique=True, nullable=False)
    first_name = Column(Unicode(128), nullable=True)
    last_name = Column(Unicode(128), nullable=True)
    password = Column(Unicode(255), nullable=False)
    active = Column(Boolean, default=True)
    email = Column(Unicode(128), nullable=True)
    tel = Column(Unicode(64), nullable=True)
    mobile = Column(Unicode(64), nullable=True)

    groups = relationship(Group, secondary='user_groups')

    @classmethod
    def by_id(cls, id):
        return User.query.filter(User.id==id).first()

    @classmethod
    def by_username(cls, username):
        return User.query.filter(User.username==username).first()

    @classmethod
    def credentials(cls, username):
        u = User.query.filter(User.username==username).first()
        if u is not None:
            return u.permissions
        return None

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return str(self.first_name) + " " + str(self.last_name)
        return self.username

    @property
    def permissions(self):
        perms = []
        for g in self.groups:
            perms.append(g.permissions)
        return perms

    def _set_password(self, password):
        hashed_password = password

        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()

        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        self.password = hashed_password

    def validate_password(self, password):
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()

    def __repr__(self):
        '''Proper formatting for session storage and retrieval as pickled User object.
        '''
        return "<User({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10})>".format(
            self.id,self.username, self.first_name, self.last_name, self.password,
            self.active, self.email, self.tel, self.mobile)