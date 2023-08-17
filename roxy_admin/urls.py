"""
This module provides the `path` function for defining URL patterns for 
Django views.

"""
from django.urls import path
from . import views

app_name = "roxy_admin"

urlpatterns = [
    # login/logout paths
    path("login/", views.LoginRequest, name="LoginRequest"),
    path("logout/", views.custom_logout, name="Logout"),
    # User creation paths
    path("surfer-create/", views.UserCreate_Surfer, name="UserCreate_Surfer"),
    path
    ("volunteer-create/", views.UserCreate_Volunteer, name="UserCreate_Volunteer"),
    # Role landing paths
    path("surfer/", views.SurferPage, name="SurferPage"),
    path("volunteer/", views.VolunteerPage, name="VolunteerPage"),
    path("admin/", views.AdminPage, name="AdminPage"),
    # Details paths
    path("surfer/<pk>/", views.SurferDetails, name="SurferDetails"),
    path("volunteer/<pk>/", views.VolunteerDetails, name="VolunteerDetails"),
    # Edit path
    path("editsurfer/<pk>/", views.SurferEdit, name="SurferEdit"),
    path("editvolunteer<pk>/", views.VolunteerEdit, name="VolunteerEdit"),
    # Calendar Paths
    path("calendar/", views.calendar_view, name="Calendar"),
    path("add_event/", views.add_event, name="AddEvent"),
    # Adv Search Paths
    path("search/", views.advanced_search, name="Adv_search"),
    # Export Paths
    path('export_to_excel/', views.export_excel, name='ExportExcel'),
    path('store_selected_users/', views.store_selected_users, name='StoreSelectedUsers'),
    # QR Code Paths
    path('qrscanner/', views.QRScannerView, name='QR_Scanner'),
    path('startendtracking/', views.StartEndTracking , name='StartEndTracking'),
    path('endalltracking/', views.EndAllTracking , name='EndAllTracking'),
    path('search-users-by-name/', views.SearchUsersByName, name='SearchUsersByName'),
    path('getusername/', views.GetUsername, name='GetUsername'),
]


