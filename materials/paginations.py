from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Пагинация на уровне страниц"""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
