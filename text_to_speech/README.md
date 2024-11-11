# FreeTextToSpeechApp Documentation
## version: 1.0.0

## Overview
In this project I demonstrate the use of Django Rest Framework to build an application API and how to seamlessly connect it to the frontend for amazing User Interface(UI). Included, is an integration of Google's Text-to-speech (gTTS) engine that leverages on AI to help convert texts to audio.

## Authentication
No authentication is set in this early version. The app allows you to write text and output it immediately as an audio output without needing to access the database.

## Endpoints Overview

### TextToSpeechView
- **URL**: `/api/`
- **Method**: `POST`
- **Description**: Enter text using the form provided and submit it for real-time processing
- **Request Body**:
  ```json
  {
    
    "text": "sample text",
    
  }
  ```
- **Response**: Returns a an audio file containing the converted text.


## Example Usage
### Convert TextToSpeech from your terminal
```bash
curl -X POST http://localhost:8000/api/ \
     -H "Content-Type: application/json" \
     -d '{
           "text": "Hello, this is a test for text-to-speech conversion.",
           "rate": 1.0,
           "volume": 1.0,
           "lang": "en"
         }' \
     --output output.mp3

```

## Error Codes
- **400**: Bad Request — The request could not be understood or was missing required parameters.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.