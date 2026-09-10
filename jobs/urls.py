from django.urls import path

from . import views

urlpatterns = [
    path('', views.JoblistView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job_create'),
    path('jobs/<int:pk>/update/', views.JobUpdateView.as_view(), name='job_update'),
    path('jobs/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),
    path('my-jobs/', views.MyJobListView.as_view(), name='my_job_list'),
    path('jobs/<int:pk>/apply/', views.apply_to_job, name='apply_to_job'),
    path('my-applications/', views.MyApplicationListView.as_view(), name='my_application_list'),
]
