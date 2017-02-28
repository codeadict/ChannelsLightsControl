"""ChannelsLightsControl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from channels import include as routing_include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from lights.views import LightListView, LightDetailView, switch

admin.site.site_header = 'Lights Control'

urlpatterns = [
    url(r'^(?P<url>.*)/switch/$', switch, name='switch'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', LightListView.as_view(), name='lights'),
    url(r'^(?P<slug>[-\w]+)/$', LightDetailView.as_view(), name='light-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_PATH,
                          document_root=settings.MEDIA_ROOT)

channel_routing = [
    routing_include('lights.urls.websocket_routing', path=r'^/lights/stream'),
]
