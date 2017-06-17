"""AplikacjeWWW2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
import elections.views
from rest_framework.authtoken import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url="/static/index.html")),
    url(r'^login/', RedirectView.as_view(url="/static/login.html")),
    url(r'^signup/', RedirectView.as_view(url="/static/signup.html")),
    url(r'^search/', RedirectView.as_view(url="/static/search.html")),

    url(r'^api/kandydaci/Obwód(0)?(?P<arg>.*)', elections.views.get_candidates_info),
    url(r'^api/kandydaci/(?P<arg>.*)', elections.views.get_candidates_info),
    url(r'^api/zbiorcze/Obwód(0)?(?P<arg>.*)', elections.views.get_general_info),
    url(r'^api/zbiorcze/(?P<arg>.*)', elections.views.get_general_info),
    url(r'^api/szczegolowe/Obwód(0)?(?P<arg>.*)', elections.views.get_detailed_info),
    url(r'^api/szczegolowe/(?P<arg>.*)', elections.views.get_detailed_info),
    url(r'^api/search/(?P<arg>.*)', elections.views.get_search_results),

    url(r'^api/signup', elections.views.process_signup),
    url(r'^api/login', elections.views.process_login),
    url(r'^api/update', elections.views.update_community),

    url(r'^admin/', admin.site.urls),
    url(r'^api/get-token', views.obtain_auth_token)
]
