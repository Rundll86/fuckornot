FROM python:3.10-slim

COPY ./backend /app/backend
COPY ./frontend /app/frontend
COPY ./public /app/public
COPY ./requirements.txt /app
RUN mkdir /app/data
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python", "backend/server.py"]