from django.contrib.auth.decorators import user_passes_test

from main.models import TestModel

from main.forms import TestModelForm

from .helpers import (
    generic_list,
    generic_add_object,
    generic_edit_object,
    generic_delete_object,
)


class TestView:
    @staticmethod
    @user_passes_test(lambda user: user.has_perm("main.view_modeltest"))
    def list(request):
        fields = [
            "name",
            "is_active",
            "created_at",
            "updated_at",
        ]
        field_labels = ["Name", "Is Active", None, "Updated At"]
        queryset = TestModel.objects.filter(is_active=True)
        return generic_list(
            request,
            "Test Model",
            queryset,
            fields,
            field_labels,
            None,
            "main:test_model_add",
            "main:test_model_edit",
            "main:test_model_delete",
            "modeltest",
            {
                "Action": {"reverse_url": "main:test_model_edit", "text": "Action Text"},
                "Another Action": {
                    "reverse_url": "main:test_model_delete",
                    "favicon_class": "fas fa-trash text-danger",
                },
            },
        )

    @staticmethod
    @user_passes_test(lambda user: user.has_perm("main.add_modeltest"))
    def add(request):
        return generic_add_object(
            request,
            "Test Model",
            TestModelForm,
            "main:test_model_list",
        )

    @staticmethod
    @user_passes_test(lambda user: user.has_perm("main.edit_modeltest"))
    def edit(request, pk):
        return generic_edit_object(
            request, "Test Model", TestModel, pk, TestModelForm, "main:test_model_list"
        )

    @staticmethod
    @user_passes_test(lambda user: user.has_perm("main.delete_modeltest"))
    def delete(request, pk):
        return generic_delete_object(request, TestModel, pk, "main:test_model_list")
