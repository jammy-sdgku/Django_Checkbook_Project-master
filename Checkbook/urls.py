from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('create/', views.create_account, name='create'),
     path('balance/<int:pk>/', views.balance, name='balance'),
    path('balance2/<int:pk>/', views.balance2, name='balance2'),
    path('transaction/', views.transaction, name='transaction'),
    path('transaction/<int:pk>/update/', views.update_transaction, name='updateTransaction'),
    path('transaction/<int:pk>/delete/', views.delete_transaction, name='deleteTransaction'),
    path('account/<int:pk>/delete/', views.delete_account, name='deleteAccount'),
    path('account/<int:pk>/update/', views.update_account, name='updateAccount'),
]
