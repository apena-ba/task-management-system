FROM python:3.11-slim

RUN apt-get update && apt-get install -y netcat-traditional curl

WORKDIR /app
COPY . .

RUN chmod +x /app/scripts/entrypoint.sh
RUN pip3 install -r requirements.txt

EXPOSE 8000