from django.db import models
from django.db.models.base import Model
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class News(models.Model):

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    title = models.CharField(max_length=255, verbose_name='Тема')
    first_information = models.TextField(verbose_name='Первая часть информация')
    second_information = models.TextField(verbose_name='Вторая часть информация', blank=True, null=True)
    third_information = models.TextField(verbose_name='Третья часть информация', blank=True, null=True)
    released_date = models.DateTimeField(default=timezone.now, verbose_name='Дата анонсирование')
    first_picture = models.ImageField(upload_to='images/', verbose_name='Первая картина')
    second_picture = models.ImageField(upload_to='images/', verbose_name='Вторая картина', blank=True, null=True)
    third_picture = models.ImageField(upload_to='images/', verbose_name='Третья картина', blank=True, null=True)
    author = models.ForeignKey('NewUser', on_delete=models.RESTRICT, null=True, verbose_name='Автор')

    def __str__(self):
        return self.title


class Status(models.Model):
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статус'

    title = models.CharField(max_length=150, verbose_name='Статус')

    def __str__(self):
        return f'{self.title}'


class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, username, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(username, name, password, **other_fields)

    def create_user(self, username, name, password, **other_fields):

        user = self.model(username=username,
                          name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователи'

    username = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')
    name = models.CharField(max_length=150, blank=True, verbose_name='Имя и фамилия')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, null=True, verbose_name='Статус')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона', null=True)
    start_date = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False, verbose_name='Статус администратора')
    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.name} - {self.username}'        


class Subject(models.Model):
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    title = models.CharField(max_length=255, verbose_name='Наименование предмета')

    def __str__(self):
        return self.title
        

class Teacher(models.Model):
    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    user = models.ForeignKey('NewUser', verbose_name='Учитель(-ница)', on_delete=models.PROTECT,
                             help_text='Пользователь')
    group = models.ManyToManyField('Group', verbose_name='Руководимые классы', blank=True)
    subject = models.ManyToManyField('Subject', verbose_name='Предметы которые обучаете')

    def __str__(self):
        return f'{self.user.name}'      


class Group(models.Model):

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    title = models.CharField(max_length=50, verbose_name='Название класса')
    teacher_user = models.ForeignKey('Teacher', verbose_name='Классный руководитель', on_delete=models.PROTECT, null=True, related_name='teacher', blank=True)
    students = models.ManyToManyField('Student', verbose_name='Ученики', related_name='related_students', blank=True) 

    def __str__(self):
        return self.title


class Student(models.Model):
    class Meta:
        verbose_name = 'Ученик(-ца)'
        verbose_name_plural = 'Ученики'

    user = models.ForeignKey('NewUser', verbose_name='Ученик(-ца)', on_delete=models.PROTECT)
    group = models.ForeignKey('Group', verbose_name='Класс ученика(-цы)', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.user.name}'
    

class Secret_key(models.Model):

    class Meta:
        verbose_name = 'Ключ для регистрации'
        verbose_name_plural = 'Ключи для регистрации'

    key = models.CharField(max_length=10, verbose_name='Ключ', help_text='Придумайте код из 10-ти цифр')
    status = models.ForeignKey('Status', on_delete=models.PROTECT, null=True, verbose_name='Кляч для ....')

    def __str__(self):
        return f'{self.status.title}'

# Create your models here.
