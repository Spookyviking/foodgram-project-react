import django_filters
from django_filters.rest_framework import (
    AllValuesMultipleFilter,
    BooleanFilter,
    filters,)

from recipes.models import Ingredient, Recipe  # , Tag
from users.models import User, ShoppingCart


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )

    class Meta:
        model = Ingredient
        fields = ["name"]


class RecipeFilter(django_filters.FilterSet):
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='get_is_in_shopping_cart')
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(
        to_field_name="id", queryset=User.objects.all()
    )
    # tags = filters.ModelMultipleChoiceFilter(
    #     field_name="tags__slug",
    #     to_field_name="slug",
    #     queryset=Tag.objects.all(),
    # )
    # is_favorited = filters.BooleanFilter(
    #     field_name="favorite__favorite",
    #     method="filter_favorite_or_shopping_cart",
    # )
    # is_in_shopping_cart = filters.BooleanFilter(
    #     field_name="favorite__shopping_cart",
    #     method="filter_favorite_or_shopping_cart",
    # )

    class Meta:
        model = Recipe
        fields = ["author", "tags", "is_favorited", "is_in_shopping_cart"]

    # def filter_favorite_or_shopping_cart(self, queryset, name, value):
    #     if value:
    #         return queryset.filter(
    #             favorite__user=self.request.user, **{name: value}
    #         ).all()

    #     return queryset.exclude(
    #         favorite__user=self.request.user, **{name: True}
    #     ).all()
    def get_is_favorited(self, queryset, name, value):
        if not value:
            return queryset
        favorites = self.request.user.favorites.all()
        return queryset.filter(
            pk__in=(favorite.recipe.pk for favorite in favorites)
        )

    def get_is_in_shopping_cart(self, queryset, name, value):
        if not value:
            return queryset
        try:
            recipes = (
                self.request.user.shopping_cart.recipes.all()
            )
        except ShoppingCart.DoesNotExist:
            return queryset
        return queryset.filter(
            pk__in=(recipe.pk for recipe in recipes)
        )
