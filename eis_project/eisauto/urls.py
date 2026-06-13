from django.urls import path

from eis_project.eisauto.views import (
    HomeView,
    GalleryView,
    AboutView,
    PricesView,
    ContactsView,
    ServicePageView,
    gallery_more,
)

urlpatterns = [
    path('',                              HomeView.as_view(),        name="home_page"),
    path('about/',                        AboutView.as_view(),       name="about"),
    path('services/<str:service_type>/',  ServicePageView.as_view(), name="service_page"),
    path('prices/',                       PricesView.as_view(),      name="prices"),
    path('gallery/',                      GalleryView.as_view(),     name="gallery"),
    path('gallery/more/',                 gallery_more,              name="gallery_more"),
    path('contacts/',                     ContactsView.as_view(),    name="contacts"),
]
