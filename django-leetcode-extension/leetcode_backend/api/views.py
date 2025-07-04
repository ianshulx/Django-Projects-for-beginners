from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
from django.conf import settings
    
# Create your views here.

genai.configure(api_key=settings.GEMINI_API_KEY)
@csrf_exempt
def solve_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get("title")
        url = data.get("url")
        print(f"Received: {title}, {url}")
            
        prompt = f"""
        You're an expert LeetCode mentor. A user is working on the problem titled: "{title}" ({url}).
        Give them clear, step-by-step guidance to solve it — including edge cases, brute-force thinking, and optimization ideas.
        DO NOT write or suggest actual code.
        Only provide strategic help in natural language.
        """

        
        model = genai.GenerativeModel("models/gemini-1.5-flash")  
        response = model.generate_content(prompt)
        answer = response.text

    
        steps = answer.strip().split("\n")
        steps = [step.strip() for step in steps if step.strip()]

        return JsonResponse({"steps": steps})

    return JsonResponse({"error": "Only POST allowed"}, status=400)
