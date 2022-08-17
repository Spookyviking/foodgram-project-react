from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from core.models import CreatedModel
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        "Название",
        max_length=100,
    )
    measurement_unit = models.CharField(
        "Ед.изм.",
        max_length=10,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        "Название",
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        "slug",
        max_length=50,
        unique=True,
    )
    color = ColorField(
        "Цветовой код",
        default="#FF0000",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="recipe",
    )
    name = models.CharField(
        "Название",
        max_length=100,
    )
    image = models.ImageField(
        "Картинка",
        upload_to="recipes/images/",
        help_text="Загрузите картинку",
    )
    text = models.TextField(
        "Описание",
        help_text="Введите описание рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientsInRecipes",
        related_name="recipes",
    )
    tags = models.ManyToManyField(
        Tag,
        through="RecipesTags",
        related_name="recipes",
    )
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовления, минуты",
        validators=(
            MinValueValidator(
                1, message="Минимальное время приготовления - 1 мин."
            ),
        ),
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=("author", "name",), name="unique_author_name"
            )
        ]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def get_absolute_url(self):
        return f"/posts/{self.pk}/"

    def __str__(self):
        return self.name[:15]


class FavoriteRecipe(CreatedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="favorite",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="favorite",
    )
    favorite = models.BooleanField("Избранное", default=False)
    shopping_cart = models.BooleanField(
        "Корзина покупок",
        default=False,
    )

    class Meta:
        ordering = ("-created",)
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe",), name="unique_user_recipe"
            ),
        )
        verbose_name = "Рецепт в избранных или в списке покупок"
        verbose_name_plural = "Рецепты в избранных или в списке покупок"


class IngredientsInRecipes(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredient_in_recipe",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_in_recipe",
    )
    amount = models.PositiveSmallIntegerField(
        "Кол-во ингредиента",
        validators=(
            MinValueValidator(
                1, message="Убедитесь, что это значение больше либо равно 1."
            ),
        ),
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Ингредиент в рецепт"
        verbose_name_plural = "Ингредиент в рецепт"
        constraints = (
            models.UniqueConstraint(
                fields=("ingredient", "recipe"),
                name="ingredient_recipe_relations",
            ),
        )

    def __str__(self):
        return f"{self.ingredient.name}, {self.recipe.name}"


class RecipesTags(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="tag",
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="recipe",
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Тег рецепта"
        verbose_name_plural = "Тeги рецептов"

    def __str__(self):
        return f"{self.tag.name}, {self.recipe.name}"
