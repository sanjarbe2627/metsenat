from django.urls import path

from api.v1.sponsor import views

urlpatterns = [
    # for sponsor models
    path('list/', views.SponsorListCreateView.as_view(), name='sponsor-list'),
    path('create/', views.SponsorListCreateView.as_view(), name='sponsor-create'),
    path('detail/<int:pk>/', views.SponsorDetailUpdateDeleteView.as_view(), name='sponsor-detail'),
    path('update/<int:pk>/', views.SponsorDetailUpdateDeleteView.as_view(), name='sponsor-update'),
    path('delete/<int:pk>/', views.SponsorDetailUpdateDeleteView.as_view(), name='sponsor-delete'),
]
