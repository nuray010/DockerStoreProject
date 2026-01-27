from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination


class CategoryPagination(PageNumberPagination):
    page_size = 2


class ProductPagination(PageNumberPagination):
    page_size = 2