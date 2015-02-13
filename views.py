from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View, ListView, DetailView, FormView, UpdateView, CreateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
#from registration.views import RegistrationView
from registration.backends.default.views import RegistrationView
from aidsbank.models import Centre, Aid, Applicant, Asset, Loan, Manager, Movement, AssetComment
from aidsbank.forms import UserRegistrationForm, ApplicantProfileForm, AssetRequestForm, LoanEditManagerForm, AssetCreateManagerForm, MovementCreateManagerForm, AssetForm, AssetCommentCreateManagerForm, AssetCommentApproveManagerForm

import datetime

"""
Cenres list
"""
class CentreListView(ListView):
    model = Centre

"""
Aids list
"""
class AidListView(ListView):
    model = Aid

"""
Aid detail
"""
class AidDetailView(DetailView):
    model = Aid

    def get_context_data(self, **kwargs):
        context = super(AidDetailView, self).get_context_data(**kwargs)
        if self.request.user.has_perm('aidsbank.view_asset_loan_unavailable'):
            assets = Asset.objects.filter(aid=self.object)
        else:
            assets = Asset.objects.filter(aid=self.object, loan_available=True)

        context['assets'] = assets

        return context

"""
Applicant profile
"""
class ApplicantProfileView(DetailView):
    model = Applicant
    template_name = 'aidsbank/applicant_profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Applicant, user=self.request.user)

"""
Applicant profile form edit
"""
class ApplicantProfileFormView(UpdateView):
    form_class = ApplicantProfileForm
    template_name = 'aidsbank/applicant_profile_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Applicant, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ApplicantProfileFormView, self).get_context_data(**kwargs)
        applicant = get_object_or_404(Applicant, user=self.request.user)
        context['applicant'] = applicant

        return context

