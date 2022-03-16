FROM python:3.9.6-alpine
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENV FLASK_APP=app_auth
ENV FLASK_DEBUG=1
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]
EXPOSE 80
