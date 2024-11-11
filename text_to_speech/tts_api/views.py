from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from gtts import gTTS
import tempfile
from django.http import HttpResponse

class TextToSpeechView(APIView):
    def post(self, request):
        # Retrieve the 'text' input from the POST request data
        text = request.data.get('text')
        
        if not text:
            return Response({"error": "Text parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve user settings for rate, volume, and language
        rate = float(request.data.get('rate', 1.0))  # Default rate is 1.0
        volume = float(request.data.get('volume', 5.0))  # Default volume is 1.0
        language = request.data.get('lang', 'en')  # Default language is 'en'

        # Check if the rate is within an acceptable range (0.1 to 3.0 for gTTS)
        if rate < 0.1 or rate > 2.0:
            return Response({"error": "Invalid rate. It must be between 0.1 and 3.0."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the volume is within an acceptable range (0.0 to 1.0 for gTTS)
        if volume < 0.0 or volume > 10.0:
            return Response({"error": "Invalid volume. It must be between 0.0 and 1.0."}, status=status.HTTP_400_BAD_REQUEST)

        # Map rate to the 'slow' parameter in gTTS
        slow = rate < 1.0  # If rate is less than 1, consider it slow speech
        
        # Generate speech using Google TTS with user-specified language and slow speed
        tts = gTTS(text=text, lang=language, slow=slow)  # Using the slow parameter to control speed

        # Save speech to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            tts.save(temp_audio.name)
            
            with open(temp_audio.name, 'rb') as f:
                audio_data = f.read()
            
            response = HttpResponse(audio_data, content_type='audio/mp3')
            response['Content-Disposition'] = 'inline; filename="audio.mp3"'  # Inline to play in the browser
            return response
