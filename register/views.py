from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# import requests
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, UserForm, UserProfileForm
from register import models as register_models

from adminview import emails as adminview_emails, models as admin_models, tables as admin_tables, forms as admin_forms
import stripe


# Create your views here.
@login_required
def account_logout(request):
    logout(request)
    return redirect("login")


def account_register(request):
    form = RegisterForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user_obj = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            userprofile = register_models.UserProfile.objects.create(user=user_obj, email_verified=False)
            adminview_emails.send_email(userprofile, "https://{}".format(request.get_host()), 'register')
            messages.success(request, "Signup Successfully!")
            return redirect("login")
        else:
            messages.error(request, "Error validating the form")
    return render(request, "pages/sign-up.html",
                  {
                      "form": form,
                      "msg": msg,
                      "title": "Signup",
                      "subtitle": "Add your Details",
                      "btn_title": "Sign Up",
                      'signup_flag': True
                  }
                  )


@csrf_exempt
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            userprofile = register_models.UserProfile.objects.filter(user=user).last()
            if userprofile and not userprofile.email_verified:
                messages.error(request, "Email is not verified, Please verify email First")
                return redirect('login')
            if user is not None:
                login(request, user)
                if user.is_staff:
                    messages.success(request, "Welcome Admin!")
                    return redirect('admin-dashboard-verified-users')
                messages.success(request, "Welcome User!")
                return redirect('user-dashboard')
            else:
                messages.error(request, "Email or Password not correct!")
        else:
            messages.error(request, "Error validating the form")
    return render(request, "pages/sign-in.html",
                  {
                      "form": form,
                      "msg": msg,
                      "title": "Login",
                      "subtitle": "Add your credentials",
                      "btn_title": "Sign in"
                  }
                  )


def verify_email(request, pk):
    obj = register_models.UserProfile.objects.filter(user_id=pk).last()
    obj: register_models.UserProfile
    obj.email_verified = True
    messages.success(request, f"{obj.user.get_full_name()} your Email has been verified Successfully")
    return redirect('login')


# ===========TODO==========================


@csrf_exempt
def user_dashboard(request):
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
        "table": admin_tables.ProductsTable(queryset),

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
        'is_admin': False
    }
    return render(request, "pages/django-tables.html", context)


def user_open_orders(request):
    user = request.user
    open_orders = admin_models.UserProducts.objects.filter(user=user.userprofile, is_completed=False)
    context = {
        "title": "List of Open Orders",
        "page_name": "Open Orders",
        "queryset": open_orders,
        "table": admin_tables.OpenProductsTable(open_orders),
        "header": {
            "links": [

            ],
        },
        "segment": "open_orders",
        # 'nav_conf': {
        #     'active_classes': ['admin-settings', ''],
        #     'collapse_class': '',
        # },
        'is_admin': False
    }
    return render(request, "pages/django-tables.html", context)


def completed_orders(request):
    user = request.user
    open_orders = admin_models.UserProducts.objects.filter(user=user.userprofile, is_completed=True)
    context = {
        "title": "List of Open Orders",
        "page_name": "Open Orders",
        "queryset": open_orders,
        "table": admin_tables.CompletedProductsTable(open_orders),
        "header": {
            "links": [

            ],
        },
        "segment": "completed_orders",
        # 'nav_conf': {
        #     'active_classes': ['admin-settings', ''],
        #     'collapse_class': '',
        # },
        'is_admin': False
    }
    return render(request, "pages/django-tables.html", context)


def user_buy_product(request, product_id):
    product = get_object_or_404(admin_models.Products, id=product_id)
    lst = []
    lst.append({'price_data': {'currency': 'usd', 'unit_amount': int(product.price) * 100,
                               'product_data': {
                                   'name': f'Product: {product.name} (USD {product.price})',
                                   'description': f"Description: {product.description}",
                               }
                               },
                'quantity': 1,
                }
               )
    success_url = "{}://{}{}".format(request.scheme, request.get_host(),
                                     reverse('success-order',
                                             kwargs={'slug': str(product_id) + "," + str(request.user.id)}))
    cancel_url = "{}://{}{}".format(request.scheme, request.get_host(),
                                    reverse('failed-order',
                                            kwargs={'slug': str(product_id) + "," + str(request.user.id)}))
    stipe_secret_key = "sk_test_51PGKtcCU4q9m0okPsUbR4DnQOsYE9df4Mc5zWYLIp4XPqubLWTvo2tjvMK6l1h8ldezryfl64whKzkStIhoR43N600v2uKzFt0"
    try:
        stripe.api_key = stipe_secret_key
        checkout_session = stripe.checkout.Session.create(
            success_url=success_url,
            cancel_url=cancel_url,
            payment_method_types=['card'],
            mode='payment',
            line_items=lst,
        )

        # print({'sessionUrl': checkout_session.url, 'sessionID': checkout_session.id})
        return redirect(checkout_session.url)
    except Exception as e:
        messages.error(request, f"Something went wrong in Stripe!")
        return redirect('checkout-order-billing')



def upload_file(request, product_id):
    user = request.user
    user_product = admin_models.UserProducts.objects.get(user=user.userprofile, id=product_id)
    user_product.files.create(file=request.FILES['file'])
    user_product.save()
    return JsonResponse({'status': 'success', "success": True})


def success_order(request, slug):
    product_id, user_id = slug.split(",")
    user = User.objects.get(id=user_id)
    product = admin_models.Products.objects.get(id=product_id)
    user_product = admin_models.UserProducts.objects.create(user=user.userprofile, product_id=product_id)
    user_product.is_completed = False
    user_product.save()

    return redirect('user-dashboard')


def failed_order(request, slug):
    return redirect('user-dashboard')
