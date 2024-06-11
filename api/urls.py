from django.urls import path
from . import views
urlpatterns = [
    path('start_scraping/' , views.test_view),
    path('scraping_status/<str:job_id>' , views.scraping_status)
]
