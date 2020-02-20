from django.urls import include, path

from recepie import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)

app_name = 'recepie'

urlpatterns = [
    path('', include(router.urls))
]
