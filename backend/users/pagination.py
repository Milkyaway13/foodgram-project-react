from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageLimitPagination(PageNumberPagination):
    page_size_query_param = "limit"


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 1

    def get_paginated_response(self, data):
        """Паджинатор для Users."""
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )