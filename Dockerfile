FROM python:3.7.2

ADD . /flask-deploy

WORKDIR /flask-deploy

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python app.py