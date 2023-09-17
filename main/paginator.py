from rest_framework.pagination import PageNumberPagination


class MainPaginator(PageNumberPagination):
    """Класс MainPaginator является пагинаторм который, определяет количество объектов на одной странице,
    он наследуется от класса PageNumberPagination"""
    page_size = 100
