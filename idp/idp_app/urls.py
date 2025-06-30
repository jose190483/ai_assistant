from django.urls import path
from . import views
urlpatterns = [
    path('search_keywords', views.search_keywords, name='search_keywords'),
    path('manage_pdfs/', views.manage_pdfs, name='manage_pdfs'),
]