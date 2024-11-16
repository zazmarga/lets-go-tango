from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.views import generic

# from django.template.context_processors import request

from tango.forms import LoginForm, SignUpForm
from tango.models import Activity, Member, Place, Opinion, Category, Occupation


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


class ActivitiesListView(generic.ListView):
    model = Activity
    paginate_by = 5

    def get_queryset(self):
        queryset = (Activity.objects.order_by("name").select_related("location", "possessor")
                    .prefetch_related("members"))
        category_id = self.request.GET.get("id_category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(activity_count=Count("activity"))
        return context


class ActivityDetailView(generic.DetailView):
    model = Activity
    queryset = (Activity.objects.order_by("name").select_related("category", "location", "possessor")
                    .prefetch_related("members__occupations"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(activity_count=Count("activity"))
        return context


class MembersListView(generic.ListView):
    model = Member
    paginate_by = 5

    def get_queryset(self):
        queryset = Member.objects.order_by("last_name", "first_name").prefetch_related("occupations")
        occupation_id = self.request.GET.get("occupation_id")
        if occupation_id:
            queryset = queryset.filter(occupations__id=occupation_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["occupations"] = Occupation.objects.annotate(member_count=Count("members"))
        return context


class MemberDetailView(generic.DetailView):
    model = Member
    queryset = Member.objects.order_by("last_name", "first_name").prefetch_related("occupations")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["occupations"] = Occupation.objects.annotate(member_count=Count("members"))
        context["activities"] = (Activity.objects.order_by("name").select_related("possessor")
                    .prefetch_related("members"))
        return context


class PlacesListView(generic.ListView):
    model = Place
    paginate_by = 5
