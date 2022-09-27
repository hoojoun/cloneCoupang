from django.contrib.auth import login as authlogin
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from shops.models import *
from .forms import *
from .models import *
from django.core.paginator import Paginator


# Create your views here.
class UpdatedLoginView(auth_views.LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        if remember_me:
            self.request.session.set_expiry(10000000)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)


# def landing(request):
#     page = request.GET.get('page', '1')
#     products = Products.objects.all()
#     paginator = Paginator(products, 10)
#     page_obj = paginator.get_page(page)
#     context = {'products': page_obj}
#     return render(request, 'shops/landing.html', {'products': products})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    consents = Consent.objects.all()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if request.POST['password1'] == request.POST['password2']:
                username = "U_" + request.POST['username']
                user = CustomUser.objects.create_user(
                    username=username,
                    password=request.POST['password1'],
                    name=request.POST['name'],
                    phone=request.POST['phone'],
                )
                # username =form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # name = form.cleaned_data.get('name')
            # phone = form.cleaned_data.get('phone')
            # form.save()
            # user = authenticate(username=username, password=raw_password, name=name, phone=phone)
            authlogin(request, user)
            ######
            user = CustomUser.objects.get(username=username)
            consent_list = []
            for consent in consents:
                if request.POST.get(consent.name) == "on":
                    checked = 1
                else:
                    checked = 0
                if consent.isUser == 1:
                    consent_list.append(UserConsent(cid=consent, ccheck=checked, user=user))
            UserConsent.objects.bulk_create(consent_list)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'shops/signup.html', {'form': form, 'consents': consents})


def signup_seller(request):
    if request.user.is_authenticated:
        return redirect('/')
    consents = Consent.objects.all()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if request.POST['password1'] == request.POST['password2']:
                USERNAME = "S_" + request.POST['username']
                user = CustomUser.objects.create_user(
                    username=USERNAME,
                    password=request.POST['password1'],
                    name=request.POST['name'],
                    phone=request.POST['phone'],
                    email=request.POST['email'],
                )

            # form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # name = form.cleaned_data.get('name')
            # email = form.cleaned_data.get('email')
            # phone = form.cleaned_data.get('phone')
            # user = authenticate(username=username, password=raw_password, name=name, phone=phone, email=email)
            authlogin(request, user)
            ######
            user = CustomUser.objects.get(username=USERNAME)
            ######
            CustomSeller.objects.create(CustomUser=user, businessType=request.POST.get('businessType'))
            consent_list = []
            for consent in consents:
                if request.POST.get(consent.name) == "on":
                    checked = 1
                else:
                    checked = 0
                if consent.isUser == 0:
                    consent_list.append(UserConsent(cid=consent, ccheck=checked, user=user))
            UserConsent.objects.bulk_create(consent_list)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'shops/signupSeller.html', {'form': form, 'consents': consents})
