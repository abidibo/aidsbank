from django import template
from django.contrib.auth.models import Group, Permission
from aidsbank.forms import UserAuthenticationForm
from aidsbank.models import Applicant, Manager, Loan, AssetComment
from django.conf import settings

register = template.Library()

@register.inclusion_tag('aidsbank/profile_box.html', takes_context=True)
def profile_box(context, next = None):
    user = context['user']
    if user.groups.filter(name=settings.BANCOAUSILI_APPLICANT_GROUP).count():
        applicant = Applicant.objects.get(user=user)
        manager = None
    elif user.groups.filter(name=settings.BANCOAUSILI_MANAGER_GROUP).count():
        applicant = None
        manager = None
    else:
        applicant = None
        manager = None

    return {'applicant': applicant, 'manager': manager, 'user': user, 'authenticated': context['user'].is_authenticated()}

@register.inclusion_tag('aidsbank/manager_menu.html', takes_context=True)
def manager_menu(context):
    user = context['user']
    can_change_loan = user.has_perm('aidsbank.change_loan')
    manager_group = Group.objects.get(name=settings.BANCOAUSILI_MANAGER_GROUP)
    if manager_group in user.groups.all():
        manager = Manager.objects.get(user=user)
        request_status_0_num = Loan.objects.filter(asset__centre__in=manager.centres.all(), status=0).count()
        request_status_1_num = Loan.objects.filter(asset__centre__in=manager.centres.all(), status=1).count()
        request_status_2_num = Loan.objects.filter(asset__centre__in=manager.centres.all(), status=2).count()
        request_status_3_num = Loan.objects.filter(asset__centre__in=manager.centres.all(), status=3).count()
        request_status_4_num = Loan.objects.filter(asset__centre__in=manager.centres.all(), status=4).count()
        comments_to_be_approved_num = AssetComment.objects.filter(asset__centre__in=manager.centres.all(), published=False).count()
        comments_approved_num = AssetComment.objects.filter(asset__centre__in=manager.centres.all(), published=True).count()
    else:
        return {'manager': None}

    return {
        'manager': manager, 
        'request_status_0_num':request_status_0_num, 
        'request_status_1_num':request_status_1_num, 
        'request_status_2_num':request_status_2_num, 
        'request_status_3_num':request_status_3_num, 
        'request_status_4_num':request_status_4_num, 
        'comments_to_be_approved_num':comments_to_be_approved_num, 
        'comments_approved_num':comments_approved_num, 
        'can_change_loan': can_change_loan
    }

@register.inclusion_tag('aidsbank/login_box.html', takes_context=True)
def login_box(context, next = None):
    return {'title': 'Accedi', 'form': UserAuthenticationForm, 'next': next, 'authenticated': context['user'].is_authenticated()}

@register.filter(name='is_manager')
def is_manager(user):
    manager_group = Group.objects.get(name=settings.BANCOAUSILI_MANAGER_GROUP)
    return True if manager_group in user.groups.all() else False

@register.filter(name='is_applicant')
def is_applicant(user):
    applicant_group = Group.objects.get(name=settings.BANCOAUSILI_APPLICANT_GROUP)
    return True if applicant_group in user.groups.all() else False

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
