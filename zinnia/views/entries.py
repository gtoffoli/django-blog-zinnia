"""Views for Zinnia entries"""
# from django.views.generic import CreateView, UpdateView
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

""" see also:
https://stackoverflow.com/questions/17192737/django-class-based-view-for-both-create-and-update
https://chriskief.com/2015/01/19/create-or-update-with-a-django-modelform/
"""

"""
class EntryEditMixin(TemplateResponseMixin):
    pass

class EntryCreate(EntryEditMixin, CreateView):
    form_class = EntryEditForm
    template_name = "zinnia/entry_edit.html"
    # fields = ['title', 'status', 'content', 'sites', 'comment_enabled',]
    initial = {'status': DRAFT, 'sites': [1], 'comment_enabled': False,}
    success_url="/weblog/"


class EntryUpdate(EntryEditMixin, UpdateView):
    form_class = EntryEditForm
    template_name = "zinnia/entry_edit.html"
    fields = ['id']
    success_url="/weblog/"
"""

@staff_member_required
def EntryCreate(request):
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
            else:
                data_dict['action'] = '/weblog/entry/{}/update/'.format(entry_id)
                return render(request, template_name, data_dict)
        else:
            data_dict['action'] = '/weblog/entry/new/'
    else:
        form = EntryEditForm(initial={'status': DRAFT, 'sites': [1], 'comment_enabled': False,})
        data_dict = {'form': form, 'action': '/weblog/entry/new/'}
    return render(request, template_name, data_dict)

@staff_member_required
def EntryView(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    return HttpResponseRedirect(entry.get_absolute_url())

@staff_member_required
def EntryUpdate(request, entry_id=None):
    form_class = EntryEditForm
    template_name = "zinnia/entry_edit.html"
    if request.POST:
        entry_id = request.POST.get('id', '')
        entry = get_object_or_404(Entry, id=entry_id)
        form = form_class(request.POST, instance=entry)
        data_dict = {'form': form}
        if form.is_valid():
            entry = form.save()
            author = Author.objects.get(username=request.user.username)
            entry.authors.add(author)
            entry_id = entry.id
            if request.POST.get('save', ''): 
                return HttpResponseRedirect(entry.get_absolute_url())
            else:
                data_dict['action'] = '/weblog/entry/{}/update/'.format(entry_id)
                return render(request, template_name, data_dict)
    else:
        entry = get_object_or_404(Entry, id=entry_id)
        form = EntryEditForm(instance=entry)
        action = '/weblog/entry/{}/update/'.format(entry_id)
        data_dict = {'form': form, 'action': action}
        return render(request, template_name, data_dict)

