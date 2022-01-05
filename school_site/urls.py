"""school_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', main, name='main'),
    path('about_school/', about_school, name='about_school'),
    path('courses/', courses, name='courses'),
    path('news/', news, name='news'),
    path('news/<news_id>/', open_news, name='open_news'),
    path('contact/', contact, name='contact'),
    path('search_news/', search_news, name='search_news'),
    path('students_teachers/', students_teachers, name='students_teachers'),
    path('login/', login_profile, name='login'),
    path('logout/', logout_profile, name='logout'),
    path('register/', register, name='register'),
    path('info_user/', info_user, name='info_user'),
    path('register/<status_id>/', register_second_stage, name='register_second_stage'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)