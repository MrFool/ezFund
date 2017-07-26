from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required

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


@permission_required('fund.student_approve')
def stucon_approve(request, fund_id):
    app_fund = get_object_or_404(Fund, pk=fund_id)
    app_fund.is_viewed_by_student = True
    app_fund.save()
    return detail(request, fund_id)


@permission_required('fund.teacher_approve')
def teacher_approve(request, fund_id):
    app_fund = get_object_or_404(Fund, pk=fund_id)
    app_fund.is_viewed_by_teacher = True
    app_fund.save()
    return detail(request, fund_id)


@permission_required('fund.student_approve')
def stucon_deny(request, fund_id):
    app_fund = get_object_or_404(Fund, pk=fund_id)
    app_fund.is_viewed_by_student = True
    app_fund.is_objected = True
    app_fund.save()
    return detail(request, fund_id)


@permission_required('fund.teacher_approve')
def teacher_deny(request, fund_id):
    app_fund = get_object_or_404(Fund, pk=fund_id)
    app_fund.is_viewed_by_teacher = True
    app_fund.is_objected = True
    app_fund.save()
    return detail(request, fund_id)



