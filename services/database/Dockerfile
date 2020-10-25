FROM python:3.8-alpine
WORKDIR /database
ENV FLASK_APP database.py
ENV FLASK_DEBUG=1
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["flask", "run"]