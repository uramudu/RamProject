from django.shortcuts import render,redirect
from .models import Student,Faculty,Creater,Question,Negative_Exam,Non_Negative_Eaxm
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
import datetime


def getUser(request):
    user = request.session["token"]
    return user

def logIn(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    request.session['token'] = email
    qs = Creater.objects.filter(adminemail=email,admilpass=password)
    qs1 = Student.objects.filter(emailid=email,password=password)
    semail = ""
    for x in qs1:
        semail = x.emailid
    request.session["semail"] = semail
    if qs:
        return render(request,"loginpage.html")
    elif qs1:
        return render(request,"loginsuccess.html",{"res":qs1})
    else:
        return render(request,"invaild.html")


def testReport(request):
    qs = Student.objects.all()
    return render(request,"testreport.html",{"res": qs})



def admin_Report(request):
    d1 = request.POST.get("d1")
    d2 = request.POST.get("d2")
    email = request.POST.get("email")
    exam = request.POST.get("exam")
    print(exam)
    qs = Faculty.objects.all()
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    if exam == "Non-negative":
        qs3 = Non_Negative_Eaxm.objects.filter(date__range=(d1,d2),email=email)
        print(qs3)
        return render(request,"adminreport.html",{"res3":qs3,"res1":qs,"res":qs1})
    else:
        qs2 = Negative_Exam.objects.filter(date__range=(d1,d2),email=email)
        return render(request,"adminreport.html",{"res3":qs2,"res1":qs,"res":qs1})



def testStatus(request):
    qs = Student.objects.all()
    return render(request, "teststatus.html",{"res": qs})


def statusTest(request):
    email1 = request.POST.get("email")
    subject = request.POST.get("subject")
    exam = request.POST.get("exam")
    if exam == "Non-negative":
        qs2 = Non_Negative_Eaxm.objects.filter(email=email1,type=subject)
        return render(request,"non_negative_results.html",{"res2":qs2})
    else:
        qs3 = Negative_Exam.objects.filter(email=email1,type=subject)
        return render(request,"non_negative_results.html",{"res2":qs3})


def registerPage(request):
    return render(request,"register.html")


def saveDetails(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    gender = request.POST.get("gender")
    password = request.POST.get("password")
    contact_no = request.POST.get("contact_no")
    qualification = request.POST.get("qualification")
    course = request.POST.get("course")
    experience = request.POST.get("experience")
    address = request.POST.get("address")
    s = Student(name=name,emailid=email,gender=gender,password=password,contact_no=contact_no,qualification=qualification,course=course,experience=experience,address=address)
    s.save()
    qs = Student.objects.filter(emailid=email)
    semail = ""
    for x in qs:
        semail = x.emailid
    request.session["semail"] = semail
    return render(request,"loginsuccess.html",{"res":qs})


class CreateFaculty(CreateView):
    template_name = "faculty.html"
    model = Faculty
    success_url = '/addfaculty/'
    fields = ('name','emailid','password','gender','contact_no','qualification','skils','experience','address')

#
# def checkLogin(request):
#     email = request.POST.get("email")
#     password = request.POST.get("password")
#     qs = Student.objects.filter(emailid=email,password=password)
#     if not qs:
#         return render(request,"invaild.html")
#     else:
#         semail = ""
#         for x in qs:
#             semail = x.emailid
#         request.session["semail"] = semail
#         return render(request,"loginsuccess.html",{"res":qs})


def showDetails(request):
    email = request.GET.get("email")
    qs = Student.objects.filter(emailid=email)
    return render(request,"onestudent.html",{"res":qs})


def viewFaculty(request):
    res  = request.session["semail"]
    print(res)
    # print("Welcome",res)
    qs1  =  Student.objects.filter(emailid=res)

    qs = Faculty.objects.all()
    return render(request,"allfaculty.html",{"result":qs,"res":qs1})


class UpdateProf(SuccessMessageMixin,UpdateView):
    template_name = "updateprof.html"
    model = Student
    fields = ('name','emailid','password','gender','contact_no','qualification','course','experience','address')
    success_url = '/viewfaculty/'
    success_message = "User Profile Updated successfully"



def changePass(request):
    qs = Creater.objects.all()
    return render(request,"changepass.html",{"res":qs})


def updatePass(request):
    uname = request.POST.get("uname")
    oldpw = request.POST.get("oldpw")
    newpw = request.POST.get("newpw")
    qs = Creater.objects.filter(adminemail=uname)
    for x in qs:
        if uname == x.adminemail and oldpw == x.admilpass:
            Creater(adminemail=uname,admilpass=newpw).save()
            return render(request,"loginpage.html",{"message":"Password is Updated"})
        else:
            return render(request,"changepass.html",{"msg":"Invalid Details"})


def passUpdate(request):
    email = request.GET.get("email")
    qs = Student.objects.filter(emailid=email)
    return render(request,"passupdate.html",{"res":qs})


def newPass(request):
    uname = request.POST.get("uname")
    oldpw = request.POST.get("oldpw")
    newpw = request.POST.get("newpw")
    name = request.POST.get("name")
    gender = request.POST.get("gender")
    contact_no = request.POST.get("contact_no")
    qualification = request.POST.get("qualification")
    course = request.POST.get("course")
    experience = request.POST.get("experience")
    address = request.POST.get("address")
    qs = Student.objects.filter(emailid=uname)
    for x in qs:
        if uname == x.emailid and oldpw == x.password:
            Student(emailid=uname,password=newpw,name=name,gender=gender,contact_no=contact_no,qualification=qualification,course=course,experience=experience,address=address).save()
            return render(request, "loginsuccess.html", {"message": "Password is Updated","res":qs})
        else:
            return render(request, "passupdate.html", {"msg": "Invalid Details","res":qs})


def logOut(request):
    del request.session['token']
    return render(request,"logout.html")

def openExam(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request,"index.html",{"res":qs1,"res1":qs})


def selectExam(request):
    opt = request.POST.get("r1")
    etype = opt
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    request.session['type_exam']= etype
    if opt == "Visualbasic6.0":
        return render(request,"visual.html",{"res":qs1,"res1":qs})
    elif opt == "Java":
        return render(request,"java.html",{"res":qs1,"res1":qs})
    elif opt == "ASP":
        return render(request,"asp.html",{"res":qs1,"res1":qs})
    else:
        return render(request,"noexam.html",{"res":qs1,"res1":qs})


def visualExam(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request,"visual_1.html",{"res":qs1,"res1":qs})


def visual_2(request):

    que1 = request.POST.get("q1")
    c_a1 = request.POST.get("c1")
    ans1 = request.POST.get("a1")
    type = request.session["type_exam"]
    res = request.session["semail"]

    que2 = request.POST.get("q2")
    c_a2 = request.POST.get("c2")
    ans2 = request.POST.get("a2")


    que3 = request.POST.get("q3")
    c_a3 = request.POST.get("c3")
    ans3 = request.POST.get("a3")


    que4 = request.POST.get("q4")
    c_a4 = request.POST.get("c4")
    ans4 = request.POST.get("a4")
    date=datetime.datetime.now()

    Non_Negative_Eaxm.objects.bulk_create([
        Non_Negative_Eaxm(question=que1, correct_ans=c_a1, answer=ans1, type=type,date=date,email=res),
        Non_Negative_Eaxm(question=que2, correct_ans=c_a2, answer=ans2, type=type,date=date,email=res),
        Non_Negative_Eaxm(question=que3, correct_ans=c_a3, answer=ans3, type=type,date=date,email=res),
        Non_Negative_Eaxm(question=que4, correct_ans=c_a4, answer=ans4, type=type,date=date,email=res),
    ])
    qs3 = Non_Negative_Eaxm.objects.filter(date=date)
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request,"feedback.html",{"res":qs1,"res1":qs,"res3":qs3,"q1":que1,"q2":que2,"q3":que3,"q4":que4,"c1":c_a1,"c2":c_a2,"c3":c_a3,"c4":c_a4,"a1":ans1,"a2":ans2,"a3":ans3,"a4":ans4,"d1":date,"t1":type})


def select_JAVA(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request, "java_1.html", {"res": qs1,"res1": qs})


def option_JAVA(request):
    que1 = request.POST.get("q1")
    c_a1 = request.POST.get("c1")
    ans1 = request.POST.get("a1")
    type = request.session["type_exam"]
    res = request.session["semail"]

    que2 = request.POST.get("q2")
    c_a2 = request.POST.get("c2")
    ans2 = request.POST.get("a2")

    que3 = request.POST.get("q3")
    c_a3 = request.POST.get("c3")
    ans3 = request.POST.get("a3")

    que4 = request.POST.get("q4")
    c_a4 = request.POST.get("c4")
    ans4 = request.POST.get("a4")
    date = datetime.datetime.now()

    Non_Negative_Eaxm.objects.bulk_create([
        Non_Negative_Eaxm(question=que1, correct_ans=c_a1, answer=ans1, type=type, date=date, email=res),
        Non_Negative_Eaxm(question=que2, correct_ans=c_a2, answer=ans2, type=type, date=date, email=res),
        Non_Negative_Eaxm(question=que3, correct_ans=c_a3, answer=ans3, type=type, date=date, email=res),
        Non_Negative_Eaxm(question=que4, correct_ans=c_a4, answer=ans4, type=type, date=date, email=res),
    ])
    qs3 = Non_Negative_Eaxm.objects.filter(date=date)
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request, "feedback.html",
                  {"res": qs1, "res1": qs, "res3": qs3, "q1": que1, "q2": que2, "q3": que3, "q4": que4, "c1": c_a1,
                   "c2": c_a2, "c3": c_a3, "c4": c_a4, "a1": ans1, "a2": ans2, "a3": ans3, "a4": ans4, "d1": date,
                   "t1": type})


