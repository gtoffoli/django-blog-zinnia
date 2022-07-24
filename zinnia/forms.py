"""Forms for Zinnia """
from django import forms
from django.utils.translation import gettext_lazy as _

from zinnia.models.entry import Entry


class EntryEditForm(forms.ModelForm):
    """
    Form for Entry creation and editing on the regular UI.
    content is richtext; TinyMCE is a required; tested with django-tinymce-4
    Initially derived from class EntryAdminForm
    """

    class Meta:
        """
        EntryEditForm's Meta.
        """
        model = Entry
        fields = ['title', 'lead', 'excerpt', 'content', 'status', 'comment_enabled', 'sites',]
    title = forms.CharField(required=True, label=_('title'), widget=forms.TextInput(attrs={'class':'form-control',}))
    lead = forms.CharField(required=False, label=_('lead'), widget=forms.TextInput(attrs={'class':'form-control',}))
    excerpt = forms.CharField(required=False, label=_('excerpt'), widget=forms.TextInput(attrs={'class':'form-control',}))
    content = forms.CharField(required=False, label=_('content'), widget=forms.Textarea(attrs={'class':'form-control richtext', 'rows': 10,}))
