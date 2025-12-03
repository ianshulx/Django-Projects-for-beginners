from django.shortcuts import render

# Create your views here.
# downloader/views.py
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseBadRequest
import requests
from urllib.parse import urlparse
import os

# Optional: restrict domains if you want
ALLOWED_DOMAINS = set()  # leave empty to allow all direct URLs (careful)

def is_allowed_domain(url):
    if not ALLOWED_DOMAINS:
        return True
    try:
        netloc = urlparse(url).netloc.lower()
        return any(netloc.endswith(d) for d in ALLOWED_DOMAINS)
    except Exception:
        return False

def stream_video_from_url(request):
    if request.method == "GET":
        return render(request, "downloader/form.html")

    video_url = request.POST.get("video_url", "").strip()
    if not video_url:
        return HttpResponseBadRequest("Video URL required.")

    if not is_allowed_domain(video_url):
        return HttpResponseBadRequest("Domain not allowed. Use trusted direct URLs only.")

    try:
        r = requests.get(video_url, stream=True, timeout=15)
        r.raise_for_status()
    except Exception as e:
        return HttpResponseBadRequest(f"Failed to fetch video: {e}")

    parsed = urlparse(video_url)
    filename = os.path.basename(parsed.path) or "video.mp4"

    def stream_generator(resp):
        try:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk
        finally:
            resp.close()

    content_type = r.headers.get("Content-Type", "application/octet-stream")
    response = StreamingHttpResponse(stream_generator(r), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
