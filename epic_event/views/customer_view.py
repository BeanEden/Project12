from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated

from epic_event.models.customer import Customer
from epic_event.serializers import CustomerDetailSerializer
from epic_event.views.general_view import PaginatedViewMixin
from epic_event.controller.customer_controller import \
    customer_permission_redirect_read_only, \
    update_customer, \
    delete_customer, \
    create_customer, \
    create_customer_permission_redirect, user_customer_queryset, my_customers_queryset

User = get_user_model()


class CustomerListView(LoginRequiredMixin, APIView, PaginatedViewMixin):

    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/customer_list.html'

    def get(self, request):
        queryset = Customer.objects.all()
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'customers': posts_paged})


class UserCustomerListView(LoginRequiredMixin, APIView, PaginatedViewMixin):

    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/customer_list.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        queryset = user_customer_queryset(user)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'customers': posts_paged})


class MyCustomerListView(LoginRequiredMixin, APIView, PaginatedViewMixin):

    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/customer_list.html'

    def get(self, request):
        queryset = my_customers_queryset(request)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'customers': posts_paged})


@api_view(('GET', 'POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@login_required()
def customer_create_view(request):
    create_customer_permission_redirect(request=request)
    serializer = CustomerDetailSerializer()
    if "create_customer" in request.POST:
        print("post")
        return create_customer(request=request)
    return render(request, 'customer/customer_create.html',
                  context={'serializer': serializer})


@api_view(('GET', 'POST', 'DELETE'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@login_required()
def customer_detail_view(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer_permission_redirect_read_only(request=request, customer=customer)
    serializer = CustomerDetailSerializer(customer)
    if "update_customer" in request.POST:
        return update_customer(request=request, customer=customer)
    if "delete_customer" in request.POST:
        return delete_customer(request=request, customer=customer)
    return render(request, 'customer/customer_detail.html',
                  context={'serializer': serializer, 'customer': customer})
