FROM python:3.8-alpine
WORKDIR /
ENV FLASK_APP auth.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]