from django.urls import path

from api.v1.student import views

urlpatterns = [
    # Student Api
    path('list/', views.StudentListCreateView.as_view(), name='student-list'),
    path('create/', views.StudentListCreateView.as_view(), name='student-create'),
    path('detail/<int:pk>/', views.StudentDetailUpdateDeleteView.as_view(), name='student-detail'),
    path('update/<int:pk>/', views.StudentDetailUpdateDeleteView.as_view(), name='student-update'),
    path('delete/<int:pk>/', views.StudentDetailUpdateDeleteView.as_view(), name='student-delete'),

    # University api
    path('university/', views.UniversityListCreateView.as_view(), name='university-list-create'),
    path('university/<int:pk>/', views.UniversityDetailUpdateDeleteView.as_view(), name='university-dud'),
]
