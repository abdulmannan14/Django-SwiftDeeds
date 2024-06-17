from datetime import datetime
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from register import models as register_models
from . import tables as admin_tables, forms as admin_forms, emails as adminview_emails, models as admin_models

import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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
    userproduct = admin_models.UserProducts.objects.filter(id=request.GET.get('product_id')).last()
    if not userproduct:
        return JsonResponse({'files': []}, safe=False)
    files = userproduct.files.all()
    if not files:
        return JsonResponse({'files': []}, safe=False)
    files = [file.file.url for file in files]
    if userproduct.is_completed:
        files = files
        print("files======", files)
    return JsonResponse({'files': files}, safe=False)


def approve_order(request):
    if request.method == 'POST':
        
        try:
            print("userproduct", request.POST.get('product_id'))
            print("this is the file=====", request.FILES.get('file'))
            product_id = request.POST.get('product_id')
            file = request.FILES.get('file')

            userproduct = admin_models.UserProducts.objects.get(id=product_id)
            print("userproduct", userproduct)
            userproduct.completed_final_file = file
            userproduct.is_completed = True
            userproduct.completed_on = timezone.now()
            print("completion date set!")
            userproduct.save()
            print("User product saved!")
            print(settings.SENDGRID_API_KEY)

            sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
            email = Mail(
                    from_email=settings.SENDGRID_FROM_EMAIL,
                    to_emails=userproduct.user.user.email,
                    subject='Your order has been approved',
                    html_content='<p>Your order has been approved successfully. Please log into the site and check your "Completed Orders" tab to view the report</p>'
                )
            response = sg.send(email)
            print("Email sent:", response.status_code, response.body)

            return JsonResponse({'success': True}, safe=False)
        except admin_models.UserProducts.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        except sendgrid.exceptions.SendGridException as e:
            print(f"SendGrid error: {e}")
            return JsonResponse({'status': 'error', 'message': 'Failed to send email. Please check your SendGrid configuration.'}, status=500)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


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
