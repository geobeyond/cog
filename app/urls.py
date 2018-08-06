from django.conf.urls import url

from . import views, api_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
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
