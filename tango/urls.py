from django.contrib.auth.views import LogoutView
from django.urls import path

from tango.views import (
    index,
    login_view,
    register_user,
    ActivitiesListView,
    ActivityDetailView,
    MembersListView,
    MemberDetailView,
    PlacesListView,
)



urlpatterns = [
    path("", index, name="index"),
    path("login/", login_view, name="login"),
    path("register/", register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("activities/", ActivitiesListView.as_view(), name="activity-list"),
    path("activities/<int:pk>/", ActivityDetailView.as_view(), name="activity-detail"),
    path("members/", MembersListView.as_view(), name="member-list"),
    path("members/<int:pk>/", MemberDetailView.as_view(), name="member-detail"),
    path("places/", PlacesListView.as_view(), name="place-list"),

]

app_name = "tango"
