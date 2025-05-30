import csv
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


def generic_delete_object(
    request, model_class, pk, reverse_url, reverse_url_kwargs={}, alert_action=True
):
    """Call when deleting corresponding object url is being created

    Args:
        request (request): django request object
        model_class (django.Modal): modal class for which object will be deleted as class instance
        pk (pk): primary key for which the object will be deleted
        reverse_url (str): reverse url name for the view that needs to be rendered
        reverse_url_kwargs (dict, optional): kwargs for the reverse url. Defaults to {}.
        alert_action (bool, optional): should message alert be sent on action completion. Defaults to True.

    Returns:
        _type_: redirects to the reverse url
    """
    instance = get_object_or_404(model_class, pk=pk)
    try:
        instance.delete()
        return HttpResponseRedirect(reverse(reverse_url, kwargs=reverse_url_kwargs))
    except ProtectedError:
        if alert_action:
            messages.add_message(
                request,
                messages.WARNING,
                f"Error! Failed to delete Object ID: {instance}. First remove related items.",
            )
        return HttpResponseRedirect(reverse(reverse_url, kwargs=reverse_url_kwargs))
    except:
        if alert_action:
            messages.add_message(
                request,
                messages.WARNING,
                f"Error! Failed to delete Object ID: {instance}. Something went wrong.",
            )
        return HttpResponseRedirect(reverse(reverse_url, kwargs=reverse_url_kwargs))


def generic_add_object(
    request,
    heading,
    form_class,
    reverse_url,
    form_kwargs={},
    reverse_url_kwargs={},
    extra_context={},
    template_name="generic/form.html",
    alert_action=True,
):
    if request.method == "POST":
        form = form_class(request.POST, request.FILES, user=request.user, **form_kwargs)
        if form.is_valid():
            instance = form.save()
            if alert_action:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"Success! Object ID: {instance} created successfully.",
                )
            return HttpResponseRedirect(reverse(reverse_url, kwargs=reverse_url_kwargs))
    else:
        form = form_class(user=request.user, **form_kwargs)
    extend_template_name = (
        "base/base-sbadmin2.html"
        if request.user.render_sbadmin2_ui
        else "base/base.html"
    )
    return render(
        request,
        template_name,
        {
            "form": form,
            "heading": heading,
            "extend_template_name": extend_template_name,
            **extra_context,
        },
    )


def generic_edit_object(
    request,
    heading,
    model_class,
    pk,
    form_class,
    reverse_url,
    extra_context={},
    form_kwargs={},
    reverse_url_kwargs={},
    instance=None,
    template_name="generic/form.html",
    alert_action=False,
):
    instance = instance or get_object_or_404(model_class, pk=pk)
    if request.method == "POST":
        form = form_class(
            request.POST,
            request.FILES,
            instance=instance,
            user=request.user,
            **form_kwargs,
        )
        if form.is_valid():
            instance = form.save()
            if alert_action:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"Success! Object ID: {instance} created successfully.",
                )
            return HttpResponseRedirect(reverse(reverse_url, kwargs=reverse_url_kwargs))
    else:
        form = form_class(instance=instance, user=request.user, **form_kwargs)
    extend_template_name = (
        "base/base-sbadmin2.html"
        if request.user.render_sbadmin2_ui
        else "base/base.html"
    )
    return render(
        request,
        template_name,
        {
            "form": form,
            "heading": heading,
            "extend_template_name": extend_template_name,
            **extra_context,
        },
    )


def get_field(instance, field):
    field_path = field.split("__")
    attr = instance
    for elem in field_path:
        try:
            attr = getattr(attr, elem)
        except AttributeError:
            return None
    return attr


