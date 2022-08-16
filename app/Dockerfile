FROM python:3.7-alpine
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w", "4", "prom_monitoring_urls_web_app:create_app()", "--access-logfile=-", "--bind=0.0.0.0"]