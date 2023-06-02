from django.urls import path
from django.urls import include

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('logout', views.logout_view, name='customlogout'),
    path('accounts/signup', views.signupView, name='signup'),
    path('accounts/reset/done',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_complete.html'),
        name='password_reset_complete'),
    path('analytics/', views.analytics, name='analytics'),
    path('feedback/', views.commentView, name='comment'),
    path('comment_history/', views.comment_history, name='comment_history'),
    path('comment_detail/<comment_id>', views.comment_detail, name='comment_detail'),
    path('email/', views.generate_report, name='email'),
    path('profile/', views.user_profile, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),

]