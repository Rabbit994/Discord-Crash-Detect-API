FROM python:3.9

#Install FFMPEG
RUN apt update
RUN apt install -y ffmpeg
#Run PIP install
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

#Copy App into /app which is standard for python docker files
COPY ./app /app
#Run uvicorn server on port 8000 listening on all interfaces
EXPOSE 8000
CMD ["uvicorn", "app.main:app","--host","0.0.0.0"]