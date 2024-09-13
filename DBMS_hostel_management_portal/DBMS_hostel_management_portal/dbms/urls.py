from django.contrib import admin
from django.urls import path
from hostel.views import (
    dashboard,
    signin_user,
    register_user,
    booking,
    student_dashboard,
    logout_user
)
from django.contrib.auth import views as auth_views

admin.site.index_title = 'Hostel administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('login/', signin_user, name='login'),
    path('register/', register_user, name='register'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_complete'),
    path('me/', student_dashboard, name='student_dashboard'),
    path('logout/', logout_user, name='logout'),
    path('<hostel_name>/book/', booking, name='book'),
]
