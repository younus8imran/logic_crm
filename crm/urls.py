from django.urls import path
from .views import (
    get_client, CreateClient, get_chain_marketing, 
    get_client_list, save_sales_dump, save_marketing_plan, 
    get_plan_list, ProductAPIView, PaymentDetailsView
)


urlpatterns = [
    path('master_data/', get_client, name='marketing-filter'),
    path('create_campaign/', CreateClient.as_view(), name='marketing-existence-check'),
    path('client/client_list/', get_client_list, name="client-list"),
    path('marketing/chain/', get_chain_marketing, name="generate marketing code"),
    path('dump/', save_sales_dump, name='save-sales-dump'),
    path('save_plan/', save_marketing_plan, name="save campaign marketing code in table"),
    path('plan_list/', get_plan_list, name="get list of generated campaign marketing code"),
    path('products/', ProductAPIView.as_view(), name='product with price'),
    path('payments/', PaymentDetailsView.as_view(), name='payment-details'),
]
