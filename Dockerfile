FROM dullage/gunicorn-python:3.8-alpine
WORKDIR pi-vault
COPY requirements.txt requirements.txt
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev python3-dev libffi-dev openssl-dev
COPY . .
EXPOSE 5000
ENTRYPOINT gunicorn -w 4 --bind 0.0.0.0:5000 flasky:app
