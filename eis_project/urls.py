from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from eis_project.eisauto.views import stream_media

urlpatterns = [
    # Admin "forgot password" flow — must come before admin/ so the admin
    # login page's "Forgotten your password or username?" link resolves.
    # Sends a reset link to the email set on the Django user account
    # (Admin → Users → <user> → Email address), via EMAIL_HOST_USER/.env.
    path(
        'admin/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='admin_password_reset',
    ),
    path(
        'admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path('admin/', admin.site.urls),
    path('', include('eis_project.eisauto.urls')),
]

# Serve uploaded media files with Range request support (needed for video seeking)
if settings.DEBUG:
    urlpatterns += [path('media/<path:path>', stream_media)]

