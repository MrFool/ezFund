from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<fund_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<fund_id>[0-9]+)/approve_by_stu', views.stucon_approve, name='student congress approve'),
    url(r'^(?P<fund_id>[0-9]+)/deny_by_stu', views.stucon_deny, name='student congress deny'),
    url(r'^(?P<fund_id>[0-9]+)/approve_by_tec', views.teacher_approve, name='teacher approve'),
    url(r'^(?P<fund_id>[0-9]+)/deny_by_tec', views.teacher_deny, name='teacher deny'),
]
