"""Views for Zinnia entries"""
from django.conf import settings
from django.views.generic.dates import BaseDateDetailView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.admin.views.decorators import staff_member_required

from zinnia.forms import EntryEditForm
from zinnia.managers import DRAFT

from zinnia.models import Entry, Author
from zinnia.views.mixins.archives import ArchiveMixin
from zinnia.views.mixins.callable_queryset import CallableQuerysetMixin
from zinnia.views.mixins.entry_cache import EntryCacheMixin
from zinnia.views.mixins.entry_preview import EntryPreviewMixin
from zinnia.views.mixins.entry_protection import EntryProtectionMixin
from zinnia.views.mixins.templates import EntryArchiveTemplateResponseMixin


class EntryDateDetail(ArchiveMixin,
                      EntryArchiveTemplateResponseMixin,
                      CallableQuerysetMixin,
                      BaseDateDetailView):
    """
    Mixin combinating:

    - ArchiveMixin configuration centralizing conf for archive views
    - EntryArchiveTemplateResponseMixin to provide a
      custom templates depending on the date
    - BaseDateDetailView to retrieve the entry with date and slug
    - CallableQueryMixin to defer the execution of the *queryset*
      property when imported
    """
    queryset = Entry.published.on_site


class EntryDetail(EntryCacheMixin,
                  EntryPreviewMixin,
                  EntryProtectionMixin,
                  EntryDateDetail):
    """
    Detailled archive view for an Entry with password
    and login protections and restricted preview.
    """


def EntryCreate(request, sites=[settings.SITE_ID]):
    form_class = EntryEditForm
    template_name = "zinnia/entry_edit.html"
    if request.POST:
        form = form_class(request.POST)
        data_dict = {'form': form}
        if form.is_valid():
            entry = form.save()
            entry.slug = slugify(entry.title)
            author = Author.objects.get(username=request.user.username)
            entry.authors.add(author)
            entry.save()
            entry_id = entry.id
            if request.POST.get('save', ''): 
                return HttpResponseRedirect(entry.get_absolute_url())
            else: # save and continue
                data_dict['action'] = '/weblog/entry/{}/update/'.format(entry_id)
                return render(request, template_name, data_dict)
        else:
            data_dict['action'] = '/weblog/entry/new/'
    else:
        form = EntryEditForm(initial={'status': DRAFT, 'sites': sites, 'comment_enabled': False,})
        data_dict = {'form': form, 'action': '/weblog/entry/new/'}
    return render(request, template_name, data_dict)


def EntryView(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    return HttpResponseRedirect(entry.get_absolute_url())


def EntryUpdate(request, entry_id):
    form_class = EntryEditForm
    template_name = "zinnia/entry_edit.html"
    if request.POST:
        entry = get_object_or_404(Entry, id=entry_id)
        form = form_class(request.POST, instance=entry)
        data_dict = {'form': form, 'entry': entry, 'action': '/weblog/entry/{}/update/'.format(entry_id)}
        if form.is_valid():
            entry = form.save()
            author = Author.objects.get(username=request.user.username)
            entry.authors.add(author)
            if request.POST.get('save', ''): 
                return HttpResponseRedirect(entry.get_absolute_url())
            else: # save and continue
                data_dict['entry'] = entry
                return render(request, template_name, data_dict)
        else:
            return render(request, template_name, data_dict)
    else:
        entry = get_object_or_404(Entry, id=entry_id)
        form = EntryEditForm(instance=entry)
        action = '/weblog/entry/{}/update/'.format(entry_id)
        data_dict = {'form': form, 'entry': entry, 'action': action}
        return render(request, template_name, data_dict)

