import re

from rest_framework.serializers import ValidationError


# class DescriptionCourseValidator:
"""Класс DescriptionCourseValidator валидирует данные получаемые в соответсвии с заданной моделью класса Course, 
    данный класс водирирует в соответсвубщем сериализаторе поле description"""
#
#     def __init__(self, field):
#         self.field = field
#
#     def __call__(self, value):
#         tmp_value = dict(value).get(self.field)
#         reg = re.compile('^/((http:\/\/)?(www\.)?youtube.com\S*)/gi')
#         if bool(reg.match(tmp_value)):
#             raise ValidationError('В материалах не допускаются ссылки на сторонние ресурсы, кроме youtube.com')


class DescriptionLessonValidator:
    """Класс DescriptionLessonValidator валидирует данные получаемые в соответсвии с заданной моделью класса Lesson,
    данный класс водирирует в соответсвубщем сериализаторе поле link_video"""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        reg = re.compile('^/((http:\/\/)?(www\.)?youtube.com\S*)/gi')
        if bool(reg.match(tmp_value)):
            raise ValidationError('В материалах не допускаются ссылки на сторонние ресурсы, кроме youtube.com')
