# base image 
FROM python:3.10.7

# setup environment variable 
ENV DockerHOME=/home/app/backend 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

# set work directory  
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# copy whole project to your docker home directory. 
COPY . /home/app/backend 

RUN pip install -r requirements.txt

RUN apt -y update && apt -y upgrade

RUN apt -y install ffmpeg

EXPOSE 8000

CMD ["python", "main.py"]