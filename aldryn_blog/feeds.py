# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from aldryn_blog.models import Post


class LatestEntriesFeed(Feed):
    def link(self):
        return reverse('latest-posts', current_app='blog')

    def title(self):
        return _('Blog posts on %(site_name)s') % {'site_name': Site.objects.get_current().name}

    def items(self, obj):
        return Post.published.order_by('-publication_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.lead_in


class TagFeed(LatestEntriesFeed):
    def get_object(self, request, tag):
        return tag

    def items(self, obj):
        return Post.published.filter(tags__slug=obj)[:10]