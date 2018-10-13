FROM python:3

EXPOSE 5000

ADD rr.py /

ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python3", "./rr.py" ]
