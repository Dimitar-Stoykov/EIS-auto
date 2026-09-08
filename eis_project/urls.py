from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from eis_project.eisauto.views import stream_media, robots_txt
from eis_project.eisauto.sitemaps import StaticViewSitemap, ServicePageSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'services': ServicePageSitemap,
}

urlpatterns = [
    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),

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

# Serve uploaded media files (gallery/price images, video) with Range
# request support, needed for video seeking. Always on — there's no
# separate web server (nginx/whitenoise) in front handling this, whether
# running locally or deployed, so gating it behind DEBUG just breaks every
# image on the site once DEBUG=False (which is exactly what happened).
urlpatterns += [path('media/<path:path>', stream_media)]

