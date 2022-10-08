FROM python:3.6-slim
RUN python -m pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r ./requirements.txt
RUN mkdir /src
WORKDIR /src
COPY ./src /src
CMD [ "python","./worker.py" ]