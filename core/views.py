from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.forms import *

from core.models import News, Status, Student, Teacher


def main(request):
    request.session['path'] = request.path
    news = News.objects.all().order_by('-released_date')[:3]
    return render(request, 'index.html', {'news': news})


def news(request):
    request.session['path'] = request.path
    news = News.objects.all().order_by('-released_date')
    three_last_news = News.objects.all().order_by('-released_date')[:3]
    pagin = Paginator(news, 6)
    page = request.GET.get('page', None)
    if page is None:
        combine_pagin_news = pagin.get_page(1)
    else:
        combine_pagin_news = pagin.get_page(page)
    return render(request, 'blog.html', {'news': combine_pagin_news, 'three_last_news': three_last_news})


def search_news(request):
    request.session['path'] = request.path
    if request.method == 'POST':
        title = request.POST.get('title', None)
        title = title[0].upper() + title[1:len(title)]
        print(title)
        news = News.objects.filter(title__icontains=title)
        three_last_news = News.objects.all().order_by('-released_date')[:3]
        pagin = Paginator(news, 6)
        page = request.GET.get('page', None)
        if page is None:
            combine_pagin_news = pagin.get_page(1)
        else:
            combine_pagin_news = pagin.get_page(page)
        return render(request, 'blog.html', {'news': combine_pagin_news, 'three_last_news': three_last_news})
    return redirect('/news/')


def open_news(request, news_id):
    request.session['path'] = request.path
    news = News.objects.get(id=news_id)
    two_last_news = News.objects.all().order_by('-released_date')[:2]
    return render(request, 'single-post.html', {'news': news, 'two_last_news': two_last_news})


def about_school(request):
    request.session['path'] = request.path
    return render(request, 'about.html', {})


def courses(request):
    request.session['path'] = request.path
    return render(request, 'courses.html', {})


def contact(request): 
    request.session['path'] = request.path
    return render(request, 'contact.html', {})


def login_profile(request):
    if request.method == 'POST' and not request.user.is_authenticated:
        path = request.session['path']
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data['username']
            password = form_login.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(path)
        messages.error(request, 'Не существует пользователь или неправильный пароль')
    
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_profile(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def info_user(request):
    if request.user.is_authenticated:
        print(request.user.status)
        if request.user.status is not None:
            if request.user.status.id == 1 or request.user.status.id == 3:
                person = Teacher.objects.get(user=request.user)
            elif request.user.status.id == 2:
                person = Student.objects.get(user=request.user)  
            else:
                person = request.user
        else:
                person = request.user
        return render(request, 'info_user.html', {'person': person})
    return redirect('/')


def register(request):
    if not request.user.is_authenticated:
        status = Status.objects.all()
        return render(request, 'register_first_stage.html', {'statuses': status})
    return redirect('/')


def register_second_stage(request, status_id):
    if not request.user.is_authenticated:
        status_id = int(status_id)
        if status_id == 1 or status_id == 3:
            return register_teacher(request, status_id)
        elif status_id == 2:
            return register_student(request, status_id)
        elif status_id == 4:
            return register_principal(request, status_id)

    return redirect('/')



def register_principal(request, status_id):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            key = request.POST.get('key', None)
            real_key = Secret_key.objects.get(id=status_id)
            if str(key) == str(real_key.key):
                form = RegistretionForm(request.POST)
                if form.is_valid():
                    instance = form.save(commit=False)
                    status = Status.objects.get(id=status_id)
                    instance.status = status
                    instance.save()
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password2']
                    user = authenticate(username=username, password=password)
                    if user:
                        login(request, user)
                        return redirect('/')
                else:

                    messages.error(request, form.errors)
            else:
                messages.error(request, 'Не верный ключ!')

        form = RegistretionForm()
        return render(request, 'registretion_user.html', {'form': form, 'status_id': status_id})
    else:
        return redirect('/')


def register_student(request, status_id):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            key = request.POST.get('key', None)
            real_key = Secret_key.objects.get(id=status_id)
            if str(key) == str(real_key.key):
                form = RegistretionForm(request.POST)
                if form.is_valid():
                    instance = form.save(commit=False)
                    status = Status.objects.get(id=status_id)
                    instance.status = status
                    instance.save()
                    group = Group.objects.get(id=request.POST.get('group'))
                    new_student = Student.objects.create(user=instance, group=group)
                    tmp_grpup = Group.objects.get(id=request.POST.get('group'))
                    tmp_grpup.students.add(new_student)
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password2']
                    user = authenticate(username=username, password=password)
                    if user:
                        login(request, user)
                        return redirect('/')
                else:

                    messages.error(request, form.errors)
            else:
                messages.error(request, 'Не верный ключ!')

        form = RegistretionForm()
        form2 = StudentForm()
        return render(request, 'registretion_student.html', {'form': form, 'form2': form2, 'status_id': status_id})
    else:
        return redirect('/')


def register_teacher(request, status_id):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            key = request.POST.get('key', None)
            real_key = Secret_key.objects.get(status__id=status_id)
            if str(key) == str(real_key.key):
                form = RegistretionForm(request.POST)
                if form.is_valid():
                    instance = form.save(commit=False)
                    status = Status.objects.get(id=status_id)
                    instance.status = status
                    instance.save()

                    form2 = TeacherForm(request.POST)
                    print(request.POST.get('group'))
                    if form2.is_valid():

                        instance2 = form2.save(commit=False)
                        instance2.user = instance
                        instance2.save()
                        for subject in request.POST.getlist('subject'):
                            instance2.subject.add(Subject.objects.get(id=subject))
                        if request.POST.getlist('group', None) is not None:      
                            for group in request.POST.getlist('group'):
                                tmp_group = Group.objects.get(id=group)
                                if tmp_group.teacher_user is None:    
                                    instance2.group.add(Group.objects.get(id=group))
                                    instance2.save()
                                    tmp_group.teacher_user = instance2
                                    tmp_group.save()
                                else:
                                   messages.error(request, f'Класс {tmp_group.title} имеет руководителя {tmp_group.teacher_user}')
                                   instance2.delete() 
                                   instance.delete()
                                   

                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password2']
                        user = authenticate(username=username, password=password)
                        if user:
                            login(request, user)
                            return redirect('/')
                    else:
                        messages.error(request, form.errors)
                        print(form.errors)
                        return redirect('/')
                else:
                    print(form.errors)
                    messages.error(request, form.errors)
            else:
                messages.error(request, 'Не верный ключ!')

        form = RegistretionForm()
        form_teacher = TeacherForm()
        return render(request, 'registretion_teacher.html', {'form': form, 'form2': form_teacher, 'status_id': status_id})

    else:
        return redirect('/')


def students_teachers(request):
    group = Group.objects.all()
    subject = Subject.objects.all()
    teacher = Teacher.objects.all()
    principal = NewUser.objects.filter(status__id=4)
    head_teacher = Teacher.objects.filter(user__status__id=3)

    return render(request, 'students_teachers.html', {'subjects': subject,'groups': group, 'teachers': teacher, 'principals': principal, 'head_teachers': head_teacher})
# Create your views here.
