import django_filters
from django.db.models import IntegerField, Value
from django_filters.rest_framework import (
    CharFilter,
    filters,
    FilterSet
)

from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class RecipeFilter(django_filters.FilterSet):
    author = filters.ModelChoiceFilter(
        to_field_name="id", queryset=User.objects.all()
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.BooleanFilter(
        field_name="favorite__favorite",
        method="filter_favorite_or_shopping_cart",
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name="favorite__shopping_cart",
        method="filter_favorite_or_shopping_cart",
    )

    class Meta:
        model = Recipe
        fields = ("author", "tags", "is_favorited", "is_in_shopping_cart",)

    def filter_favorite_or_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(
                favorite__user=self.request.user, **{name: value}
            ).all()

        return queryset.exclude(
            favorite__user=self.request.user, **{name: True}
        ).all()


class IngredientSearchFilter(FilterSet):
    name = CharFilter(method='search_by_name')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def search_by_name(self, queryset, name, value):
        if not value:
            return queryset
        start_with_queryset = (
            queryset.filter(name__istartswith=value).annotate(
                order=Value(0, IntegerField())
            )
        )
        contain_queryset = (
            queryset.filter(name__icontains=value).exclude(
                pk__in=(ingredient.pk for ingredient in start_with_queryset)
            ).annotate(
                order=Value(1, IntegerField())
            )
        )
        return start_with_queryset.union(contain_queryset).order_by('order')
