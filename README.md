# vocal-instrumental
Separating vocal and instrumental, with django backend and angular frontend. Spleeter library is used to do this.

- WITH DOCKER
1 - Be sure that you have docker in your system. If you don't please visit installation page for docker: https://docs.docker.com/engine/install/


2 - Clone the repository, then cd into backend folder. Then run container with command: 
    ```docker compose up```


3 - Open any browser and navigate to 127.0.0.1:8000/

- WITH LOCAL DEV SERVER
1- This is written with python version 3.8.10. So any python of version 3.8.xx should be OK.


2-In your system(windows, mac, linux) be sure that ```ffmpeg``` and ```libsndfile``` are 
installed, and path of both are added to path(environmental variables). To be sure, 
after installation write 'ffmpeg' to terminal, if there is no error then it is good to go. And to check if another one is installed correctly. To check write 'sndfile-cmp' to terminal,
again if there is no error then you are good to go.


3 - Clone or download this repository

4 - Goto downloaded folder, and navigate to backend folder and create virtual environment
    ```python3 -m venv venv``` 
    or if you are on windows 
    ```python -m venv venv```

5 - Activate vitual environment. In terminal:
    ```source venv/bin/activate```
    or if you are on windows 
    ```venv/Scripts/activate```

6 - Inside activated virtual environment install necessary packages
    ```pip3 install -r requirements.txt```  
    or if you are on windows 
    ```pip install -r requirements.txt```

7 - Run the server
    ```python3 manage.py runserver``` 
    or if you are on windows 
    ```python manage.py runserver``` 

8 - Navigate to your browser and open localhost:8000

9 - After you send you mp3 file, it will retieve separated audio files and you can play it


ERROR???: Spleeter has pre trained models to work with already. But they are not available locally. So when this application starts first time, spleeter automatically downloads it from remote repository for once, later it uses it. Sometimes it cannot download that, download process fails with SSL_ERROR. In this case download pre_trained models from repository, apprx 60-70mb (https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems.tar.gz). Then place it under backend/pretrained_models/2stems/(downloaded files). Then try again.


What to do next?

- Frontend with angular.
- Generated audio files are too big, it has to be optimized.
- At the moment it processes one file at once on batch, later it can cause performance issues and out of memory issues, optimization is need here by separating audio files into chunks. So that it can be memory friendly.
- Generated files are stored in storage for the moment, it is done for development purposes. Later backend will delete it after sending it to client. This way storage will not be throttled for nothing.