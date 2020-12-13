FROM tiangolo/uwsgi-nginx-flask:python3.8
COPY . .
RUN cd install; ./install.sh;
ENTRYPOINT uwsgi --socket 0.0.0.0:5000 --protocol=http -w flasky:app --ini server.ini
