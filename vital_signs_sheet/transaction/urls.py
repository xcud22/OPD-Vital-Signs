from django.urls import path
from . import views

app_name = 'transaction'

urlpatterns = [
    path('create/', views.create_transaction, name='create_transaction'),
    path('list/', views.transaction_list, name='transaction_list'),
    path('export_pdf/<uuid:transaction_id>/', views.export_pdf, name='export_pdf'),
]