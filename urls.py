from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from aidsbank.views import CentreListView, AidListView, AidDetailView, ApplicantProfileView, ApplicantProfileFormView
from aidsbank.views import ApplicantRequestCreateView, LoanRequestListMangerView, LoanRequestUpdateStatusMangerView
from aidsbank.views import LoanRequestRejectedListMangerView, LoanRequestAcceptedListMangerView, LoanRequestEditMangerView, LoanRequestReadyListMangerView, LoanRequestDeliveredListMangerView, AssetCreateMangerView, AssetListMangerView, MovementCreateManagerView, MovementHistoryListManagerView, AssetUpdateManagerView, AssetCommentCreateMangerView, AssetCommentListMangerView, AssetCommentDeleteMangerView, AssetCommentPublishedListMangerView, AssetCommentApproveMangerView

urlpatterns = patterns('pages.views',

  url(r'^centri/?$', CentreListView.as_view(), name='centre_list'),
  url(r'^ausili/?$', AidListView.as_view(), name='aid_list'),
  url(r'^ausili/cespiti/movimento/(?P<pk>[0-9]+)/?$', MovementCreateManagerView.as_view(), name='movement_create_manager'),
  url(r'^ausili/cespiti/movimenti/storia/(?P<pk>[0-9]+)/?$', MovementHistoryListManagerView.as_view(), name='movement_history'),
  url(r'^ausili/cespiti/modifica/(?P<pk>[0-9]+)/?$', AssetUpdateManagerView.as_view(), name='asset_edit_manager'),
  url(r'^ausili/cespiti/carica/?$', AssetCreateMangerView.as_view(), name='asset_create_manager'),
  url(r'^ausili/cespiti/lista/?$', AssetListMangerView.as_view(), name='asset_list_manager'),
  url(r'^ausili/cespiti/commenti/pubblicati?$', AssetCommentPublishedListMangerView.as_view(), name='asset_comment_published_list_manager'),
  url(r'^ausili/cespiti/commenti/?$', AssetCommentListMangerView.as_view(), name='asset_comment_list_manager'),
  url(r'^ausili/cespiti/commenti/elimina/(?P<pk>[0-9]+)/?$', AssetCommentDeleteMangerView.as_view(), name='asset_comment_delete_manager'),
  url(r'^ausili/cespiti/commenti/approva/(?P<pk>[0-9]+)/?$', AssetCommentApproveMangerView.as_view(), name='asset_comment_approve_manager'),
  url(r'^ausili/richieste/?$', LoanRequestListMangerView.as_view(), name='loan_request_list_manager'),
  url(r'^ausili/richieste/rifiutate/?$', LoanRequestRejectedListMangerView.as_view(), name='loan_request_list_rejected_manager'),
  url(r'^ausili/pratiche/aperte/?$', LoanRequestAcceptedListMangerView.as_view(), name='loan_request_list_accepted_manager'),
  url(r'^ausili/pratiche/prontaconsegna/?$', LoanRequestReadyListMangerView.as_view(), name='loan_request_list_ready_manager'),
  url(r'^ausili/pratiche/consegnate/?$', LoanRequestDeliveredListMangerView.as_view(), name='loan_request_list_delivered_manager'),
  url(r'^ausili/pratica/modifica/(?P<pk>[0-9]+)/?$', LoanRequestEditMangerView.as_view(), name='loan_edit_manager'),
  url(r'^ausili/richieste/update/(?P<pk>[0-9]+)/(?P<status>[0-9]+)/?$', LoanRequestUpdateStatusMangerView.as_view(), name='loan_request_update_status_manager'),
  url(r'^ausili/(?P<slug>[-_\w]+)/?$', AidDetailView.as_view(), name='aid_detail'),
  url(r'^richiedente/profilo/?$', login_required(ApplicantProfileView.as_view()), name='applicant_profile'),
  url(r'^richiedente/profilo/modifica/?$', login_required(ApplicantProfileFormView.as_view()), name='applicant_profile_form'),
  url(r'^richiedente/ausili/commenta/(?P<pk>[0-9]+)?$', AssetCommentCreateMangerView.as_view(), name='applicant_asset_comment_form'),
  url(r'^cespite/richiesta/(?P<id>[\d]+)/?$', ApplicantRequestCreateView.as_view(), name='asset_request'),

)
