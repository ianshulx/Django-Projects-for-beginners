import json
import logging

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@csrf_exempt
def chatbot(request):
    if request.method == "GET":
        return render(request, "chat.html")

    try:
        body = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    user_message = body.get("message", "").strip()

    if not user_message:
        return JsonResponse({"error": "Message cannot be empty."}, status=400)

    role_message = (
        body.get("role", "").strip()
        or getattr(settings, "DEFAULT_BOT_ROLE", "You are a nasty lover.")
    )

    api_key = getattr(settings, "OPENROUTER_API_KEY", None)

    if not api_key:
        logger.error("OPENROUTER_API_KEY is missing.")
        return JsonResponse(
            {"error": "OpenRouter API key is not configured."},
            status=500,
        )

    model = getattr(
        settings,
        "OPENROUTER_MODEL",
        "openai/gpt-4.1-mini",
    )

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": role_message,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        "temperature": 0.7,
        "max_tokens": 300,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",

        # Recommended by OpenRouter
        "HTTP-Referer": "http://127.0.0.1:8000",
        "X-Title": "Django Chatbot",
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )

    except requests.exceptions.ConnectionError:
        logger.exception("Unable to connect to OpenRouter.")
        return JsonResponse(
            {
                "error": "Cannot connect to OpenRouter. Check your internet connection."
            },
            status=502,
        )

    except requests.exceptions.Timeout:
        logger.exception("OpenRouter request timed out.")
        return JsonResponse(
            {"error": "The AI service took too long to respond."},
            status=504,
        )

    except requests.RequestException as exc:
        logger.exception(exc)
        return JsonResponse(
            {"error": "An unexpected network error occurred."},
            status=502,
        )

    print("=" * 80)
    print("STATUS:", response.status_code)
    print("BODY:")
    print(response.text)
    print("=" * 80)

    if response.status_code != 200:
        try:
            error = response.json()
        except Exception:
            error = response.text

        logger.error(error)

        return JsonResponse(
            {
                "error": "OpenRouter API Error",
                "details": error,
            },
            status=response.status_code,
        )

    try:
        data = response.json()

        ai_reply = (
            data["choices"][0]["message"]["content"].strip()
        )

        if not ai_reply:
            ai_reply = "The AI returned an empty response."

        return JsonResponse(
            {
                "reply": ai_reply,
            }
        )

    except Exception as exc:
        logger.exception(exc)

        return JsonResponse(
            {
                "error": "Failed to parse OpenRouter response.",
                "raw_response": response.text,
            },
            status=500,
        )