def select_ASP(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request, "asp_1.html", {"res": qs1, "res1": qs})


def option_ASP(request):
    que1 = request.POST.get("q1")
    c_a1 = request.POST.get("c1")
    ans1 = request.POST.get("a1")
    type = request.session["type_exam"]
    res = request.session["semail"]

    que2 = request.POST.get("q2")
    c_a2 = request.POST.get("c2")
    ans2 = request.POST.get("a2")

    que3 = request.POST.get("q3")
    c_a3 = request.POST.get("c3")
    ans3 = request.POST.get("a3")

    que4 = request.POST.get("q4")
    c_a4 = request.POST.get("c4")
    ans4 = request.POST.get("a4")
    date = datetime.datetime.now()

    Non_Negative_Eaxm.objects.bulk_create([
        Non_Negative_Eaxm(question=que1, correct_ans=c_a1, answer=ans1, type=type, date=date, email=res),
        Non_Negative_Eaxm(question=que2, correct_ans=c_a2, answer=ans2, type=type, date=date, email=res),
        Non_Negative_Eaxm(question=que3, correct_ans=c_a3, answer=ans3, type=type, date=date, email=res),
        Non_Negative_Eaxm(question=que4, correct_ans=c_a4, answer=ans4, type=type, date=date, email=res),
    ])
    qs3 = Non_Negative_Eaxm.objects.filter(date=date)
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request, "feedback.html",
                  {"res": qs1, "res1": qs, "res3": qs3, "q1": que1, "q2": que2, "q3": que3, "q4": que4, "c1": c_a1,
                   "c2": c_a2, "c3": c_a3, "c4": c_a4, "a1": ans1, "a2": ans2, "a3": ans3, "a4": ans4, "d1": date,
                   "t1": type})