"""
Asset request
"""
class ApplicantRequestCreateView(FormView):
    form_class = AssetRequestForm
    template_name = 'aidsbank/asset_request_form.html'

    @method_decorator(permission_required('aidsbank.send_asset_request'))
    def dispatch(self, *args, **kwargs):
        self.asset_id = kwargs['id']
        return super(ApplicantRequestCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        applicant = get_object_or_404(Applicant, user=self.request.user)
        return applicant.get_absolute_url()

    def form_valid(self, form):
        reservation_date = datetime.datetime.now()
        applicant = get_object_or_404(Applicant, user=self.request.user)
        asset = get_object_or_404(Asset, pk=self.asset_id)

        loan = Loan.objects.create(applicant=applicant, asset=asset, reservation_date=reservation_date, status=1)

        managers = Manager.objects.filter(centres__in=[asset.centre], user__is_active=True)
        mail_subject = render_to_string('aidsbank/request_email_subject.txt', {'asset': asset}).replace("\n", "")
        mail_object = render_to_string('aidsbank/request_email_object.txt', {'asset': asset, 'applicant': applicant})

        emails = []
        for manager in managers:
            emails.append(manager.user.email)

        send_mail(mail_subject, mail_object, 'no-reply@bancoausili.it', emails)

        return super(ApplicantRequestCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicantRequestCreateView, self).get_context_data(**kwargs)
        applicant = get_object_or_404(Applicant, user=self.request.user)
        asset = get_object_or_404(Asset, pk=self.asset_id)
        context['applicant'] = applicant
        context['asset'] = asset

        return context

"""
User registration
"""
class UserRegistrationView(RegistrationView):
    form_class = UserRegistrationForm
    success_url = '/'

    def register(self, request, **cleaned_data):

        user = super(UserRegistrationView, self).register(request, **cleaned_data)

        user.first_name = cleaned_data['firstname']
        user.last_name = cleaned_data['lastname']

        user.save();

        address = cleaned_data['address']
        city = cleaned_data['city']
        cap = cleaned_data['cap']
        province = cleaned_data['province']
        phone = cleaned_data['phone']

        applicant = Applicant.objects.create(user=user, address=address, city=city, cap=cap, province=province, phone=phone)
        applicant.save()

        group = Group.objects.get(name=settings.BANCOAUSILI_APPLICANT_GROUP)
        group.user_set.add(user)

        applicant.save()

        return user

"""
Requests list, manager
"""
class LoanRequestListMangerView(ListView):
    model = Loan
    template_name = 'aidsbank/loan_request_list_manager.html'

    def get_queryset(self):
        return Loan.objects.filter(status=1)

"""
Request acceptance, manager
"""
class LoanRequestUpdateStatusMangerView(SingleObjectMixin, View):
    model = Loan

    @method_decorator(permission_required('aidsbank.change_loan'))
    def dispatch(self, *args, **kwargs):
        self.status = kwargs['status']
        return super(LoanRequestUpdateStatusMangerView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        print request.GET
        self.object = self.get_object()
        self.object.status = self.status
        self.object.save()

        referer = request.META.get('HTTP_REFERER')
        if not referer:
            return 'loan_request_list_manager'

        return redirect(referer)

"""
Requests rejected list, manager
"""
class LoanRequestRejectedListMangerView(ListView):
    model = Loan
    template_name = 'aidsbank/loan_request_rejected_list_manager.html'

    @method_decorator(permission_required('aidsbank.change_loan'))
    def dispatch(self, *args, **kwargs):
        return super(LoanRequestRejectedListMangerView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Loan.objects.filter(status=0)

"""
Requests accepted list, manager
"""
class LoanRequestAcceptedListMangerView(ListView):
    model = Loan
    template_name = 'aidsbank/loan_request_accepted_list_manager.html'

    @method_decorator(permission_required('aidsbank.change_loan'))
    def dispatch(self, *args, **kwargs):
        return super(LoanRequestAcceptedListMangerView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Loan.objects.filter(status=2)

"""
Edit loan, manager
"""
class LoanRequestEditMangerView(UpdateView):
    model = Loan
    form_class = LoanEditManagerForm
    template_name = 'aidsbank/loan_edit_manager.html'

    @method_decorator(permission_required('aidsbank.change_loan'))
    def dispatch(self, *args, **kwargs):
        self.loan_id = kwargs['pk']
        return super(LoanRequestEditMangerView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()
        loan = Loan.objects.get(id=self.loan_id)
        return HttpResponse(render_to_string('aidsbank/loan_edit_manager_success.html', {'loan': loan}))

"""
Requests ready to deliver, manager
"""
class LoanRequestReadyListMangerView(ListView):
    model = Loan
    template_name = 'aidsbank/loan_request_ready_list_manager.html'

    @method_decorator(permission_required('aidsbank.change_loan'))
    def dispatch(self, *args, **kwargs):
        return super(LoanRequestReadyListMangerView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Loan.objects.filter(status=3)

"""
Requests ready to deliver, manager
"""
class LoanRequestDeliveredListMangerView(ListView):
    model = Loan
    template_name = 'aidsbank/loan_request_delivered_list_manager.html'

    @method_decorator(permission_required('aidsbank.change_loan'))
    def dispatch(self, *args, **kwargs):
        return super(LoanRequestDeliveredListMangerView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Loan.objects.filter(status=4)

"""
Asset creation, manager
"""
class AssetCreateMangerView(CreateView):
    model = Asset
    template_name = 'aidsbank/asset_create_manager.html'
    form_class = AssetCreateManagerForm
    success_url = reverse_lazy('asset_list_manager');

    @method_decorator(permission_required('aidsbank.change_asset'))
    def dispatch(self, *args, **kwargs):
        return super(AssetCreateMangerView, self).dispatch(*args, **kwargs)

"""
Assets list, manager
"""
class AssetListMangerView(ListView):
    model = Asset
    template_name = 'aidsbank/asset_list_manager.html'

    @method_decorator(permission_required('aidsbank.change_asset'))
    def dispatch(self, *args, **kwargs):
        return super(AssetListMangerView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        manager_group = Group.objects.get(name=settings.BANCOAUSILI_MANAGER_GROUP)
        if manager_group in user.groups.all():
            manager = Manager.objects.get(user=user)
            return Asset.objects.filter(centre__in=manager.centres.all())
        else:
            return Asset.objects.all()

"""
Asset move, manager
"""
class MovementCreateManagerView(CreateView):
    model = Movement
    form_class = MovementCreateManagerForm
    template_name = 'aidsbank/movement_create_manager.html'

    @method_decorator(permission_required('aidsbank.add_movement', login_url=reverse_lazy('login_ajax')))
    def dispatch(self, *args, **kwargs):
        self.asset_id = kwargs['pk']
        return super(MovementCreateManagerView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MovementCreateManagerView, self).get_context_data(**kwargs)
        asset = get_object_or_404(Asset, pk=self.asset_id)
        context['asset'] = asset

        return context

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        asset = Asset.objects.get(id=self.asset_id)
        manager = Manager.objects.get(user=self.request.user)
        form.instance.manager = manager
        form.instance.asset = asset
        form.save()
        return HttpResponse(render_to_string('aidsbank/movement_create_manager_success.html', {'asset': asset}))

"""
Movements list, manager
"""
class MovementHistoryListManagerView(ListView):
    model = Movement
    template_name = 'aidsbank/movement_history_manager.html'

    @method_decorator(permission_required('aidsbank.add_movement', login_url=reverse_lazy('login_ajax')))
    def dispatch(self, *args, **kwargs):
        self.asset_id = kwargs['pk']
        self.asset = get_object_or_404(Asset, pk=self.asset_id)
        return super(MovementHistoryListManagerView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MovementHistoryListManagerView, self).get_context_data(**kwargs)
        context['asset'] = self.asset

        return context

    def get_queryset(self):
        return Movement.objects.filter(asset=self.asset).order_by('-id')

"""
Asset edit, manager
"""
class AssetUpdateManagerView(UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = 'aidsbank/asset_edit_manager.html'

    @method_decorator(permission_required('aidsbank.change_asset'))
    def dispatch(self, *args, **kwargs):
        self.asset_id = kwargs['pk']
        return super(AssetUpdateManagerView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()
        asset = Asset.objects.get(id=self.asset_id)
        return HttpResponse(render_to_string('aidsbank/asset_edit_manager_success.html', {'asset': asset}))

    def get_context_data(self, **kwargs):
        context = super(AssetUpdateManagerView, self).get_context_data(**kwargs)
        return context

"""
Asset comment creation, applicant
"""
class AssetCommentCreateMangerView(CreateView):
    model = AssetComment
    template_name = 'aidsbank/asset_comment_create_manager.html'
    form_class = AssetCommentCreateManagerForm
    success_url = reverse_lazy('applicant_profile');

    @method_decorator(permission_required('aidsbank.publish_asset_comments'))
    def dispatch(self, *args, **kwargs):
        self.asset_id = kwargs['pk']
        return super(AssetCommentCreateMangerView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        asset = get_object_or_404(Asset, pk=self.asset_id)
        applicant = get_object_or_404(Applicant, user=self.request.user)
        return {
            'asset': asset,
            'applicant': applicant,
            'date': datetime.datetime.now(),
            'published': False
        }

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()
        asset = get_object_or_404(Asset, pk=self.asset_id)
        return HttpResponse(render_to_string('aidsbank/asset_comment_create_manager_success.html', {'asset': asset}))

    def get_context_data(self, **kwargs):
        context = super(AssetCommentCreateMangerView, self).get_context_data(**kwargs)
        asset = get_object_or_404(Asset, pk=self.asset_id)
        context['asset'] = asset

        return context

"""
Assets comment list, manager
"""
class AssetCommentListMangerView(ListView):
    model = AssetComment
    template_name = 'aidsbank/asset_comment_list_manager.html'

    @method_decorator(permission_required('aidsbank.moderate_asset_comments'))
    def dispatch(self, *args, **kwargs):
        return super(AssetCommentListMangerView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        manager_group = Group.objects.get(name=settings.BANCOAUSILI_MANAGER_GROUP)
        if manager_group in user.groups.all():
            manager = Manager.objects.get(user=user)
            return AssetComment.objects.filter(asset__centre__in=manager.centres.all(), published=False)
        else:
            return Asset.objects.all()

"""
Assets comment deletion, manager
"""
class AssetCommentDeleteMangerView(DeleteView):
    model = AssetComment
    template_name = 'aidsbank/asset_comment_confirm_delete.html'

    @method_decorator(permission_required('aidsbank.moderate_asset_comments'))
    def dispatch(self, *args, **kwargs):
        self.comment_id = kwargs['pk']
        return super(AssetCommentDeleteMangerView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(render_to_string('aidsbank/asset_comment_delete_manager_success.html', {}))

    def get_context_data(self, **kwargs):
        context = super(AssetCommentDeleteMangerView, self).get_context_data(**kwargs)
        comment = get_object_or_404(AssetComment, pk=self.comment_id)
        context['comment'] = comment

        return context

"""
Assets comment published list, manager
"""
class AssetCommentPublishedListMangerView(ListView):
    model = AssetComment
    template_name = 'aidsbank/asset_comment_published_list_manager.html'

    @method_decorator(permission_required('aidsbank.moderate_asset_comments'))
    def dispatch(self, *args, **kwargs):
        return super(AssetCommentPublishedListMangerView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        manager_group = Group.objects.get(name=settings.BANCOAUSILI_MANAGER_GROUP)
        if manager_group in user.groups.all():
            manager = Manager.objects.get(user=user)
            return AssetComment.objects.filter(asset__centre__in=manager.centres.all(), published=True)
        else:
            return Asset.objects.all()

"""
Asset comment approval, manager
"""
class AssetCommentApproveMangerView(UpdateView):
    model = AssetComment
    template_name = 'aidsbank/asset_comment_approve_manager.html'
    form_class = AssetCommentApproveManagerForm

    @method_decorator(permission_required('aidsbank.moderate_asset_comments'))
    def dispatch(self, *args, **kwargs):
        self.comment_id = kwargs['pk']
        return super(AssetCommentApproveMangerView, self).dispatch(*args, **kwargs)
    """
    def get_initial(self):
        comment = get_object_or_404(AssetComment, pk=self.comment_id)
        return {
            'asset': comment.asset,
            'applicant': comment.applicant,
            'date': comment.date,
            'published': False
        }
    """
    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.instance.published = True
        form.save()
        comment = AssetComment.objects.get(id=self.comment_id)
        return HttpResponse(render_to_string('aidsbank/asset_comment_approve_manager_success.html', {'comment': comment}))

    def get_context_data(self, **kwargs):
        context = super(AssetCommentApproveMangerView, self).get_context_data(**kwargs)
        comment = get_object_or_404(AssetComment, pk=self.comment_id)
        context['comment'] = comment

        return context
