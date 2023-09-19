from rest_framework.pagination import PageNumberPagination


class MainPaginator(PageNumberPagination):
    """Класс MainPaginator является пагинаторм который, определяет количество объектов на одной странице,
    он наследуется от класса PageNumberPagination"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
