"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import *
from . import view,testdb
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^test$', testdb.testdb),
    url(r'^$', view.ChangeHP),    
    url(r'^TurnToIndex2$', view.ChangeHP2),
    url(r'^TurnToIndex1$', view.ChangeHP),
    url(r'^search_FID$', view.search_by_ID),
    url(r'^search_FFT$', view.search_by_FT),
    url(r'^admin/', view.admin),
    url(r'^admin_login$', view.admin_login),

    url(r'^SendCode$',view.send_by_app),
    url(r'^Register$',view.register_by_app),
    url(r'^Login$',view.login_by_app),
    url(r'^Search$',view.search_app),
    url(r'^Marked$',view.marked_by_app),
    url(r'^SearchMarked$',view.search_marked_app),

    #url(r'^query_help$', view.query_help),
]
