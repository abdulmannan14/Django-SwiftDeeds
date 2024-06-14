import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from register import models as register_models
from . import tables as admin_tables, forms as admin_forms, emails as adminview_emails, models as admin_models


# Create your views here.


def all_verified_users(request):
    queryset = register_models.UserProfile.objects.filter(user__is_staff=False)

    sort = request.GET.get('sort', None)
    filter_form = admin_forms.FilterForm()
    if sort:
        data = queryset.order_by(sort)
    context = {
        "title": "List of Users",
        "page_name": "Users",
        "queryset": [],
        'filter_form': filter_form,
        "table": admin_tables.AllVerifiedUsersTable(
            queryset),
        "header": {
            "links": [
            ],
        },
        "segment": "users",
        'nav_conf': {
            'active_classes': ['admin-settings', ''],
            'collapse_class': '',
        },
        'is_admin': True
    }
    return render(request, "pages/django-tables.html", context)


def all_products(request):
    queryset = admin_models.Products.objects.all()
    sort = request.GET.get('sort', None)
    # filter_form = admin_forms.FilterForm()
    if sort:
        data = queryset.order_by(sort)
    context = {
        "title": "List of Products",
        "page_name": "Products",
        "queryset": [],
        # 'filter_form': filter_form,
        "table": admin_tables.ProductsTableAdmin(queryset),

        "header": {
            "links": [

                # {
                #     "title": "Add",
                #     "href": laboratory_urls.add_laboratories(),
                #     "classes": "btn btn-sm btn-outline-success",
                #     "icon": "fa fa-plus"
                # },
                # {
                #     "title": "Import CSV",
                #     "href": laboratory_urls.import_laboratories(),
                #     "classes": "btn btn-sm btn-outline-primary",
                #     "icon": "fa fa-file-import"
                # },
            ],
        },
        "segment": "products",
        'nav_conf': {
            'active_classes': ['admin-settings', ''],
            'collapse_class': '',
        },
        'is_admin': True
    }
    return render(request, "pages/django-tables.html", context)


@login_required
@csrf_exempt
def resend_email(request, id):
    userprofile = register_models.UserProfile.objects.filter(user_id=id).last()
    resp = adminview_emails.send_email(userprofile, "https://{}".format(request.get_host()), 'resend verification')
    # result_utils.send_sms(result, "https://{}".format(request.get_host()))
    return redirect('admin-dashboard-non-verified-users')
    # if resp.status_code in [202]:
    #     # messages.success(request, "Email Sent!")
    #     return JsonResponse({'success': True, }, safe=False)
    # else:
    #     # messages.error(request, "Email sending error!")
    #     return JsonResponse({'success': False}, safe=False)


def open_orders(request):
    queryset = admin_models.UserProducts.objects.filter(is_completed=False)

    sort = request.GET.get('sort', None)
    if sort:
        data = queryset.order_by(sort)
    context = {
        "title": "List of Orders",
        "page_name": "Orders",
        "queryset": [],
        # 'filter_form': filter_form,
        "table": admin_tables.OpenOrdersAdmin(queryset),

        "header": {
            "links": [

                # {
                #     "title": "Add",
                #     "href": laboratory_urls.add_laboratories(),
                #     "classes": "btn btn-sm btn-outline-success",
                #     "icon": "fa fa-plus"
                # },
                # {
                #     "title": "Import CSV",
                #     "href": laboratory_urls.import_laboratories(),
                #     "classes": "btn btn-sm btn-outline-primary",
                #     "icon": "fa fa-file-import"
                # },
            ],
        },
        "segment": "open_orders",
        'nav_conf': {
            'active_classes': ['admin-settings', ''],
            'collapse_class': '',
        },
        'is_admin': True
    }
    return render(request, "pages/django-tables.html", context)


def fetch_files(request):
    print("=========", request.GET.get('product_id'))
    userproducts = admin_models.UserProducts.objects.filter(id=request.GET.get('product_id')).last()
    if not userproducts:
        return JsonResponse({'files': []}, safe=False)
    files = userproducts.files.all()
    if not files:
        return JsonResponse({'files': []}, safe=False)
    files = [file.file.url for file in files]
    if userproducts.is_completed:
        files = files
        print("files======", files)
    return JsonResponse({'files': files}, safe=False)


def approve_order(request):
    print("userproducts", request.POST.get('product_id'))
    print("thisi si hte file=====", request.FILES.get('file'))
    userproducts = admin_models.UserProducts.objects.get(id=request.POST.get('product_id'))
    print("userproducts", userproducts)
    userproducts.completed_final_file = request.FILES.get('file')
    userproducts.is_completed = True
    userproducts.completed_on = datetime.datetime.now()
    userproducts.save()
    resp = adminview_emails.send_email(userproducts.user.user.email, final=True)
    return JsonResponse({'success': True}, safe=False)


def completed_order(request):
    completed_order = admin_models.UserProducts.objects.filter(is_completed=True)
    context = {
        "title": "List of Completed Orders",
        "page_name": "Completed Orders",
        "queryset": completed_order,
        "table": admin_tables.CompletedProductsTable(completed_order),
        "header": {
            "links": [

            ],
        },
        "segment": "completed_orders",
        # 'nav_conf': {
        #     'active_classes': ['admin-settings', ''],
        #     'collapse_class': '',
        # },
        'is_admin': True
    }
    return render(request, "pages/django-tables.html", context)
