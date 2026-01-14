FROM python:3.12-slim

WORKDIR /app
COPY server.py .

RUN pip install requests

EXPOSE 5000
CMD ["python", "server.py"]