def paginate_queryset(request, queryset, fields, search_field="pk__icontains"):
    search = request.GET.get("search", None)
    if search and search_field:
        queryset = queryset.filter(**{search_field: search})
    page_length = request.GET.get("page_length", 25)
    if page_length == "MAX":
        return None, queryset.values_list(*fields)
    page_number = int(request.GET.get("page", 1))
    p = Paginator(queryset, page_length)
    qs = []
    page_number = max(0, page_number)
    page_number = min(p.num_pages, page_number)
    page = p.page(page_number)
    for element in p.page(page_number):
        if isinstance(element, tuple):
            element_data = element
        if isinstance(element, dict):
            element_data = []
            for field in fields:
                element_data.append(element.get(field, None))
        else:  # Type == MODEL
            element_data = []
            for field in fields:
                element_data.append(get_field(element, field))
        qs.append(element_data)
    return page, qs


def apply_functions(arr, index_to_func):
    # Adding 1 here since we have appended pk at 0 manually
    temp = list(arr)
    for index, func in index_to_func.items():
        temp[index + 1] = func(temp[index + 1])
    return temp


def generate_export_data_response(data, filename):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
    writer = csv.writer(response)
    writer.writerow(data["fields"])
    for row in data["data"]:
        writer.writerow(row)
    return response


def remove_non_label_field_data(arr, field_labels):
    return [x for i, x in enumerate(arr) if field_labels[i] != None]


def generic_list(
    request,
    heading,
    queryset,
    fields,  # pk is automatically added to the same
    field_labels,  # Doesn't render skipped labels
    view_url,
    add_url,
    edit_url,
    delete_url,
    model_name_lowercase_no_space,
    action_urls,
    extra_context={},
    search_field="pk__icontains",
    search_field_label="ID",
    data_transform_functions_mapping_with_index={},  # 0 based index and corresponding function
    filter_form=None,
    template_name="generic/list.html",
):
    if len(fields) != len(field_labels):
        raise AttributeError(
            "Fields and labels should be of same length in generic_list"
        )

    view_perm = request.user.has_perm(f"main.view_{model_name_lowercase_no_space}")
    add_perm = request.user.has_perm(f"main.add_{model_name_lowercase_no_space}")
    edit_perm = request.user.has_perm(f"main.edit_{model_name_lowercase_no_space}")
    delete_perm = request.user.has_perm(f"main.delete_{model_name_lowercase_no_space}")

    fields.insert(0, "pk")
    field_labels.insert(0, "pk")

    page_obj, qs = paginate_queryset(request, queryset, fields, search_field)

    view_url = view_url or None if view_perm else None
    add_url = add_url or None if add_perm else None
    edit_url = edit_url or None if edit_perm else None
    delete_url = delete_url or None if delete_perm else None

    # Should have object of form action_name(example: "Edit"):
    # dict(reverse_url(required), reverse_url_kwargs(optional), favicon_class or text)
    # Example actions can be edit, delete, print, approve etc..
    action_urls = action_urls or {}

    fields_render = [label for label in field_labels if label != None]
    if edit_url:
        fields_render += ["Edit"]
    if delete_url:
        fields_render += ["Delete"]

    tableData = {
        "data": [
            remove_non_label_field_data(
                apply_functions(instance, data_transform_functions_mapping_with_index),
                field_labels,
            )
            for instance in qs
        ],
        "fields": fields_render + list(action_urls.keys()),
    }

    if request.GET.get("export"):
        return generate_export_data_response(tableData, f"{heading}_data.csv")

    extend_template_name = (
        "base/base-sbadmin2.html"
        if request.user.render_sbadmin2_ui
        else "base/base.html"
    )

    return render(
        request,
        template_name,
        {
            "heading": heading,
            "table": tableData,
            "view_url": view_url,
            "add_url": add_url,
            "edit_url": edit_url,
            "delete_url": delete_url,
            "action_urls": action_urls,
            "page_obj": page_obj,
            "search_value": request.GET.get("search", None),
            "search_field_label": search_field_label,
            "filter_form": filter_form,
            "extend_template_name": extend_template_name,
            **extra_context,
        },
    )
