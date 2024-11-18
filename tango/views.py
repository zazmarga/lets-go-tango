from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import generic


from tango.forms import LoginForm, SignUpForm
from tango.models import Activity, Member, Place, Category, Occupation



@login_required(login_url="/login/")
def index(request):
    num_activities = Activity.objects.count()
    num_members = Member.objects.count()
    num_places = Place.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "segment": "index",
        "num_activities": num_activities,
        "num_members": num_members,
        "num_places": num_places,
        "num_visits": num_visits + 1,
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

            # return redirect("/")

        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


class LogoutView(LoginRequiredMixin, generic.TemplateView):
    template_name = "accounts/logout.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        sessions = Session.objects.filter()
        for session in sessions:
            data = session.get_decoded()
            if data.get("_auth_user_id") == str(user.id):
                session.delete()
        logout(request)
        return redirect("/")


class ActivitiesListView(LoginRequiredMixin, generic.ListView):
    model = Activity
    paginate_by = 4

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


class ActivityDetailView(LoginRequiredMixin, generic.DetailView):
    model = Activity
    queryset = (Activity.objects.order_by("name").select_related("category", "location", "possessor")
                    .prefetch_related("members__occupations"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(activity_count=Count("activity"))
        return context


class MembersListView(LoginRequiredMixin, generic.ListView):
    model = Member
    paginate_by = 4

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


class MemberDetailView(LoginRequiredMixin, generic.DetailView):
    model = Member
    queryset = Member.objects.order_by("last_name", "first_name").prefetch_related("occupations")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["occupations"] = Occupation.objects.annotate(member_count=Count("members"))
        context["activities"] = (Activity.objects.order_by("name").select_related("possessor")
                    .prefetch_related("members"))
        return context


class PlacesListView(LoginRequiredMixin, generic.ListView):
    model = Place
    paginate_by = 4

    def get_queryset(self):
        queryset = Place.objects.order_by("name")
        city = self.request.GET.get("city")
        if city:
            queryset = queryset.filter(city=city)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities_count"] = Place.objects.values("city").annotate(place_count=Count("id"))
        return context


class PlaceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Place
    queryset = Place.objects.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities_count"] = Place.objects.values("city").annotate(place_count=Count("id"))
        context["activities"] = Activity.objects.order_by("name").select_related("location", "possessor")
        return context


class MemberCreateView(LoginRequiredMixin, generic.CreateView):
    model = Member
    form_class = SignUpForm
    success_url = reverse_lazy("tango:member-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["occupations"] = Occupation.objects.annotate(member_count=Count("members"))
        return context
