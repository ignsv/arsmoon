# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name="home"),
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
    path('users/', include('arsmoon.users.urls')),
    path('bitmex/', include('arsmoon.bitmex.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
