# Copyright 2018 Geobeyond Srl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls import url

from . import views, api_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^explorer', views.explorer, name='explorer'),
    url(
        r'^api/cogs/$',
        api_views.COGListCreateView.as_view(),
        name='cog_create'
    ),
    url(
        r'^api/cogs/(?P<uuid>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/$',
        api_views.COGDetailView.as_view(),
        name='cog_detail'
    ),
    url(r'^health', views.health, name='health'),
    url(r'^404', views.handler404, name='404'),
    url(r'^500', views.handler500, name='500'),
]
