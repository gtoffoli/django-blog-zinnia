# -*- coding: utf-8 -*-
"""
Extensible permission system for zinnia,
inspired by the permission system of pybbm (Django forums)
"""

from importlib import import_module
from django.conf import settings
from zinnia.managers import PUBLISHED # other status: DRAFT, HIDDEN, 

class DefaultPermissionHandler:
    """
    If you want to implement custom permissions, you can inherit from this class
    and override any of the `filter_*` and `can_*` methods. Methods starting with
    `can` are expected to return `True` or `False`, whereas methods starting with `filter_*`
    should filter the queryset they receive, and return a new queryset containing only the
    objects the user is allowed to see.

    To activate your custom permission handler, set `settings.ZINNIA_PERMISSION_HANDLER` to
    the full qualified name of your class, e.g. "`commons.zinnia_adapter.MyPermissionHandler`".
    """

    def can_add_category(self, user):
        """return True if `user` is allowed to create a new category """
        if user.is_superuser:
            return True
        return user.has_perm("zinnia.can_add_category")

    def can_delete_category(self, user, category):
        """return True if `user` is allowed to delete a category """
        if user.is_superuser:
            return True
        return user.has_perm("zinnia.can_delete_category")

    def can_change_category(self, user, category):
        """return True if `user` is allowed to modify category """
        if user.is_superuser:
            return True
        return user.has_perm("zinnia.can_delete_category")

    def filter_entries(self, user, qs):
        """return a queryset with forums `user` is allowed to see"""
        if user.is_superuser or user.has_perm("zinnia.can_view_all"):
            return qs
        return qs.filter(status=PUBLISHED)

    def can_create_entry(self, user):
        """return True if `user` is allowed to create a new bog """
        if user.is_superuser:
            return True
        return user.has_perm("zinnia.can_add_entry")

    def can_change_authors(self, user, entry):
        """return True if `user` is allowed to change the entry author(s) """
        if user.is_superuser:
            return True
        return user.has_perm("zinnia.can_change_author")

    def can_change_entry(self, user, entry):
        """return True if `user` is allowed to modify the entry """
        if user.is_superuser:
            return True
        if not entry.authors.filter(username=user.username):
            return False
        return user.has_perm("zinnia.can_change_entry")

    def can_change_status(self, user, entry):
        if user.is_superuser:
            return True
        if not entry.authors.filter(username=user.username):
            return False
        return user.has_perm("zinnia.can_change_status")

    def can_comment_entry(self, user, entry):
        if user.is_superuser:
            return True
        if not entry.comments_are_open:
            return False
        return user.is_authenticated

def resolve_class(name):
    """resolves a class function given as string, returning the function"""
    if not name:
        return None
    modname, funcname = name.rsplit(".", 1)
    print('resolve_class', modname, funcname)
    return getattr(import_module(modname), funcname)()

perms = resolve_class(settings.ZINNIA_PERMISSION_HANDLER)
