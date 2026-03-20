FROM python:3.14-trixie

RUN mkdir -p /opt/app

WORKDIR /opt/app

COPY requirements.txt ./
COPY wikievents.py ./

RUN pip install -r requirements.txt

CMD [ "python", "wikievents.py" ]