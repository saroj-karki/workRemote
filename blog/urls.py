from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView, 
    UserPostListView, 
    JobApplyView, 
    DashboardView, 
    JobSearchView,
    ApplicantDetailView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/job_apply/', JobApplyView.as_view(), name='job-apply'),
    path('post/<int:pk>/job_dashboard/', DashboardView.as_view(), name='job-dashboard'),
    path('post/<int:pk>/job_dashboard/applicant_detail/<int:sno>/', ApplicantDetailView.as_view(), name='applicant-detail'),

    path('post/<int:pk>/job_dashboard/<int:sno>/delete', views.job_applicant_delete, name='applicant-delete'),
    path('post/<int:pk>/job_dashboard/applicant_detail/<int:sno>/delete/', views.job_applicant_delete, name='applicant-delete2'),
    path('post/<int:pk>/job_dashboard/applicant_detail/<int:sno>/approve/', views.job_applicant_approve, name='applicant-approve'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('search/', JobSearchView.as_view(), name='job-search'),
    path('about/', views.about, name='blog-about'),

]