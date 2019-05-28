# -*- coding: utf-8 -*-
from django.urls import NoReverseMatch
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _

from aldryn_blog.models import Category

from cms.menu_bases import CMSAttachMenu
from menus.base import NavigationNode
from menus.menu_pool import menu_pool


class BlogCategoryMenu(CMSAttachMenu):

    name = _('Blog Categories')

    def get_nodes(self, request):
        nodes = []
        categories = Category.objects.language()
        # bug in hvad - Meta ordering isn't preserved
        categories = categories.order_by('ordering')

        for category in categories:
            try:
                node = NavigationNode(category.name,
                                      category.get_absolute_url(),
                                      category.slug)
                nodes.append(node)
            except NoReverseMatch:
                pass
        return nodes

menu_pool.register_menu(BlogCategoryMenu)


def clear_menu_cache(**kwargs):
    menu_pool.clear(all=True)

post_save.connect(clear_menu_cache, sender=Category)
post_delete.connect(clear_menu_cache, sender=Category)