def neg_Exam(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request,"neg_exam.html",{"res":qs1,"res1":qs})


def select_NEG_exam(request):
    neg_opt = request.POST.get("r1")
    etype = neg_opt
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    request.session['type_neg_exam'] = etype
    if neg_opt == "Visualbasic6.0":
        return render(request, "neg_visual.html", {"res": qs1, "res1": qs})
    elif neg_opt == "Java":
        return render(request, "neg_java.html", {"res": qs1, "res1": qs})
    elif neg_opt == "ASP":
        return render(request, "neg_asp.html", {"res": qs1, "res1": qs})
    else:
        return render(request, "neg_noexam.html", {"res": qs1, "res1": qs})


def neg_visualExam(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request,"neg_visual_1.html",{"res":qs1,"res1":qs})


def neg_Visual_2(request):

    que1 = request.POST.get("q1")
    c_a1 = request.POST.get("c1")
    ans1 = request.POST.get("a1")
    type = request.session["type_neg_exam"]
    res = request.session["semail"]

    que2 = request.POST.get("q2")
    c_a2 = request.POST.get("c2")
    ans2 = request.POST.get("a2")


    que3 = request.POST.get("q3")
    c_a3 = request.POST.get("c3")
    ans3 = request.POST.get("a3")


    que4 = request.POST.get("q4")
    c_a4 = request.POST.get("c4")
    ans4 = request.POST.get("a4")
    date=datetime.datetime.now()

    Negative_Exam.objects.bulk_create([
        Negative_Exam(question=que1, correct_ans=c_a1, answer=ans1, type=type,date=date,email=res),
        Negative_Exam(question=que2, correct_ans=c_a2, answer=ans2, type=type,date=date,email=res),
        Negative_Exam(question=que3, correct_ans=c_a3, answer=ans3, type=type,date=date,email=res),
        Negative_Exam(question=que4, correct_ans=c_a4, answer=ans4, type=type,date=date,email=res),
    ])
    qs3 = Negative_Exam.objects.filter(date=date)
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request,"neg_feedback.html",{"res":qs1,"res1":qs,"res3":qs3,"q1":que1,"q2":que2,"q3":que3,"q4":que4,"c1":c_a1,"c2":c_a2,"c3":c_a3,"c4":c_a4,"a1":ans1,"a2":ans2,"a3":ans3,"a4":ans4,"d1":date,"t1":type})


