"""URL mapping for the recipe app."""

#So this is the default router that provided by the Django rest framework
# and you can use this with an API view to automatically create routes for
# all of the different options available for that view.

# we create a default router

# now we register our viewset with that router with the name recipes.
# we are using modelviewset which is why the recipeviewset will support all methods for create, read, update, delete.

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]