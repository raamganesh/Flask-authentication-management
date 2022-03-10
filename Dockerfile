FROM python:3.9.6-alpine
RUN pip install -r requirements.txt
CMD ["export", "FLASK_APP=app_auth"]
CMD ["export", "FLASK_DEBUG=1"]
CMD ["python", "-m", "flask", "run"]
