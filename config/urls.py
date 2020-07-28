# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.schemas import SchemaGenerator
from rest_framework.documentation import include_docs_urls

class CustomGenerator(SchemaGenerator):
    def create_view(self, callback, method, request=None):
        view = super(CustomGenerator, self).create_view(callback, method, request)
        view.schema.view = view
        return view

docs = include_docs_urls(
    generator_class=CustomGenerator, title='Bitmex API', description='Bitmex API documentation.',)


urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name="home"),
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
    path('users/', include('arsmoon.users.urls')),

    # API documentation
    path('docs/', docs, name='docs'),

    # API urls
    path('api/v1/', include('arsmoon.bitmex.api_urls')),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
