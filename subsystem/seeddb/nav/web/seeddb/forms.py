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

from django import forms

from nav.models.cabling import Cabling, Patch
from nav.models.manage import Netbox, NetboxType, Room, Location, Organization, Usage, Vendor, Subcategory, Vlan, Prefix, Category
from nav.models.service import Service

class NetboxFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        Category.objects.order_by('id').all(), required=False)
    room = forms.ModelChoiceField(
        Room.objects.order_by('id').all(), required=False)
    organization = forms.ModelChoiceField(
        Organization.objects.order_by('id').all(), required=False)

class RoomFilterForm(forms.Form):
    location = forms.ModelChoiceField(
        Location.objects.order_by('id').all(), required=False)

class RoomMoveForm(forms.Form):
    location = forms.ModelChoiceField(Location.objects.order_by('id').all(), required=True)

class NetboxForm(forms.ModelForm):
    class Meta:
        model = Netbox
        fields = (
            'ip', 'sysname', 'category', 'room', 'organisation', 'read_only',
            'read_write'
        )

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            del self.fields['id']

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization

    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            del self.fields['id']

class UsageForm(forms.ModelForm):
    class Meta:
        model = Usage

    def __init__(self, *args, **kwargs):
        super(UsageForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            del self.fields['id']

class NetboxTypeForm(forms.ModelForm):
    class Meta:
        model = NetboxType

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory

class PrefixForm(forms.ModelForm):
    class Meta:
        model = Prefix

class CablingForm(forms.ModelForm):
    class Meta:
        model = Cabling

class PatchForm(forms.ModelForm):
    class Meta:
        model = Patch
