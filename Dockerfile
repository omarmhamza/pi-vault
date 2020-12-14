FROM dullage/gunicorn:20.0-python3.8
WORKDIR pi-vault
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT gunicorn -w 4 --bind 0.0.0.0:5000 flasky:app
