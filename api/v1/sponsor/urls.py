from django.urls import path

from api.v1.sponsor import views

urlpatterns = [
    # for sponsor model
    path('list/', views.SponsorListCreateView.as_view(), name='sponsor-list'),
    path('create/', views.SponsorListCreateView.as_view(), name='sponsor-create'),
    path('detail/<int:pk>/', views.SponsorDetailUpdateDeleteView.as_view(), name='sponsor-detail'),
    path('update/<int:pk>/', views.SponsorDetailUpdateDeleteView.as_view(), name='sponsor-update'),
    path('delete/<int:pk>/', views.SponsorDetailUpdateDeleteView.as_view(), name='sponsor-delete'),

    # for sponsorship model
    path('sponsorship/list/', views.SponsorshipListCreateView.as_view(), name='sponsorship-list'),
    path('sponsorship/create/', views.SponsorshipListCreateView.as_view(), name='sponsorship-create'),
    path('sponsorship/detail/<int:pk>/', views.SponsorDetailUpdateDeleteView.as_view(), name='sponsorship-detail'),
    path('sponsorship/update/<int:pk>/', views.SponsorDetailUpdateDeleteView.as_view(), name='sponsorship-update'),
    path('sponsorship/delete/<int:pk>/', views.SponsorDetailUpdateDeleteView.as_view(), name='sponsorship-delete'),
]
