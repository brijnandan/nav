#
# Copyright (C) 2013 UNINETT AS
#
# This file is part of Network Administration Visualized (NAV).
#
# NAV is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.  You should have received a copy of the GNU General Public
# License along with NAV. If not, see <http://www.gnu.org/licenses/>.
#
"""Module comment"""

from django.conf.urls import patterns, include, url
from . import (list_navlets, get_user_navlets, add_user_navlet,
               remove_user_navlet)
from .portadmin import NavletPortadmin
from .machinetracker import MachineTrackerNavlet
from .status import StatusNavlet
from .vlangraph import VlanGraphNavlet

urlpatterns = patterns('',
    url(r'^list-navlets/', list_navlets, name='list-navlets'),
    url(r'^get-user-navlets/', get_user_navlets, name='get-user-navlets'),
    url(r'^add-user-navlet/', add_user_navlet, name='add-user-navlet'),
    url(r'^remove-user-navlet/', remove_user_navlet,
        name='remove-user-navlet'),
    url(r'^portadmin/', NavletPortadmin.as_view(),
        name='navlet-portadmin'),
    url(r'^machinetracker/', MachineTrackerNavlet.as_view(),
        name='navlet-machinetracker'),
    url(r'^status/', StatusNavlet.as_view(),
        name='navlet-status'),
    url(r'^vlangraph/', VlanGraphNavlet.as_view(),
        name='navlet-vlangraph')
)