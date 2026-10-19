import json

from django.test import Client, TestCase

from .models import FlashCard


class FlashCardApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        FlashCard.objects.create(question="2+2?", answer="4")
        FlashCard.objects.create(question="Capital of NL?", answer="Amsterdam")

    def test_list_cards(self):
        resp = self.client.get("/api/flash/cards/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data["cards"]), 2)
        self.assertEqual(data["cards"][0]["question"], "2+2?")

    def test_detail_found(self):
        resp = self.client.get("/api/flash/cards/1/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["answer"], "4")

    def test_detail_not_found(self):
        resp = self.client.get("/api/flash/cards/999/")
        self.assertEqual(resp.status_code, 404)

    def test_create_card(self):
        resp = self.client.post(
            "/api/flash/cards/create/",
            data=json.dumps({"question": "New?", "answer": "Yes"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(FlashCard.objects.count(), 3)

    def test_create_card_missing_fields(self):
        resp = self.client.post(
            "/api/flash/cards/create/",
            data=json.dumps({"question": "New?"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_create_card_non_object_body(self):
        resp = self.client.post(
            "/api/flash/cards/create/",
            data=json.dumps([{"question": "q", "answer": "a"}]),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_create_card_non_string_field(self):
        resp = self.client.post(
            "/api/flash/cards/create/",
            data=json.dumps({"question": 123, "answer": "a"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_create_card_invalid_json(self):
        resp = self.client.post(
            "/api/flash/cards/create/",
            data="not json{",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_create_card_too_long(self):
        resp = self.client.post(
            "/api/flash/cards/create/",
            data=json.dumps({"question": "q" * 501, "answer": "a"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_update_card(self):
        resp = self.client.put(
            "/api/flash/cards/1/update/",
            data=json.dumps({"answer": "five"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(FlashCard.objects.get(id=1).answer, "five")

    def test_delete_card(self):
        resp = self.client.delete("/api/flash/cards/2/update/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(FlashCard.objects.count(), 1)
