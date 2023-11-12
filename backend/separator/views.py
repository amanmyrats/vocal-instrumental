import os
import tempfile
from django.http import HttpResponse, JsonResponse, HttpResponseServerError, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.decorators import api_view
from spleeter.separator import Separator
from pydub import AudioSegment
import zipfile

@csrf_exempt
@api_view(['POST'])
def separate_view(request):
    file = request.FILES['file']
    try:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)

        # Write the uploaded file to the temporary file
        with temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)

        # Path to the temporary file
        input_audio = temp_file.name

        # Output directory based on your Django app's BASE_DIR
        output_dir = os.path.join(settings.BASE_DIR, 'output')

        separator = Separator("spleeter:2stems")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        audio = AudioSegment.from_file(input_audio)

        chunk_duration = 30 * 1000
        vocals_segments = []
        accompaniment_segments = []

        for start_time in range(0, len(audio), chunk_duration):
            chunk = audio[start_time:start_time + chunk_duration]
            chunk_file = os.path.join(output_dir, f"chunk_{start_time}.mp3")
            chunk.export(chunk_file, format="mp3")
            separator.separate_to_file(chunk_file, output_dir)

            vocal_file = os.path.join(output_dir, f"chunk_{start_time}", "vocals.wav")
            accompaniment_file = os.path.join(output_dir, f"chunk_{start_time}", "accompaniment.wav")

            vocals = AudioSegment.from_wav(vocal_file)
            accompaniment = AudioSegment.from_wav(accompaniment_file)

            vocals_segments.append(vocals)
            accompaniment_segments.append(accompaniment)

            # os.remove(vocal_file)
            # os.remove(accompaniment_file)
            # os.remove(chunk_file)

        merged_vocals = sum(vocals_segments)
        merged_accompaniment = sum(accompaniment_segments)

        # Export the merged audio segments to separate files
        merged_vocals.export(os.path.join(output_dir, "vocals.mp3"), format="mp3")
        merged_accompaniment.export(os.path.join(output_dir, "accompaniment.mp3"), format="mp3")

        # Create a ZIP archive containing the separated audio files
        zip_file_path = os.path.join(output_dir, 'separated_audio.zip')
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(os.path.join(output_dir, 'vocals.mp3'), 'vocals.mp3')
            zipf.write(os.path.join(output_dir, 'accompaniment.mp3'), 'accompaniment.mp3')

        # Return the ZIP archive as a response
        with open(zip_file_path, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="separated_audio.zip"'
            return response
    except Exception as f:
        print('general exception', str(f))
        return HttpResponseServerError('An error occurred during audio processing')
    finally:
        os.remove(input_audio)
