import re

from rest_framework.serializers import ValidationError


# class DescriptionCourseValidator:
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
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        reg = re.compile('^/((http:\/\/)?(www\.)?youtube.com\S*)/gi')
        if bool(reg.match(tmp_value)):
            raise ValidationError('В материалах не допускаются ссылки на сторонние ресурсы, кроме youtube.com')
