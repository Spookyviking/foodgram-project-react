from django.urls import include, path
from rest_framework import routers

from api.views import IngredientsViewSet, RecipeViewSet, TagViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router_v1.urls)),
]