def select_neg_java(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request, "neg_java_1.html", {"res":qs1, "res1":qs})


def neg_java_2(request):
    que1 = request.POST.get("q1")
    c_a1 = request.POST.get("c1")
    ans1 = request.POST.get("a1")
    type = request.session["type_neg_exam"]
    res = request.session["semail"]

    que2 = request.POST.get("q2")
    c_a2 = request.POST.get("c2")
    ans2 = request.POST.get("a2")

    que3 = request.POST.get("q3")
    c_a3 = request.POST.get("c3")
    ans3 = request.POST.get("a3")

    que4 = request.POST.get("q4")
    c_a4 = request.POST.get("c4")
    ans4 = request.POST.get("a4")
    date = datetime.datetime.now()

    Negative_Exam.objects.bulk_create([
        Negative_Exam(question=que1, correct_ans=c_a1, answer=ans1, type=type, date=date, email=res),
        Negative_Exam(question=que2, correct_ans=c_a2, answer=ans2, type=type, date=date, email=res),
        Negative_Exam(question=que3, correct_ans=c_a3, answer=ans3, type=type, date=date, email=res),
        Negative_Exam(question=que4, correct_ans=c_a4, answer=ans4, type=type, date=date, email=res),
    ])
    qs3 = Negative_Exam.objects.filter(date=date)
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request, "neg_feedback.html",
                  {"res": qs1, "res1": qs, "res3": qs3, "q1": que1, "q2": que2, "q3": que3, "q4": que4, "c1": c_a1,
                   "c2": c_a2, "c3": c_a3, "c4": c_a4, "a1": ans1, "a2": ans2, "a3": ans3, "a4": ans4, "d1": date,
                   "t1": type})


