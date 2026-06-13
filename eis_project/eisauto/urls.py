from django.urls import path

from eis_project.eisauto.views import (
    HomeView,
    GalleryView,
    AboutView,
    ServicesView,
    PricesView,
    ContactsView,
    gallery_more,
)

urlpatterns = [
    path('',               HomeView.as_view(),     name="home_page"),
    path('about/',         AboutView.as_view(),    name="about"),
    path('services/',      ServicesView.as_view(), name="services"),
    path('prices/',        PricesView.as_view(),   name="prices"),
    path('gallery/',       GalleryView.as_view(),  name="gallery"),
    path('gallery/more/',  gallery_more,           name="gallery_more"),
    path('contacts/',      ContactsView.as_view(), name="contacts"),
]
