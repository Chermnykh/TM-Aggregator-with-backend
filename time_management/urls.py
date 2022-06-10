from . import views 
from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, TimerView, ChangePasswordView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

#app_name = 'time_management'

urlpatterns = [ 
    path('', views.index, name="home"),

    path('logout/', LogoutView.as_view(next_page='home'), name="logout"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path('profile/', views.subscription, name='profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset"),

    path('methods/', views.methods, name="methods"),

    path('tasks/', TaskList.as_view(), name='tasks'),
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),

    
    path('config/', views.stripe_config, name='config'),
    path('create-checkout-session-personal/', views.create_checkout_session_personal, name='create-checkout-session-personal'),
    path('create-checkout-session-family/', views.create_checkout_session_family, name='create-checkout-session-family'),
    path('create-checkout-session-business/', views.create_checkout_session_business, name='create-checkout-session-business'),
    path('success/', views.success, name='success'), 
    path('cancel/', views.cancel, name='cancel'), 
    path('webhook/', views.stripe_webhook, name='webhook'),

    path('timer/', TimerView.as_view(), name='timer'),
    path('update_timer/', views.update_timer, name='update_timer'),
    path('restart_timer/', views.restart_timer, name='restart_timer')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)