from django.urls import path

from tango.views import (
    index,
    login_view,
    register_user,
    LogoutView,
    ActivitiesListView,
    ActivityDetailView,
    MembersListView,
    MemberDetailView,
    PlacesListView,
    PlaceDetailView,
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
    path("places/<int:pk>/", PlaceDetailView.as_view(), name="place-detail"),
]

app_name = "tango"
