# vocal-instrumental
Separating vocal and instrumental, with django backend and angular frontend

1 - Clone or download this repository

2 - Goto downloaded folder and create virtual environment
    ```python3 -m venv venv```

3 - Install necessary packages
    ```pip3 install -r requirements.txt```

4 - Run the server
    ```python3 manage.py runserver```

5 - Navigate to your browser and open localhost:8000

6 - After you send you mp3 file, It will save it to 'output', which is located inside your django project


What to do next?

Frontend with angular, when user uploads mp3 it will send back 2 mp3 files, which are vocals.mp3 and
accompaniment.mp3.