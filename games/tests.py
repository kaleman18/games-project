from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Game


class GamesTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_game = Game.objects.create(
            name="call of duty",
            owner=testuser1,
            description="shooter that sucks now",
        )
        test_game.save()

    def test_things_model(self):
        game = Game.objects.get(id=1)
        actual_owner = str(game.owner)
        actual_name = str(game.name)
        actual_description = str(game.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "call of duty")
        self.assertEqual(
            actual_description, "shooter that sucks now"
        )

    def test_get_game_list(self):
        url = reverse("game_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        games = response.data
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0]["name"], "call of duty")

    def test_get_game_by_id(self):
        url = reverse("game_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game = response.data
        self.assertEqual(game["name"], "call of duty")

    def test_create_game(self):
        url = reverse("game_list")
        data = {"owner": 1, "name": "spoon", "description": "good for cereal and soup"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        games = Game.objects.all()
        self.assertEqual(len(games), 2)
        self.assertEqual(Game.objects.get(id=2).name, "spoon")

    def test_update_game(self):
        url = reverse("game_detail", args=(1,))
        data = {
            "owner": 1,
            "name": "call of duty",
            "description": "warzone is okay tho",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game = Game.objects.get(id=1)
        self.assertEqual(game.name, data["name"])
        self.assertEqual(game.owner.id, data["owner"])
        self.assertEqual(game.description, data["description"])

    def test_delete_game(self):
        url = reverse("game_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        games = Game.objects.all()
        self.assertEqual(len(games), 0)