def select_neg_asp(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request, "neg_asp_1.html", {"res": qs1, "res1": qs})


def neg_asp_2(request):
    que1 = request.POST.get("q1")
    c_a1 = request.POST.get("c1")
    ans1 = request.POST.get("a1")
    type = request.session["type_neg_exam"]
    res = request.session["semail"]

    que2 = request.POST.get("q2")
    c_a2 = request.POST.get("c2")
    ans2 = request.POST.get("a2")

    que3 = request.POST.get("q3")
    c_a3 = request.POST.get("c3")
    ans3 = request.POST.get("a3")

    que4 = request.POST.get("q4")
    c_a4 = request.POST.get("c4")
    ans4 = request.POST.get("a4")
    date = datetime.datetime.now()

    Negative_Exam.objects.bulk_create([
        Negative_Exam(question=que1, correct_ans=c_a1, answer=ans1, type=type, date=date, email=res),
        Negative_Exam(question=que2, correct_ans=c_a2, answer=ans2, type=type, date=date, email=res),
        Negative_Exam(question=que3, correct_ans=c_a3, answer=ans3, type=type, date=date, email=res),
        Negative_Exam(question=que4, correct_ans=c_a4, answer=ans4, type=type, date=date, email=res),
    ])
    qs3 = Negative_Exam.objects.filter(date=date)
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request, "neg_feedback.html",
                  {"res": qs1, "res1": qs, "res3": qs3, "q1": que1, "q2": que2, "q3": que3, "q4": que4, "c1": c_a1,
                   "c2": c_a2, "c3": c_a3, "c4": c_a4, "a1": ans1, "a2": ans2, "a3": ans3, "a4": ans4, "d1": date,
                   "t1": type})



#
# def visual_3(request):
#     que2 = request.POST.get("q2")
#     c_a2 = request.POST.get("c2")
#     ans2 = request.POST.get("a2")
#     request.session['question_2'] = que2
#     request.session['answer_2'] = ans2
#     request.session['cor_ans_2'] = c_a2
#     e2 = request.session['type_exam']
#     res = request.session["semail"]
#     qs1 = Student.objects.filter(emailid=res)
#     qs = Faculty.objects.all()
#     Non_Negative_Eaxm(question=que2,correct_ans=c_a2,answer=ans2,type=e2).save()
#     return render(request,"visual_3.html",{"res":qs1,"res1":qs})
#
#
# def visual_4(request):
#     que3 = request.POST.get("q3")
#     c_a3 = request.POST.get("c3")
#     ans3 = request.POST.get("a3")
#     request.session['answer_3'] = ans3
#     request.session['question_3'] = que3
#     request.session['cor_ans_3'] = c_a3
#     e3 = request.session['type_exam']
#     res = request.session["semail"]
#     qs1 = Student.objects.filter(emailid=res)
#     qs = Faculty.objects.all()
#     Non_Negative_Eaxm(question=que3,correct_ans=c_a3,answer=ans3,type=e3).save()
#     return render(request, "visual_4.html",{"res":qs1,"res1":qs})
#
#
# def examFeedback(request):
#     que4 = request.POST.get("q4")
#     c_a4 = request.POST.get("c4")
#     ans4 = request.POST.get("a4")
#     request.session['answer_4'] = ans4
#     request.session['question_4'] = que4
#     request.session['cor_ans_4'] = c_a4
#     e4 = request.session['type_exam']
#     res = request.session["semail"]
#     qs1 = Student.objects.filter(emailid=res)
#     qs = Faculty.objects.all()
#     Non_Negative_Eaxm(question=que4,correct_ans=c_a4,answer=ans4,type=e4).save()
#     return render(request,"feedback.html",{"res":qs1,"res1":qs})
#
#
# def showResult(request):
#     res = request.session["semail"]
#     qs1 = Student.objects.filter(emailid=res)
#     qs = Faculty.objects.all()
#
#     a1 = request.session['answer_1']
#     a2 = request.session['answer_2']
#     a3 = request.session['answer_3']
#     a4 = request.session['answer_4']
#
#     q1 = request.session['question_1']
#     q2 = request.session['question_2']
#     q3 = request.session['question_3']
#     q4 = request.session['question_4']
#
#     c1 = request.session['cor_ans_1']
#     c2 = request.session['cor_ans_2']
#     c3 = request.session['cor_ans_3']
#     c4 = request.session['cor_ans_4']
#
#     del request.session['answer_1']
#     del request.session['answer_2']
#     del request.session['answer_3']
#     del request.session['answer_4']
#
#     del request.session['question_1']
#     del request.session['question_2']
#     del request.session['question_3']
#     del request.session['question_4']
#     del request.session['type_exam']
#
#     del request.session['cor_ans_1']
#     del request.session['cor_ans_2']
#     del request.session['cor_ans_3']
#     del request.session['cor_ans_4']
#
#     return render(request,"result.html",{"q1":q1,"q2":q2,"q3":q3,"q4":q4,"c1":c1,"c2":c2,"c3":c3,"c4":c4,"a1":a1,"a2":a2,"a3":a3,"a4":a4,"res":qs1,"res1":qs})
#
#
# def showexamStatus(request):
#     qs2 = Non_Negative_Eaxm.objects.all()
#     res = request.session["semail"]
#     qs1 = Student.objects.filter(emailid=res)
#     qs = Faculty.objects.all()
#     return render(request,"allstatus.html",{"res2":qs2,"res":qs1,"res1":qs})


