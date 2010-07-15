# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 UNINETT AS
#
# This file is part of Network Administration Visualized (NAV).
#
# NAV is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License version 2 as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.  You should have received a copy of the GNU General Public License
# along with NAV. If not, see <http://www.gnu.org/licenses/>.
#

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404

#from nav.django.utils import get_verbose_name
from nav.web.message import new_message, Messages
from nav.models.cabling import Cabling, Patch
from nav.models.manage import Netbox, NetboxType, Room, Location, Organization
from nav.models.manage import Usage, Vendor, Subcategory, Vlan, Prefix
from nav.models.service import Service

from nav.web.seeddb.forms import RoomForm, LocationForm, OrganizationForm, \
    UsageForm, NetboxTypeForm, VendorForm, SubcategoryForm, PrefixForm, \
    CablingForm, PatchForm

class SeeddbEdit(object):
    model = None
    form_model = None
    identifier_attr = 'pk'
    title_attr = 'pk'
    navpath = None
    tab_template = ''
    template = 'seeddb/edit.html'
    redirect = ''

    def __new__(cls, request, object_id=None):
        obj = super(SeeddbEdit, cls).__new__(cls)
        return obj(request, object_id)

    def __call__(self, request, object_id=None):
        self.request = request
        self.identifier = None
        self.title = None
        self.verbose_name = self.model._meta.verbose_name
        object = None
        if object_id:
            try:
                object = self._get_object(object_id)
            except self.model.DoesNotExist:
                raise Http404

        if request.method == 'POST':
            form = self.form_model(request.POST, instance=object)
            if form.is_valid():
                object = self.save(form, object)
                return HttpResponseRedirect(reverse(self.redirect, args=(self.identifier,)))
        else:
            form = self.form_model(instance=object)

        context = {
            'object': object,
            'form': form,
            'title': 'Add new %s' % self.verbose_name,
            'active': {'add': True},
            'navpath': self.navpath,
            'tab_template': self.tab_template,
        }
        if object:
            context.update({
                'title': 'Edit %s "%s"' % (self.verbose_name, self.title),
                'active': {'edit': True},
            })
        return render_to_response(self.template,
            context, RequestContext(request))

    def _get_object(self, object_id):
        params = {self.identifier_attr: object_id}
        object = self.model.objects.get(**params)
        self.identifier = getattr(object, self.identifier_attr)
        self.title = getattr(object, self.title_attr)
        return object

    def save(self, form, object):
        object = form.save()
        self.identifier = getattr(object, self.identifier_attr)
        self.title = getattr(object, self.title_attr)
        new_message(self.request._req,
             "Saved %s %s" % (self.verbose_name, self.title),
             Messages.SUCCESS)
        return object

class SeeddbPrimaryKeyEdit(SeeddbEdit):
    def save(self, form, object):
        data = form.cleaned_data
        if 'id' in data and object and data['id'] != object.id:
            new_pk = self.primary_key_update(form, object)
            object = self._get_object(new_pk)
            form = self.form_model(self.request.POST, instance=object)
        return super(SeeddbPrimaryKeyEdit, self).save(form, object)

    def primary_key_update(self, form, object):
        from django.db import connection
        cur = connection.cursor()

        table = object._meta.db_table
        pk_col = object._meta.get_field('id').db_column
        old_pk_val = getattr(object, object._meta.get_field('id').attname)
        new_pk_val = form.cleaned_data['id']

        sql = 'UPDATE "%s" ' % table
        sql += 'SET "%s" = %%s ' % pk_col
        sql += 'WHERE "%s" = %%s' % pk_col

        params = (new_pk_val, old_pk_val)
        cur.execute(sql, params)

        return new_pk_val

class NetboxEdit(SeeddbEdit):
    # FIXME
    def __new__(cls, request, netbox_id=None):
        raise Exception, "Not implemented"

