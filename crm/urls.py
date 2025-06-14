from django.urls import path
from .views import (
    get_client, CreateClient, get_chain_marketing, 
    get_client_list, save_sales_dump, save_marketing_plan, 
    get_plan_list
)


urlpatterns = [
    path('client/', get_client, name='marketing-filter'),
    path('client/create/', CreateClient.as_view(), name='marketing-existence-check'),
    path('client/client_list/', get_client_list, name="client-list"),
    path('marketing/chain/', get_chain_marketing, name='marketing-existence-check'),
    path('dump/', save_sales_dump, name='save-sales-dump'),
    path('save_plan/', save_marketing_plan, name="save marketing plan into table"),
    path('plan_list/', get_plan_list, name="get list of generated plans")
]
