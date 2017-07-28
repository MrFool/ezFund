"""ezfund URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles import views
from django.views.static import serve
from django.contrib.auth import views as auth_views
from fund import views as fund_views

urlpatterns = [
    url(r'^fund/', include('fund.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^upload/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^login/', auth_views.login, {'template_name': 'account/sign_in.html'},name='login'),
    url(r'logout_to_login/$', fund_views.logoutnlogin),
    url(r'^password_change/$', auth_views.password_change, {'template_name': 'account/password_change_form.html','post_change_redirect': 
'/fund/?pwd=1'}, name='password_change'),
    url(r'^password_chang_done/$', auth_views.password_change_done,{'template_name': 'account/password_change_done.html'}, name='password_change_done'),
    url(r'sign_up/$', fund_views.SignUpView, name='sign_up'),
]
#password_change可以修改重定向到主页然后加一点JS特效提醒修改成功


if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
