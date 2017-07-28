from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Fund

from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from operator import itemgetter, attrgetter

from .forms import FundForm, UserForm

from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group


@login_required(login_url='/login/')
def index(request):
    now_user = request.user
    if now_user.has_perm(perm="fund.student_approve"):
        show_add_button = False
        fund_objects = Fund.objects.all()
    else:
        if now_user.has_perm(perm="fund.teacher_approve"):
            show_add_button = False
            ground_list = Fund.objects.filter(is_viewed_by_student=True)
            fund_objects = ground_list.objects.filter(is_objected=False)
        else:
            if now_user.has_perm(perm="fund.apply_only"):
                show_add_button = True
                fund_objects = Fund.objects.all()
    fund_list = sorted(fund_objects, key=attrgetter('id'), reverse=True)
    paginator = Paginator(fund_list,10)
    page = request.GET.get('page')
    try:
        fund_list = paginator.page(page)
    except PageNotAnInteger:
        fund_list = paginator.page(1)
    except EmptyPage:
        fund_list = paginator.page(paginator.num_pages)
    context = {
        'show_add_button': show_add_button,
        'username': request.user.username,
        'fund_list': fund_list,
    }
    return render(request, 'index.html', context)


@login_required(login_url='/login/')
def apply(request):
    if request.method == 'POST':
        form = FundForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = FundForm
    return render(request, 'apply.html', {'form':form})


@login_required(login_url='/login/')
def detail(request, fund_id):
    fund = get_object_or_404(Fund, pk=fund_id)
    content = {
        'username': request.user.username,
        'fund': fund,
        'fund_stat': fund.fund_status(),
    }
    return render(request, 'detail.html', content)


@login_required(login_url='/login/')
def approve(request, fund_id):
    now_user = request.user
    if now_user.has_perm(perm="fund.student_approve"):
        app_fund = get_object_or_404(Fund, pk=fund_id)
        app_fund.is_viewed_by_student = True
        app_fund.save()
    else:
        if now_user.has_perm(perm="fund.teacher_approve"):
            app_fund = get_object_or_404(Fund, pk=fund_id)
            app_fund.is_viewed_by_teacher = True
            app_fund.save()
    return detail(request, fund_id)


@login_required(login_url='/login/')
def deny(request, fund_id):
    now_user = request.user
    if now_user.has_perm(perm="fund.student_approve"):
        app_fund = get_object_or_404(Fund, pk=fund_id)
        app_fund.is_viewed_by_student = True
        app_fund.is_objected = True
        app_fund.save()
    else:
        if now_user.has_perm(perm="fund.teacher_approve"):
            app_fund = get_object_or_404(Fund, pk=fund_id)
            app_fund.is_viewed_by_teacher = True
            app_fund.is_objected = True
            app_fund.save()
    return detail(request, fund_id)


#未来添加双重密码验证注册，以及优化登陆错误细节，比如弄成ajax验证用户名重复,错误
def SignUpView(request):
    if request.method == "POST":
        SignUpForm = UserForm(request.POST)
        if SignUpForm.is_valid():
            username = SignUpForm.cleaned_data['username']
            password = SignUpForm.cleaned_data['password']
            email = SignUpForm.cleaned_data['email']
            if User.objects.filter(username=username):
                return render(request, 'account/failure.html',  {'reason': '用户名已存在，请选择其他用户名'})
            else:
                user = User.objects.create_user(username, email, password)
                user.is_staff = True
                default_group = Group.objects.get(name='student union')
                default_group.user_set.add(user)
                user.save()
                login(request, authenticate(username=username, password=password))
                return HttpResponseRedirect('/fund/')
        else:
            return render(request, 'account/failure.html', {'reason': SignUpForm.errors})
    else:
        SignUpForm = UserForm
        context = {'SignUpForm': SignUpForm}
        return render(request, 'account/sign_up.html', context)


def logoutnlogin(request):
    """
    Logout n login back
    """
    return auth_views.logout_then_login(request,login_url='/login')
