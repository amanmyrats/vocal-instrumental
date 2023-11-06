import os
from pathlib import Path
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from spleeter.separator import Separator
from pydub import AudioSegment
import numpy as np

@csrf_exempt
@api_view(['POST'])
def separate_view(request):
    file = request.FILES['file']
    try:
        input_audio = file
        output_dir = Path('output')
        separator = Separator("spleeter:2stems")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Load the input audio file
        audio = AudioSegment.from_file(input_audio)

        # Split the audio into smaller chunks (e.g., 30 seconds each)
        chunk_duration = 30 * 1000  # 30 seconds in milliseconds

        vocals_segments = []
        accompaniment_segments = []

        for start_time in range(0, len(audio), chunk_duration):
            chunk = audio[start_time:start_time + chunk_duration]

            # Export the chunk to a temporary file
            chunk_file = os.path.join(output_dir, f"chunk_{start_time}.mp3")
            chunk.export(chunk_file, format="mp3")

            # Process the chunk using Spleeter
            separator.separate_to_file(chunk_file, output_dir)

            # Load the separated vocal and accompaniment files
            vocal_file = os.path.join(output_dir, f"chunk_{start_time}", "vocals.wav")
            accompaniment_file = os.path.join(output_dir, f"chunk_{start_time}", "accompaniment.wav")

            vocals = AudioSegment.from_wav(vocal_file)
            accompaniment = AudioSegment.from_wav(accompaniment_file)

            vocals_segments.append(vocals)
            accompaniment_segments.append(accompaniment)

            # Remove the temporary files to save disk space
            os.remove(vocal_file)
            os.remove(accompaniment_file)
            os.remove(chunk_file)

        # Merge all vocal and accompaniment segments
        merged_vocals = sum(vocals_segments)
        merged_accompaniment = sum(accompaniment_segments)

        # Export the merged audio segments to separate files
        merged_vocals.export(os.path.join(output_dir, "vocals.mp3"), format="mp3")
        merged_accompaniment.export(os.path.join(output_dir, "accompaniment.mp3"), format="mp3")

        return HttpResponse('The vocals and instrumental have been successfully separated and saved to the current folder.')
    except Exception as f:
        print('general exception', str(f))
        return HttpResponseServerError('An error occurred during audio processing.')
