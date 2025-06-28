FROM python:3.10-slim

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g yarn

RUN yarn install
RUN yarn build

EXPOSE 5000
CMD ["python", "server.py"]