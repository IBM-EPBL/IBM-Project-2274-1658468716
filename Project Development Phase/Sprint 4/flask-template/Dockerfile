FROM python:3.9.15
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
RUN flask run
