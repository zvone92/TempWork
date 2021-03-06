from django.urls import path
from . import views

urlpatterns = [
    path('<int:worker_id>/<slug:slug>', views.worker_details, name='worker_details'),
    path('create_worker/', views.create_worker, name='create_worker'),
    path('worker_profile/', views.worker_profile, name='worker_profile'),
    path('edit_worker_info/', views.edit_worker_info, name='edit_worker_info'),
    path('search/', views.search, name='search'),
]
