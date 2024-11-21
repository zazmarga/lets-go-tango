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
    MemberCreateView,
    ActivityCreateView,
    PlaceCreateView,
    ActivityUpdateView,
    OccupationCreateView,
    CategoryCreateView,
    ActivityDeleteView,
    MemberUpdateView,
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
    path("members/create/", MemberCreateView.as_view(), name="member-create"),
    path("activities/create/", ActivityCreateView.as_view(), name="activity-create"),
    path("activities/<int:pk>/update/", ActivityUpdateView.as_view(), name="activity-update"),
    path("places/create/", PlaceCreateView.as_view(), name="place-create"),
    path("occupations/create/", OccupationCreateView.as_view(), name="occupation-create"),
    path("category/create/", CategoryCreateView.as_view(), name="category-create"),
    path("activities/<int:pk>/delete/", ActivityDeleteView.as_view(), name="activity-delete"),
    path("members/<int:pk>/update/", MemberUpdateView.as_view(), name="member-update"),
]

app_name = "tango"
