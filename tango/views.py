from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.template import loader
# from django.template.context_processors import request

from tango.forms import LoginForm, SignUpForm
from tango.models import Activity, Member, Place, Opinion


@login_required(login_url="/login/")
def index(request):
    num_activities = Activity.objects.count()
    num_members = Member.objects.count()
    num_places = Place.objects.count()
    num_opinions = Opinion.objects.count()

    context = {
        "segment": "index",
        "num_activities": num_activities,
        "num_members": num_members,
        "num_places": num_places,
        "num_opinions": num_opinions,
    }

    html_template = loader.get_template("tango/index.html")
    return HttpResponse(html_template.render(context, request))

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = "Invalid credentials"
        else:
            msg = "Error validating the form"

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            authenticate(username=username, password=raw_password)

            msg = "Account created successfully."
            success = True

            return redirect("/login/")

        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
