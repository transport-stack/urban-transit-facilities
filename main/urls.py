from django.urls import path

from main.views import TestView

app_name = "main"

urlpatterns = [
    # Test Model URLs
    path("test_model/list/", TestView.list, name="test_model_list"),
    path("test_model/add/", TestView.add, name="test_model_add"),
    path("test_model/edit/<pk>/", TestView.edit, name="test_model_edit"),
    path("test_model/delete/<pk>/", TestView.delete, name="test_model_delete"),
]
