from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recepie.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL = reverse('recepie:recipe-list')


def detail_url(recipe_id)
    return reverse('recepie:recipe-detail', args=[recipe_id])


def sample_tag(user, name="Main course"):
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name="Cinnamon"):
    return Ingredient.objects.create(user=user, name=name)


def sample_recepie(user, **params):
    defaults = {
        'title': 'Sample recepie',
        'time_minutes': 10,
        'price': 5.00,
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecepieApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecepieApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@email.com',
            'P@$$w0rd'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recepies(self):
        sample_recepie(self.user)
        sample_recepie(self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recepies_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'user2@email.com',
            'P@$$w0rd'
        )

        sample_recepie(user2)
        sample_recepie(self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        recipe = sample_recepie(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recepie.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)
