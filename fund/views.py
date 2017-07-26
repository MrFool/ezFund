from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import _user_has_perm
from django.contrib.auth.decorators import login_required

from .models import Fund


@login_required(login_url='/admin/')
def index(request):
    fund_list = Fund.objects.all()
    context = {
        'username': request.user.username,
        'fund_list': fund_list,
    }
    return render(request, 'index.html', context)


@login_required(login_url='/admin/')
def detail(request, fund_id):
    fund = get_object_or_404(Fund, pk=fund_id)
    content = {
        'username': request.user.username,
        'fund': fund,
        'fund_stat': fund.fund_status(),
    }
    return render(request, 'detail.html', content)


def approve(request, fund_id):
    if _user_has_perm(perm="student_approve"):
        app_fund = get_object_or_404(Fund, pk=fund_id)
        app_fund.is_accepted_by_student = True
        app_fund.save()
    else:
        if _user_has_perm(perm="teacher_approve"):
            app_fund = get_object_or_404(Fund, pk=fund_id)
            app_fund.is_accepted_by_teacher = True
            app_fund.save()
    return detail(request, fund_id)



