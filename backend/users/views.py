from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import PageLimitPagination
from api.serializers import SubscribeSerializer, UserReadSerializer

from .models import CustomUser, Subscribe


class CustomUserViewSet(UserViewSet):
    """Вьюсет для модели User и Subscribe."""

    serializer_class = UserReadSerializer
    pagination_class = PageLimitPagination

    @action(
        detail=False,
        methods=("get",),
        pagination_class=None,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = UserReadSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
        pagination_class=PageLimitPagination,
    )
    def subscriptions(self, request):
        subscriptions = Subscribe.objects.filter(subscriber=request.user)
        subscribing_users = CustomUser.objects.filter(
            subscribing__in=subscriptions
        )
        serializer = SubscribeSerializer(
            self.paginate_queryset(subscribing_users),
            many=True,
            context={"request": request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, **kwargs):
        author_id = self.kwargs.get("id")
        author = get_object_or_404(CustomUser, id=author_id)

        if request.method == "POST":
            if request.user == author:
                return Response(
                    {"detail": "Вы не можете подписаться на себя."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = SubscribeSerializer(
                author, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                if Subscribe.objects.filter(
                    subscriber=request.user, author=author
                ).exists():
                    return Response(
                        {"detail": "Вы уже подписаны на этого пользователя."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                Subscribe.objects.create(
                    subscriber=request.user, author=author
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )

        get_object_or_404(
            Subscribe, subscriber=request.user, author=author
        ).delete()
        return Response(
            {"detail": "Успешная отписка"}, status=status.HTTP_204_NO_CONTENT
        )
