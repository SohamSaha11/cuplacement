from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('student/signup', views.studentSignUp),
    path('student/login', views.studentLogIn),
    path('home', views.home),
    path('logout', views.logout),
    path('placementCell/login', views.pcLogIn),
    path('placementCell/signup', views.pcSignUp),
    path('home/company/add', views.addCompany),
    path('home/noticeBoard', views.noticeBoard),
    path('home/noticeBoard/add', views.addNotice),
    path('home/placedRecord', views.placedRecord),
    path('home/placedRecord/add', views.addStudent),
]