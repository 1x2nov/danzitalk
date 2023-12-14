from django.urls import path
from community import views
from .views import Search, ToggleBookmark
urlpatterns = [
    path('search', Search.as_view()),
    path('<int:reality_id>/bookmark', ToggleBookmark.as_view()),
]