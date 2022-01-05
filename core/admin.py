from django.contrib import admin
from django.db.models import fields
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, widgets
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.db.models import Q


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('username', 'name')
    list_filter = ('status', 'is_superuser')
    ordering = ('-start_date',)
    list_display = ('username', 'name', 'status', 'phone_number',)
    fieldsets = (
        (None, {'fields': ('username', 'name', 'status', 'phone_number', 'is_superuser', 'password')},
         ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'status', 'phone_number', 'password1', 'password2', 'is_superuser')}
         ),
    )



admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Status)
admin.site.register(Subject)


@admin.register(Secret_key)
class Secret_keyAdmin(admin.ModelAdmin):
    list_display = ['status', 'key']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('show_username', 'show_name', 'group', 'show_phone_number')

    def show_username(self, obj):
        return f'{obj.user.username}'

    def show_name(self, obj):
        return f'{obj.user.name}'

    def show_phone_number(self, obj):
        return f'{obj.user.phone_number}'

    show_name.short_description = 'Имя и фамилия'
    show_username.short_description = 'Имя пользователя'

    search_fields = ('user__icontains',)
    list_filter = ['group']


    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.user.portret.url}" alt="" width="75" class="portret">')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = NewUser.objects.filter(status__id=2)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher_user']
    search_fields = ('title__icontains',)


class NewsAdminForm(forms.ModelForm):
    first_information = forms.CharField(label='Первая часть информация', widget=CKEditorUploadingWidget())
    second_information = forms.CharField(label='Вторая часть информация', widget=CKEditorUploadingWidget(), required=False)
    third_information = forms.CharField(label='Третья часть информация', widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = News
        fields = '__all__'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'released_date', 'author']
    search_fields = ('title__icontains',)
    form = NewsAdminForm


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('show_username', 'show_name', 'show_status', 'show_phone_number', 'get_group')
    list_filter = ['subject']
    def show_username(self, obj):
            return f'{obj.user.username}'

    def show_name(self, obj):
        return f'{obj.user.name}'

    def show_phone_number(self, obj):
        return f'{obj.user.phone_number}'

    def show_status(self, obj):
        return f'{obj.user.status.title}'

    def get_group(self, obj):
        return "\n".join([p.title for p in obj.group.all()])

    show_name.short_description = 'Имя и фамилия'
    show_username.short_description = 'Имя пользователя'
    show_phone_number.short_description = 'Номер телефона'
    show_status.short_description = 'Статус'
    get_group.short_description = 'Классы'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = NewUser.objects.filter(Q(status__id=1) | Q(status__id=3))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.site_title = 'Администрация'
admin.site.site_header = 'Администрация и контроль данных'
# Register your models here.
