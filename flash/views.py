import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import FlashCard

MAX_TEXT_LEN = 500


class BadBody(Exception):
    """Raised when a request body is not a valid JSON object."""


def _json_body(request):
    """Parse the request body into a dict of string values; raise BadBody."""
    try:
        data = json.loads(request.body or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise BadBody("invalid json")
    if not isinstance(data, dict):
        raise BadBody("json object required")
    for key in ("question", "answer"):
        if key in data and not isinstance(data[key], str):
            raise BadBody(f"{key} must be a string")
    return data


def _body_error(exc):
    return JsonResponse({"error": str(exc)}, status=400)


def list_cards(request):
    cards = [card.to_dict() for card in FlashCard.objects.all()]
    return JsonResponse({"cards": cards})


def card_detail(request, card_id):
    try:
        card = FlashCard.objects.get(id=card_id)
    except FlashCard.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)
    return JsonResponse(card.to_dict())


@csrf_exempt
@require_http_methods(["POST"])
def create_card(request):
    try:
        data = _json_body(request)
    except BadBody as exc:
        return _body_error(exc)
    question = (data.get("question") or "").strip()
    answer = (data.get("answer") or "").strip()
    if not question or not answer:
        return JsonResponse({"error": "question and answer required"}, status=400)
    if len(question) > MAX_TEXT_LEN or len(answer) > MAX_TEXT_LEN:
        return JsonResponse({"error": f"max length is {MAX_TEXT_LEN}"}, status=400)
    card = FlashCard.objects.create(question=question, answer=answer)
    return JsonResponse(card.to_dict(), status=201)


@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def update_card(request, card_id):
    try:
        card = FlashCard.objects.get(id=card_id)
    except FlashCard.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)

    if request.method == "DELETE":
        card_id_val = card.id
        card.delete()
        return JsonResponse({"deleted": card_id_val})

    try:
        data = _json_body(request)
    except BadBody as exc:
        return _body_error(exc)

    if data.get("question") is not None:
        question = data["question"].strip()
        if question:
            if len(question) > MAX_TEXT_LEN:
                return JsonResponse(
                    {"error": f"max length is {MAX_TEXT_LEN}"}, status=400
                )
            card.question = question
    if data.get("answer") is not None:
        answer = data["answer"].strip()
        if answer:
            if len(answer) > MAX_TEXT_LEN:
                return JsonResponse(
                    {"error": f"max length is {MAX_TEXT_LEN}"}, status=400
                )
            card.answer = answer
    card.save()
    return JsonResponse(card.to_dict())