class ServiceEdit(SeeddbEdit):
    # FIXME
    def __new__(cls, request, service_id=None):
        raise Exception, "Not implemented"

class RoomEdit(SeeddbPrimaryKeyEdit):
    model = Room
    form_model = RoomForm
    navpath = [('stuffz', None)]
    tab_template = 'seeddb/tabs_room.html'
    redirect = 'seeddb-room-edit'

    def __new__(cls, request, room_id=None):
        return super(RoomEdit, cls).__new__(cls, request, room_id)

class LocationEdit(SeeddbEdit):
    model = Location
    form_model = LocationForm
    navpath = [('stuffz', None)]
    tab_template = 'seeddb/tabs_location.html'
    redirect = 'seeddb-location-edit'

    def __new__(cls, request, location_id=None):
        return super(LocationEdit, cls).__new__(cls, request, location_id)

class OrganizationEdit(SeeddbEdit):
    model = Organization
    form_model = OrganizationForm
    navpath = [('stuffz', None)]
    tab_template = 'seeddb/tabs_organization.html'
    redirect = 'seeddb-organization-edit'

    def __new__(cls, request, organization_id=None):
        super(OrganizationEdit, cls).__new__(cls, request, organization_id)

class UsageEdit(SeeddbEdit):
    model = Usage
    form_model = UsageForm
    navpath = [('stuffz', None)]
    tab_template = 'seeddb/tabs_usage.html'
    redirect = 'seeddb-usage-edit'

    def __new__(cls, request, usage_id=None):
        super(UsageEdit, cls).__new__(cls, request, usage_id)

class NetboxTypeEdit(SeeddbEdit):
    model = NetboxType
    form_model = NetboxTypeForm
    navpath = [('stuffz', None)]
    tab_template = 'seeddb/tabs_type.html'
    redirect = 'seeddb-type-edit'

    def __new__(cls, request, type_id=None):
        super(NetboxTypeEdit, cls).__new__(cls, request, type_id)

class VendorEdit(SeeddbEdit):
    model = Vendor
    form_model = VendorForm
    navpath = [('stuffz', None)]
    tab_template = 'seeddb/tabs_vendor.html'
    redirect = 'seeddb-vendor-edit'

    def __new__(cls, request, vendor_id=None):
        super(VendorEdit, cls).__new__(cls, request, vendor_id)

class SubcategoryEdit(SeeddbEdit):
    model = Subcategory
    form_model = SubcategoryForm
    navpath = [('stuffz', None)]
    tab_template = 'seedb/tabs_subcategory.html'
    redirect = 'seeddb-subcategory-edit'

    def __new__(cls, request, subcategory_id=None):
        super(SubcategoryEdit, cls).__new__(cls, request, subcategory_id)

class VlanEdit(SeeddbEdit):
    # FIXME
    def __new__(cls, request, vlan_id):
        raise Exception, "Not implemented"

class PrefixEdit(SeeddbEdit):
    model = Prefix
    form_model = PrefixForm
    navpath = [('stuffz', None)]
    tab_template = 'seeddb/tabs_prefix.html'
    redirect = 'seeddb-prefix-edit'

    def __new__(cls, request, prefix_id=None):
        super(PrefixEdit, cls).__new__(cls, request, prefix_id)

class CablingEdit(SeeddbEdit):
    model = Cabling
    form_model = CablingForm
    navpath = [('stuffz', None)]
    tab_template = 'seeddb/tabs_cabling.html'
    redirect = 'seeddb-cabling-edit'

    def __new__(cls, request, cabling_id=None):
        super(CablingEdit, cls).__new__(cls, request, cabling_id)

class PatchEdit(SeeddbEdit):
    model = Patch
    form_model = PatchForm
    navpath = [('stuffz', None)]
    tab_template = 'seeddb/tabs_patch.html'
    redirect = 'seeddb-patch-edit'

    def __new__(cls, request, patch_id=None):
        super(PatchEdit, cls).__new__(cls, request, patch_id)
