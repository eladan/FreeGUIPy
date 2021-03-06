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
from freeguipy.model import db

__all__=['DBBase']


class DBBase(object):
    """Base class for DB Model"""

    query = db.query_property()

    # Comparison conveniences
    def __eq__(self, other):
        if isinstance(other, self):
            return self.__class__.__name__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def __str__(self):
        try:
            return str("<{0}".format(self.__class__.__name__))+str("({0})>".format(self.name))
        except AttributeError:
            return str("<{0}".format(self.__class__.__name__))+str("({0})>".format(self.id))

    def create(self, obj):
        if type(obj) is not dict:
            raise TypeError("You need to pass a dictionary for create.")

        for k in obj:
            if hasattr(self, k):
                setattr(self, k, obj[k])

        # Modify this to change this behavior.  I use it to get ID.
        db.flush()

        return self.id

    @classmethod
    def delete(cls, id=None):
        return cls.get(id).delete()

    @classmethod
    def all(cls):
        cls.query.all()

    @classmethod
    def first(cls):
        cls.query.first()

    def todict(self):
        """ JSON Date object serializer, or what else is
        needed for convenience.
        """
        def convert_datetime(val):
            return val.strftime("%Y-%m-%d %H:%M:%S")

        for col in self.__table__.columns:
            if isinstance(col.type, DateTime):
                value = convert_datetime(getattr(self, col.name))
            else:
                value = getattr(self, col.name)

            yield (col.name, value)

    def iterfunc(self):
        """ Returns an iterable that supports .next()
        so we can do dict(cls_instance)
        """
        return self.todict()