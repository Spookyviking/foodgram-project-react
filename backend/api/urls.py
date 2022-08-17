from django.urls import include, path
from rest_framework import routers

from api.views import IngredientsViewSet, RecipeViewSet, TagViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router_v1.urls)),
]
