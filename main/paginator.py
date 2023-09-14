from rest_framework.pagination import PageNumberPagination


class MainPaginator(PageNumberPagination):
    page_size = 100
