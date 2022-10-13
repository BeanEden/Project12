from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path

# from epic_event.views import SignUpView
from epic_event.views.user_view import UserListView, UserCreateDetailView, UserDetailView
from epic_event.views.customer_view import CustomerListView, MyCustomerList, UserCustomerList, customer_detail_view, customer_create_view
from epic_event.views.contract_view import ContractListView, CustomerContractListView, MyContractListView, UserContractListView, contract_create_view,contract_detail_view
from epic_event.views.event_view import EventListView, CustomerEventListView, MyEventListView,UserEventListView, UnassignedEventListView, event_create_view, event_detail_view, contract_event_detail_view
import epic_event.views
from epic_event.views.general_view import GlobalFeed
from authentication.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),


    # -------------------------AUTHENTICATION PAGES-------------------------#

    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', LogoutView.as_view(),
         name='logout'),
    # path('signup/', SignUpView.as_view(),
    #      name='signup'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
        name='password_change'),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
        name='password_change_done'),
    # --------------------------HOME AND USER PAGES--------------------------#

    path('home/', GlobalFeed.as_view(), name='home'),
    # path('event_list/', epic_event.views.EventListView.as_view(), name='event_list'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('user_create/', SignUpView.as_view(), name='user_create'),
    path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),

    path('customer_list/', CustomerListView.as_view(), name='customer_list'),
    path('customer_create/', customer_create_view, name="customer_create"),
    path('<int:customer_id>/customer_detail/', customer_detail_view,
         name="customer_detail"),
    path('<int:user_id>/customer_list/', UserCustomerList.as_view(), name='user_customer_list'),
    path('my_customer_list/', MyCustomerList.as_view(), name='my_customer_list'),

    path('contract_list/', ContractListView.as_view(), name='contract_list'),
    path('<int:user_id>/user_contract_list/', UserContractListView.as_view(), name='user_contract_list'),
    path('my_contract_list/', MyContractListView.as_view(),  name='my_contract_list'),
    path('<int:customer_id>/customer_contract_list/', CustomerContractListView.as_view(), name='customer_contract_list'),


    path('<int:customer_id>/contract_create/', contract_create_view,
             name='contract_create'),
    path('<int:contract_id>/contract_detail/', contract_detail_view, name='contract_detail'),


    path('event_list/', EventListView.as_view(), name = 'event_list'),
    path('<int:user_id>/user_event_list/',UserEventListView.as_view(), name='user_event_list'),
    path('my_event_list/', MyEventListView.as_view(), name='my_event_list'),
    path('unassigned_event_list/', UnassignedEventListView.as_view(), name='unassigned_event_list'),
    path('<int:customer_id>/event_list/', CustomerEventListView.as_view(), name='customer_event_list'),


    path('<int:contract_id>/event_create/', event_create_view, name='event_create'),
    path('<int:event_id>/event_detail/', event_detail_view, name='event_detail'),
    path('<int:contract_id>/event_detail/', contract_event_detail_view, name='contract_event_detail')
    ]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)