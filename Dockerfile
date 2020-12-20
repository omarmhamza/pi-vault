FROM dullage/gunicorn:20.0-python3.8-alpine3.12
WORKDIR pi-vault
COPY requirements.txt requirements.txt
USER root
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev python3-dev libffi-dev openssl-dev
COPY . .
EXPOSE 5000
RUN adduser --disabled-password -hs "user"
USER user
ENTRYPOINT gunicorn -w 4 --bind 0.0.0.0:5000 flasky:app
