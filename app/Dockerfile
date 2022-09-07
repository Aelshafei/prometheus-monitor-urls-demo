FROM python:3.7-alpine
WORKDIR /app
RUN addgroup -S flask && adduser -S flask -G flask
COPY --chown=flask:flask . /app
RUN pip install -r requirements.txt
USER flask
CMD ["gunicorn", "-w", "4", "prom_monitoring_urls_web_app:create_app()", "--access-logfile=-", "--bind=0.0.0.0"]