def examResults(request):
    res = request.session["semail"]
    print(res)
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    qs2 = Non_Negative_Eaxm.objects.all()
    exam = Non_Negative_Eaxm.objects.filter(email=res)
    print(exam)
    neg_exam = Negative_Exam.objects.filter(email=res)
    return render(request,"allexamresults.html",{"data":exam,"data2":neg_exam,"res":qs1,"res1":qs,"res2":qs2})


def postQuestion(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    qs2 = Question.objects.filter(email=res)
    return render(request,"postquestion.html",{"res1":qs,"res":qs1,"res2":qs2})


def requestQuestion(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request,"requestQuestion.html",{"res1":qs,"res":qs1})


def saveQuestion(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    email = request.POST.get("email")
    print(email)
    ques = request.POST.get("question")
    e = Question(question=ques,email=email)
    e.save()
    return render(request,"requestQuestion.html",{"res1":qs,"res":qs1,"msg":"Question posted"})


def viewMessages(request):
    qs = Question.objects.all()
    return render(request,"viewMsg.html",{"res":qs})


def view_Status(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request,"view_status.html",{"res1":qs,"res":qs1})


def see_Status(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    mail = request.POST.get("email2")
    type = request.POST.get("type_mode")
    exam = request.POST.get("exam_mode")
    if exam == "Non-negative":
        qs2 = Non_Negative_Eaxm.objects.filter(email=mail,type=type)
        return render(request,"see_status.html",{"res1":qs,"res":qs1,"data":qs2})
    else:
        qs3 = Negative_Exam.objects.filter(email=mail,type=type)
        return render(request,"see_status.html",{"res1":qs,"res":qs1,"data":qs3})


def exam_Report(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    return render(request, "exam_report.html", {"res1": qs,"res": qs1})


def report_Exam(request):
    res = request.session["semail"]
    qs1 = Student.objects.filter(emailid=res)
    qs = Faculty.objects.all()
    d1 = request.POST.get("d1")
    d2 = request.POST.get("d2")
    exam = request.POST.get("exam_mode")
    if exam == "Non-negative":
        qs2 = Non_Negative_Eaxm.objects.filter(date__range=(d1,d2),email=res)
        return render(request,"report_exam.html",{"res1": qs,"res": qs1,"data":qs2})
    else:
        qs3 = Negative_Exam.objects.filter(date__range=(d1,d2),email=res)
        return render(request,"report_exam.html",{"res1": qs,"res": qs1,"data":qs3})