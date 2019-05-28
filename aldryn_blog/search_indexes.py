# -*- coding: utf-8 -*-
from aldryn_search.utils import get_index_base, strip_tags
from cms.plugin_rendering import ContentRenderer
from django.db.models import Q
from sekizai.context import SekizaiContext

from .conf import settings
from .models import Post


def render_plugin(request, plugin_instance):
    renderer = ContentRenderer(request)
    context = SekizaiContext(request)
    context['request'] = request
    return renderer.render_plugin(plugin_instance, context)


class BlogIndex(get_index_base()):
    haystack_use_for_indexing = settings.ALDRYN_BLOG_SEARCH

    INDEX_TITLE = True  # for backward compatibility until 1.1.0 aldryn-search
    index_title = True

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.lead_in

    def get_language(self, obj):
        return obj.language

    def prepare_pub_date(self, obj):
        return obj.publication_start

    def get_index_queryset(self, language):
        queryset = self.get_model().published.all()
        return queryset.filter(Q(language=language) | Q(language__isnull=True))

    def get_model(self):
        return Post

    def get_search_data(self, obj, language, request):
        lead_in = self.get_description(obj)
        text_bits = [strip_tags(lead_in)]
        plugins = obj.content.cmsplugin_set.filter(language=language)
        for base_plugin in plugins:
            instance, plugin_type = base_plugin.get_plugin_instance()
            if instance is not None:
                content = strip_tags(render_plugin(request, instance))
                text_bits.append(content)
        return ' '.join(text_bits)
