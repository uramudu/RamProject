from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=50)
    emailid = models.EmailField(max_length=50,primary_key=True)
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=20,choices=(('male','MALE'),('female','FEMALE'),('other','OTHERS')))
    contact_no = models.IntegerField()
    qualification = models.CharField(max_length=50)
    course = models.CharField(max_length=80,choices=(('java','JAVA'),('python','PYTHON'),('sql','SQL')))
    experience = models.IntegerField()
    address = models.TextField(max_length=200)


class Faculty(models.Model):
    name = models.CharField(max_length=50)
    emailid = models.EmailField(max_length=50,primary_key=True)
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=20,choices=(('male','MALE'),('female','FEMALE'),('other','OTHERS')))
    contact_no = models.IntegerField()
    qualification = models.CharField(max_length=50)
    skils = models.CharField(max_length=80)
    experience = models.IntegerField()
    address = models.TextField(max_length=200)


class Creater(models.Model):
    adminemail = models.CharField(primary_key=True,max_length=50)
    admilpass = models.CharField(max_length=50)


class Non_Negative_Eaxm(models.Model):
    question = models.CharField(max_length=50)
    correct_ans = models.CharField(max_length=50)
    answer = models.CharField(max_length=50)
    type = models.CharField(max_length=30)
    date = models.DateField()
    status = models.CharField(max_length=50)
    marks = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)


class Negative_Exam(models.Model):
    question = models.CharField(max_length=50)
    correct_ans = models.CharField(max_length=50)
    answer = models.CharField(max_length=50)
    type = models.CharField(max_length=30)
    date = models.DateField()
    status = models.CharField(max_length=50)
    marks = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)


class Question(models.Model):
    question = models.CharField(max_length=200)
    email = models.CharField(max_length=200)


