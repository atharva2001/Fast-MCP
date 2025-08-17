FROM python:3.12-slim

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt 

EXPOSE 8000 

COPY . .

CMD [ "python3", "server.py" ]    

