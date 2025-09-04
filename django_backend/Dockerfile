FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN chmod +x /app/scripts/entrypoint.sh
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y netcat-traditional 

EXPOSE 8000

CMD ["./scripts/entrypoint.sh"]