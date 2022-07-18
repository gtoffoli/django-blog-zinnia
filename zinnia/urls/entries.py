"""Urls for the Zinnia entries"""
from django.urls import re_path

from zinnia.views.entries import EntryDetail, EntryCreate, EntryView, EntryUpdate

urlpatterns = [
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
            EntryDetail.as_view(),
            name='entry_detail'),
    re_path(r'^entry/new/$',
            EntryCreate,
            name='entry_create'),
    re_path(r'^entry/(?P<entry_id>[\d-]+)/$',
            EntryView,
            name='entry_view'),
    re_path(r'^entry/(?P<entry_id>[\d-]+)/update/$',
            EntryUpdate,
            name='entry_update'),
]
