# set base image (host OS)
FROM python:3.7.8
#Add additonal packages
#RUN apt-get update
RUN apt-get --fix-missing update && apt-get --fix-broken install 
RUN apt-get install -y poppler-utils && apt-get install -y tesseract-ocr 
#RUN apt-get install -y libtesseract-dev && apt-get install -y libleptonica-dev && ldconfig 
RUN apt-get install -y ffmpeg libsm6 libxext6

# set the working directory in the container
#WORKDIR /

COPY . /grp10

WORKDIR /grp10
# copy the dependencies file to the working directory
#COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

RUN python3 -m nltk.downloader punkt

RUN pip install fastapi uvicorn
RUN pip install python-multipart

# copy the content of the local src directory to the working directory
#COPY src/ .

# copy the content of the local app directory to the working directory
#COPY . /app#

# set the working directory in the container
#WORKDIR /
EXPOSE 8000
CMD ["uvicorn", "main:app" ]

# command to run on container start
#CMD [ "python3", "./main.py" ]
