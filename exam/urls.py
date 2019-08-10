"""exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView, ListView
from app1.models import Student,Question
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', TemplateView.as_view(template_name="login.html")),
    path('login/',views.logIn),
    path('admin_logout/',views.logOut),
    path('viewmessage/',views.viewMessages),
    path('testreport/',views.testReport),
    path('admin_report/',views.admin_Report),
    path('teststatus/',views.testStatus),
    path('statustest/',views.statusTest),
    path('register/',views.registerPage),
    path('save/',views.saveDetails),
    path('addfaculty/',views.CreateFaculty.as_view()),
    path('viewall/',ListView.as_view(model=Student,template_name="viewall.html")),
    path('viewfaculty/',views.viewFaculty),
    path('studentlogin/',TemplateView.as_view(template_name="studentlogin.html")),
    # path('checklogin/',views.checkLogin),
    path('viewstudent/',views.showDetails),
    path('editprofile<str:pk>/',views.UpdateProf.as_view()),
    path('changepass/',views.changePass),
    path('updatepass/',views.updatePass),
    path('passupdate/',views.passUpdate),
    path('newpass/',views.newPass),
    path('exam/',views.openExam),
    path('selectexam/',views.selectExam),
    path('visualexam/',views.visualExam),
    path('option/',views.visual_2),
    path('select_java/',views.select_JAVA),
    path('java_option/',views.option_JAVA),
    path('select_asp/',views.select_ASP),
    path('asp_option/',views.option_ASP),
    path('neg_exam/',views.neg_Exam),
    path('select_neg_exam/',views.select_NEG_exam),
    path('neg_visualexam/',views.neg_visualExam),
    path('neg_option/',views.neg_Visual_2),
    path('select_neg_java/',views.select_neg_java),
    path('neg_java_option/',views.neg_java_2),
    path('select_neg_asp/',views.select_neg_asp),
    path('neg_asp_option/',views.neg_asp_2),
    # path('visual_3/',views.visual_3),
    # path('visual_4/',views.visual_4),
    # path('feedback/',views.examFeedback),
    # path('result/',views.showResult),
    # path('allstatus/',views.showexamStatus),
    path('allresults/',views.examResults),
    path('postquestion/',views.postQuestion),
    path('requestquestion/',views.requestQuestion),
    path('savequestion/',views.saveQuestion),
    path('view_status/',views.view_Status),
    path('see_status/',views.see_Status),
    path('exam_report/',views.exam_Report),
    path('report_exam/',views.report_Exam)
]