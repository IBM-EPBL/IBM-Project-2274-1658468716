FROM python:3.10.0-alpine
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-2.11.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
RUN pip install -r requirements.txt
EXPOSE 5000
RUN flask run
