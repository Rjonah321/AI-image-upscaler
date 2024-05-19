FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN cat requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 5000

ENV FLASK_APP=flask_app.py

RUN adduser --disabled-password appuser
USER appuser

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]