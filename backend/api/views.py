from http import HTTPStatus

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from foodgram.settings import FILE_NAME
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag

from .filters import IngredientFilter, RecipeFilter
from .pagination import PageLimitPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeIngredient,
    RecipeReadSerializer,
    RecipeSmallSerializer,
    TagSerializer,
)


class TagViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    """Вьюсет тэгов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    """Вьюсет ингредиентов."""

    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""

    queryset = Recipe.objects.all()
    pagination_class = PageLimitPagination
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        ("post", "delete"),
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == "POST":
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    "Рецепт уже есть в избранном.",
                    status=HTTPStatus.BAD_REQUEST,
                )
            serializer = FavoriteSerializer(
                data={"user": user.id, "recipe": recipe.id},
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)

        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                "Рецепта нет в избранном.",
                status=HTTPStatus.NOT_FOUND,
            )
        Favorite.objects.filter(user=user, recipe=recipe).delete()
        return Response(
            "Рецепт успешно удалён из избранного.",
            status=HTTPStatus.NO_CONTENT,
        )

    @action(
        ("post", "delete"),
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs["pk"])

        if request.method == "POST":
            serializer = RecipeSmallSerializer(
                recipe, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            if not ShoppingCart.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                ShoppingCart.objects.create(user=request.user, recipe=recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                {"errors": "Рецепт уже в списке покупок."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        get_object_or_404(
            ShoppingCart, user=request.user, recipe=recipe
        ).delete()
        return Response(
            {"detail": "Рецепт успешно удален из списка покупок."},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request, **kwargs):
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_recipe__user=request.user
            )
            .select_related("ingredient")
            .annotate(total_amount=Sum("amount"))
            .values_list(
                "ingredient__name",
                "total_amount",
                "ingredient__measurement_unit",
            )
        )
        file_list = []
        [
            file_list.append("{} - {} {}.".format(*ingredient))
            for ingredient in ingredients
        ]
        file = HttpResponse(
            "Cписок покупок:\n" + "\n".join(file_list),
            content_type="text/plain",
        )
        file["Content-Disposition"] = f"attachment; filename={FILE_NAME}"
        return file
