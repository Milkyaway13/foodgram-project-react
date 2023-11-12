from http import HTTPStatus

from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Subscribe, CustomUser
from .pagination import CustomPageNumberPagination
from api.serializers import (
    SubscribeSerializer,
    SubscriptionsSerializer,
    UserCreateSerializer,
)


class CustomUserViewSet(UserViewSet):
    """Вьюсет для модели User и Subscribe."""

    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        if self.action == "me":
            return (IsAuthenticated(), )
        return super().get_permissions()

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,),
            pagination_class=CustomPageNumberPagination)
    def subscriptions(self, request):
        subscriptions = Subscribe.objects.filter(subscriber=request.user)
        subscribing_users = CustomUser.objects.filter(subscribing__in=subscriptions)
        page = self.paginate_queryset(subscribing_users)
        serializer = SubscriptionsSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, **kwargs):
        author = self.get_object()

        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(subscriber=request.user, author=author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(Subscribe, subscriber=request.user,
                              author=author).delete()
            return Response({'detail': 'Успешная отписка'},
                            status=status.HTTP_204_NO_CONTENT)