FROM ubuntu:latest
RUN apt update
RUN apt-get upgrade
RUN apt-get install -y python3 
RUN apt-get install -y python3-pip
COPY . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]