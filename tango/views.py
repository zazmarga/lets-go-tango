from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.template import loader

from django.urls import reverse_lazy, reverse
from django.views import generic


from tango.forms import (LoginForm, SignUpForm, ActivityCreationForm,
                         PlaceCreationForm, OccupationCreationForm,
                         CategoryCreationForm, MemberSearchForm,
                         ActivitySearchForm, )
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
        queryset = (Activity.objects.order_by("name").select_related("location", "possessor"))
        form = ActivitySearchForm(self.request.GET)
        if form.is_valid():
            day_of_week = form.cleaned_data.get("day_of_week")

            if form.cleaned_data.get("is_mine"):
                queryset = queryset.filter(possessor=form.cleaned_data.get("user_id"))
            if day_of_week != "":
                queryset = queryset.filter(day_of_week=day_of_week)

        category_id = self.request.GET.get("id_category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(activity_count=Count("activity"))
        context["activity_search_form"] = ActivitySearchForm(self.request.GET)
        return context


class ActivityDetailView(LoginRequiredMixin, generic.DetailView):
    model = Activity
    queryset = (Activity.objects.order_by("name").select_related("category", "location", "possessor"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(activity_count=Count("activity"))
        return context


class MembersListView(LoginRequiredMixin, generic.ListView):
    model = Member
    paginate_by = 4

    def get_queryset(self):
        queryset = Member.objects.order_by("last_name", "first_name").prefetch_related("occupations")
        form = MemberSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                last_name__icontains=form.cleaned_data["last_name"]
            )
        occupation_id = self.request.GET.get("occupation_id")
        if occupation_id:
            queryset = queryset.filter(occupations__id=occupation_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["occupations"] = Occupation.objects.annotate(member_count=Count("members"))
        last_name = self.request.GET.get("last_name", "")
        context["member_search_form"] = MemberSearchForm(
                initial={"last_name": last_name}
        )
        return context


class MemberDetailView(LoginRequiredMixin, generic.DetailView):
    model = Member
    queryset = Member.objects.order_by("last_name", "first_name").prefetch_related("occupations")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["occupations"] = Occupation.objects.annotate(member_count=Count("members"))
        context["activities"] = (Activity.objects.order_by("name").select_related("possessor"))
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


class ActivityCreateView(LoginRequiredMixin, generic.CreateView):
    model = Activity
    form_class = ActivityCreationForm
    success_url = reverse_lazy("tango:activity-detail")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(activity_count=Count("activity"))
        return context

    def get_success_url(self):
        return reverse("tango:activity-detail", kwargs={"pk": self.object.pk})


class ActivityUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Activity
    form_class = ActivityCreationForm
    success_url = reverse_lazy("tango:activity-detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(activity_count=Count("activity"))
        return context

    def get_success_url(self):
        return reverse("tango:activity-detail", kwargs={"pk": self.object.pk})


class PlaceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Place
    form_class = PlaceCreationForm
    success_url = reverse_lazy("tango:place-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities_count"] = Place.objects.values("city").annotate(place_count=Count("id"))
        return context

    def form_valid(self, form):
        new_city = form.cleaned_data.get("new_city")
        if new_city:
            form.instance.city = new_city
        return super().form_valid(form)


class OccupationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Occupation
    form_class = OccupationCreationForm
    success_url = reverse_lazy("tango:member-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["occupations"] = Occupation.objects.annotate(member_count=Count("members"))
        return context


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    form_class = CategoryCreationForm
    success_url = reverse_lazy("tango:activity-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(activity_count=Count("activity"))
        return context


class ActivityDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Activity
    success_url = reverse_lazy("tango:activity-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(activity_count=Count("activity"))
        return context
