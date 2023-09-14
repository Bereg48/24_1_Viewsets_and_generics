from django.contrib import admin

from main.models import Course, Lesson, Pay, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'photo', 'lesson', 'user')
    list_filter = ('user',)
    search_fields = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'photo', 'link_video', 'user')


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_time', 'lesson', 'course', 'payment_amount', 'method_pay')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'updates', 'subscription')
