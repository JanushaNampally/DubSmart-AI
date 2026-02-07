from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from src.pipeline import run_pipeline

import os
import threading
import time

# -------------------------
# GLOBAL PIPELINE STATE
# -------------------------
PIPELINE_LOGS = []
PIPELINE_STATUS = {
    "running": False,
    "done": False,
    "output": None
}


def log(msg):
    PIPELINE_LOGS.append(msg)
    print(msg)


# -------------------------
# INDEX PAGE
# -------------------------
def index(request):
    return render(request, "dubbing/index.html")


@csrf_exempt
def start(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    if PIPELINE_STATUS["running"]:
        return JsonResponse({"message": "Already running"})

    video = request.FILES.get("video")
    if not video:
        return JsonResponse({"error": "No video uploaded"}, status=400)

    # ---- JOB FOLDER ----
    job_dir = os.path.join(settings.MEDIA_ROOT, "jobs", "job_001")
    os.makedirs(job_dir, exist_ok=True)

    input_path = os.path.join(job_dir, "input.mp4")
    with open(input_path, "wb+") as f:
        for chunk in video.chunks():
            f.write(chunk)

    # Reset state
    PIPELINE_LOGS.clear()
    PIPELINE_STATUS["running"] = True
    PIPELINE_STATUS["done"] = False
    PIPELINE_STATUS["output"] = None

    # ---- DEFINE RUNNER FIRST ----
    def pipeline_runner():
        try:
            output = run_pipeline(input_path, job_dir, log)
            PIPELINE_STATUS["output"] = (
                settings.MEDIA_URL + "jobs/job_001/dubbed.mp4"
            )
        finally:
            PIPELINE_STATUS["done"] = True
            PIPELINE_STATUS["running"] = False

    # ---- START THREAD ----
    threading.Thread(
        target=pipeline_runner,
        daemon=True
    ).start()

    # ---- RETURN HTTP RESPONSE ----
    return JsonResponse({"started": True})



def logs(request):
    stt = [l for l in PIPELINE_LOGS if ":" in l and "ERROR" not in l]
    return JsonResponse({
        "logs": PIPELINE_LOGS,
        "stt": "\n".join(stt)
    })


def status(request):
    return JsonResponse({
        "ready": PIPELINE_STATUS["done"],
        "url": PIPELINE_STATUS["output"]
    })
