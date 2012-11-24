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
from freeguipy.model import metadata, ForeignKey, Integer, Column, Table

# Mapping for users to groups
user_groups = Table('user_groups', metadata,
    Column('user_id', Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('group_id', Integer, ForeignKey('groups.id', onupdate="CASCADE", ondelete="CASCADE"))
)

# Mapping for admin users to admin groups
admin_user_groups = Table('admin_user_groups', metadata,
    Column('admin_user_id', Integer, ForeignKey('admin_users.id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('admin_group_id', Integer, ForeignKey('admin_groups.id', onupdate="CASCADE", ondelete="CASCADE"))
)

# Mapping group/perms for object-level permissions
group_permissions = Table('group_permissions', metadata,
    Column('group_id', Integer, ForeignKey('groups.id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('permission_id', Integer, ForeignKey('permissions.id', onupdate="CASCADE", ondelete="CASCADE"))
)

# Mapping for users to companies
user_companies = Table('user_companies', metadata,
    Column('user_id', Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('company_id', Integer, ForeignKey('companies.id', onupdate="CASCADE", ondelete="CASCADE"))
)

# Mapping for companies to contexts
company_contexts = Table('company_contexts', metadata,
    Column('company_id', Integer, ForeignKey('companies.id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('context_id', Integer, ForeignKey('contexts.id', onupdate="CASCADE", ondelete="CASCADE")),

)

# Mapping for companies to addresses
company_addresses = Table('company_addresses', metadata,
    Column('company_id', Integer, ForeignKey('companies.id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('address_id', Integer, ForeignKey('addresses.id', onupdate="CASCADE", ondelete="CASCADE")),

)

# Mapping for companies to tickets
company_tickets = Table('company_tickets', metadata,
    Column('company_id', Integer, ForeignKey('companies.id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('ticket_id', Integer, ForeignKey('tickets.id', onupdate="CASCADE", ondelete="CASCADE")),

)

# Mapping for companies to notes
company_notes = Table('company_notes', metadata,
    Column('company_id', Integer, ForeignKey('companies.id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('note_id', Integer, ForeignKey('notes.id', onupdate="CASCADE", ondelete="CASCADE")),

)

# Mapping for users to notes
user_notes = Table('user_notes', metadata,
    Column('user_id', Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('note_id', Integer, ForeignKey('notes.id', onupdate="CASCADE", ondelete="CASCADE")),

)
