import os, subprocess, base64
import tempfile
from pathlib import Path
from django.http import HttpResponse, JsonResponse, HttpResponseServerError, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.decorators import api_view
from spleeter.separator import Separator
from rest_framework.response import Response
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

        separator = Separator("spleeter:2stems")

        # Output directory based on your Django app's BASE_DIR
        output_dir = os.path.join(settings.BASE_DIR, 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        separator.separate_to_file(input_audio, output_dir)

        # BELOW CODE IS INTENDED FOR OPTIMIZATION
        # IN CASE OF LACK OF RESOURCE IT SEPARATE FILE
        # INTO CHUNKS FIRST, THEN DO SEPARATION WORK ONE BY ONE
        # AT THEN END IT MERGES ALL RESULT AUDIO FILES INTO FINAL AUDIO
        # audio = AudioSegment.from_file(input_audio)

        # chunk_duration = 30 * 1000
        # vocals_segments = []
        # accompaniment_segments = []

        # for start_time in range(0, len(audio), chunk_duration):
        #     chunk = audio[start_time:start_time + chunk_duration]
        #     chunk_file = os.path.join(output_dir, f"chunk_{start_time}.mp3")
        #     chunk.export(chunk_file, format="mp3")

        #     # Use Spleeter to separate vocals and accompaniment
        #     separator.separate_to_file(chunk_file, output_dir)
        #     # Define the command
        #     # command = ['spleeter', 'separate', '-p', 'spleeter:2stems', '-o', output_dir, chunk_file]
        #     # Run the command using subprocess.run
        #     # subprocess.run(command, check=True)
        
        #     vocal_file = os.path.join(output_dir, f"chunk_{start_time}", "vocals.wav")
        #     accompaniment_file = os.path.join(output_dir, f"chunk_{start_time}", "accompaniment.wav")

        #     vocals = AudioSegment.from_wav(vocal_file)
        #     accompaniment = AudioSegment.from_wav(accompaniment_file)

        #     vocals_segments.append(vocals)
        #     accompaniment_segments.append(accompaniment)

        #     # os.remove(vocal_file)
        #     # os.remove(accompaniment_file)
        #     # os.remove(chunk_file)

        # merged_vocals = sum(vocals_segments)
        # merged_accompaniment = sum(accompaniment_segments)

        # Export the merged audio segments to separate files
        # merged_vocals.export(os.path.join(output_dir, "vocals.mp3"), format="mp3")
        # merged_accompaniment.export(os.path.join(output_dir, "accompaniment.mp3"), format="mp3")

        # # Create a ZIP archive containing the separated audio files
        # zip_file_path = os.path.join(output_dir, 'separated_audio.zip')
        # with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        #     zipf.write(os.path.join(output_dir, 'vocals.mp3'), 'vocals.mp3')
        #     zipf.write(os.path.join(output_dir, 'accompaniment.mp3'), 'accompaniment.mp3')

        # # Return the ZIP archive as a response
        # with open(zip_file_path, 'rb') as zip_file:
        #     response = HttpResponse(zip_file.read(), content_type='application/zip')
        #     response['Content-Disposition'] = 'attachment; filename="separated_audio.zip"'
        #     return response

        # Read the separated audio files
        vocals_file = os.path.join(output_dir, Path(temp_file.name).stem, 'vocals.wav')
        accompaniment_file = os.path.join(output_dir, Path(temp_file.name).stem, 'accompaniment.wav')

        with open(vocals_file, 'rb') as vocals_file:
            vocals_content = base64.b64encode(vocals_file.read()).decode('utf-8')

        with open(accompaniment_file, 'rb') as accompaniment_file:
            accompaniment_content = base64.b64encode(accompaniment_file.read()).decode('utf-8')


        # Return the response as JSON
        response_dict = {
            'vocals': vocals_content,
            'accompaniment': accompaniment_content,
        }

        return JsonResponse(response_dict)
    except Exception as f:
        print('general exception', str(f))
        return HttpResponseServerError('An error occurred during audio processing')
    except subprocess.CalledProcessError as e:
        # Handle errors, log them, and return an error response
        error_message = f'Error executing Spleeter command: {e}'
        # Log the error message
        print(error_message)
        # Return an error response
        return HttpResponse(error_message, status=500)
    finally:
        os.remove(input_audio)
